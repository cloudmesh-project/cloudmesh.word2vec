#!/bin/bash
spark_master=`hostname -i`

/opt/spark/bin/spark-submit --master yarn --deploy-mode client --executor-memory 1g \
--conf "spark.app.id=word2vec_use_model" /opt/word2vec/data_process/use_word2vec_model.py \
hdfs://${spark_master}:8020/word2vec/model \
$1 $2 $3 $4 $5
