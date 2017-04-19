#!/bin/bash
spark_master=`hostname -i`

/opt/spark/bin/spark-submit --master yarn --deploy-mode client --executor-memory 1g \
--conf "spark.app.id=word2vec_find_relations" /opt/word2vec/data_process/find_relations.py \
hdfs://${spark_master}:8020/word2vec/model \
hdfs://${spark_master}:8020/word2vec/relationstest.csv
