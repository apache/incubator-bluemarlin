# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
#                                                 * "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

"""
spark-submit --master yarn --executor-memory 16G --driver-memory 24G --num-executors 10 --executor-cores 5 --jars spark-tensorflow-connector_2.11-1.15.0.jar --conf spark.hadoop.hive.exec.dynamic.partition=true --conf spark.hadoop.hive.exec.dynamic.partition.mode=nonstrict pipeline/_main_trainready_india.py config.yml
input: trainready table
output: dataset readable by trainer in tfrecord format
"""

import yaml
import argparse
import os
import timeit
from pyspark import SparkContext
from pyspark.sql import functions as fn
from pyspark.sql.functions import lit, col, udf, collect_list, concat_ws, first, create_map, monotonically_increasing_id
from pyspark.sql.functions import count, lit, col, udf, expr, collect_list, explode
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType, ArrayType, StringType,BooleanType
from pyspark.sql import HiveContext
from pyspark.sql.session import SparkSession
from datetime import datetime, timedelta
from lookalike_model.pipeline.util import write_to_table, write_to_table_with_partition, print_batching_info, resolve_placeholder, load_config, load_batch_config, load_df
from itertools import chain
from pyspark.sql.types import IntegerType, ArrayType, StringType, BooleanType, FloatType, DoubleType
from util import write_to_table, write_to_table_with_partition, save_pickle_file


