#!/bin/bash
spark_master=`hostname -i`

spark-submit --master yarn --deploy-mode client --executor-memory 1g \
--conf "spark.app.id=word2vec" /opt/word2vec/data_process/create-word2vec-model.py \
hdfs://${spark_master}:8020/word2vec/crawldb \
hdfs://${spark_master}:8020/word2vec/model \
http://${spark_master}:4040
