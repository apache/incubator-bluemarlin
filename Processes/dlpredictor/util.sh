#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

if false
then
    spark-submit --master yarn --num-executors 8 --executor-cores 5 --conf spark.driver.maxResultSize=2048m --executor-memory 16G --driver-memory 16G $SCRIPTPATH/util-scripts/dense_sparse_uckeys.py
fi

if false
then
    spark-submit --master yarn --num-executors 8 --executor-cores 5 --conf spark.driver.maxResultSize=2048m --executor-memory 16G --driver-memory 16G $SCRIPTPATH/util-scripts/dense_sparse_count.py
fi

if true
then
    spark-submit --master yarn --num-executors 8 --executor-cores 5 --conf spark.driver.maxResultSize=2048m --executor-memory 16G --driver-memory 16G $SCRIPTPATH/util-scripts/fact_data_count.py
fi


