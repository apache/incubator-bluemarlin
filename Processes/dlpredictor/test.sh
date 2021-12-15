#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

if true
then
    spark-submit --master yarn --num-executors 8 --executor-cores 5 --conf spark.driver.maxResultSize=2048m --executor-memory 16G --driver-memory 16G --py-files $SCRIPTPATH/lib/imscommon-2.0.0-py2.7.egg $SCRIPTPATH/tests/time_series_prediction_check/test_dlpredictor_system_errors_1.py
fi

if false
then
    spark-submit --master yarn --num-executors 8 --executor-cores 5 --conf spark.driver.maxResultSize=2048m --executor-memory 16G --driver-memory 16G --py-files $SCRIPTPATH/lib/imscommon-2.0.0-py2.7.egg $SCRIPTPATH/tests/fact_data_prediction_check/test_dlpredictor_system_errors_2.py
fi



