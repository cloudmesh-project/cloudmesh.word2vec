#!/bin/bash
spark_master=`hostname -i`

/opt/spark/bin/spark-submit --master yarn --deploy-mode client --executor-memory 1g \
--name word2vec_validate --conf "spark.app.id=word2vec_validate" /opt/word2vec/data_process/use_word2vec_model.py \
hdfs://${spark_master}:8020/word2vec/model 