def generate_tfrecord(sc, hive_context, tf_statis_path, keyword_table, cutting_date, length, trainready_table, tfrecords_hdfs_path_train, tfrecords_hdfs_path_test):

    def str_to_intlist(table):
        ji = []
        for k in [table[j].decode().split(",") for j in range(len(table))]:
            s = []
            for a in k:
                b = int(a.split(":")[1])
                s.append(b)
            ji.append(s)
        return ji

    def list_of_list_toint(table):
        ji = []
        for k in [table[j].decode().split(",") for j in range(len(table))]:
            s = [int(a) for a in k]
            ji.append(s)
        return ji

    def flatten(lst):
        f = [y for x in lst for y in x]
        return f

    def padding(kwlist,length):
        diff = length-len(kwlist)
        print(len(kwlist))
        print(length)
        print(diff)
        temp_list = [0 for i in range(diff)]
        padded_keyword = kwlist + temp_list
        return padded_keyword

    def create_dataset(df_panda ,click, keyword):
        t_set = []
        for i in range(len(df_panda.aid_index)):
            click_counts = click[i]
            keyword_int = keyword[i]
            aid_index = df_panda.aid_index[i]
            for m in range(len(click_counts)):
                for n in range(len(click_counts[m])):
                    if (click_counts[m][n] != 0):
                        pos = (aid_index, flatten(keyword_int[m + 1:m + 1 + length]), keyword_int[m][n], 1)
                        if len(pos[1]) >= 1:
                            t_set.append(pos)
                    elif (m % 5 == 0 and n % 2 == 0):
                        neg = (aid_index, flatten(keyword_int[m + 1:m + 1 + length]), keyword_int[m][n], 0)
                        if len(neg[1]) >= 1:
                            t_set.append(neg)
        return t_set

    def generating_dataframe(dataset, spark ):
        data_set = [(int(tup[0]), tup[1], int(tup[2]), int(tup[3])) for tup in dataset]
        df = spark.createDataFrame(data=data_set, schema=deptColumns)
        df = df.withColumn("sl", udf(lambda x: len(x), IntegerType())(df.keyword_list))
        df = df.where(df.sl > 5)
        df = df.withColumn('max_length', lit(df.agg({'sl': 'max'}).collect()[0][0]))
        df = df.withColumn('keyword_list_padded',
                                     udf(padding, ArrayType(IntegerType()))(df.keyword_list, df.max_length))
        return df

    def generate_tf_statistics(testsetDF, trainDF, keyword_df, tf_statis_path):
        tfrecords_statistics = {}
        tfrecords_statistics['test_dataset_count'] = testsetDF.count()
        tfrecords_statistics['train_dataset_count'] = trainDF.count()
        tfrecords_statistics['user_count'] = trainDF.select('aid').distinct().count()
        tfrecords_statistics['item_count'] = keyword_df.distinct().count() + 1
        save_pickle_file(tfrecords_statistics, tf_statis_path)


    command = """SELECT * FROM {}"""
    df = hive_context.sql(command.format(trainready_table))

    df = df.withColumn('interval_starting_time', df['interval_starting_time'].cast(ArrayType(IntegerType())))
    df = df.withColumn('_kwi', udf(list_of_list_toint, ArrayType(ArrayType(IntegerType())))(df.kwi))
    df = df.withColumn('click_counts', udf(str_to_intlist, ArrayType(ArrayType(IntegerType())))(df['kwi_click_counts']))
    df = df.withColumn('total_click', udf(lambda x: sum([item for sublist in x for item in sublist]), IntegerType())(df.click_counts))
    df = df.where(df.total_click != 0)
    df = df.withColumn('indicing', udf(lambda y: len([x for x in y if x >= cutting_date]), IntegerType())(df.interval_starting_time))
    df = df.withColumn('keyword_int_train', udf(lambda x, y: x[y:],ArrayType(ArrayType(IntegerType())))(df._kwi, df.indicing))
    df = df.withColumn('keyword_int_test', udf(lambda x, y: x[:y],ArrayType(ArrayType(IntegerType())))(df._kwi, df.indicing))
    df = df.withColumn('click_counts_train', udf(lambda x, y: x[y:],ArrayType(ArrayType(IntegerType())))(df.click_counts, df.indicing))
    df = df.withColumn('click_counts_test', udf(lambda x, y: x[:y],ArrayType(ArrayType(IntegerType())))(df.click_counts, df.indicing))

    spark = SparkSession(sc)
    deptColumns = ["aid", "keyword_list", "keyword", "label"]

    df_panda = df.select('click_counts_train', 'keyword_int_train', 'aid_index').toPandas()
    train_set = create_dataset(df_panda,df_panda.click_counts_train, df_panda.keyword_int_train)
    trainDF = generating_dataframe(train_set, spark = spark)
    trainDF.write.format("tfrecords").option("recordType", "Example").mode("overwrite").save(tfrecords_hdfs_path_train)


    df_panda = df.select('click_counts_test', 'keyword_int_test', 'aid_index').toPandas()
    test_set = create_dataset(df_panda, df_panda.click_counts_test, df_panda.keyword_int_test)
    testsetDF = generating_dataframe(test_set, spark = spark)
    testsetDF.write.format("tfrecords").option("recordType", "Example").mode("overwrite").save(tfrecords_hdfs_path_test)


    command = "SELECT * from {}"
    keyword_df = hive_context.sql(command.format(keyword_table))
    generate_tf_statistics(testsetDF, trainDF, keyword_df, tf_statis_path)

def run(sc, hive_context, cfg):
    cfgp = cfg['pipeline']
    cfg_train = cfg['pipeline']['main_trainready']
    trainready_table = cfg_train['trainready_output_table']
    cfg_tfrecord = cfg['pipeline']['tfrecords']
    tfrecords_hdfs_path_train = cfg_tfrecord['tfrecords_hdfs_path_train']
    tfrecords_hdfs_path_test = cfg_tfrecord['tfrecords_hdfs_path_test']
    cutting_date = cfg['pipeline']['cutting_date']
    length = cfg['pipeline']['length']
    tf_statis_path = cfgp['tfrecords']['tfrecords_statistics_path']
    keyword_table = cfgp['main_keywords']['keyword_output_table']


    generate_tfrecord(sc, hive_context, tf_statis_path, keyword_table, cutting_date, length, trainready_table, tfrecords_hdfs_path_train, tfrecords_hdfs_path_test)


if __name__ == "__main__":
    """
    This program performs the followings:
    adds normalized data by adding index of features
    groups data into time_intervals and dids (labeled by did)
    """
    sc, hive_context, cfg = load_config(description="pre-processing train ready data")
    resolve_placeholder(cfg)
    run(sc=sc, hive_context=hive_context, cfg=cfg)
    sc.stop()
