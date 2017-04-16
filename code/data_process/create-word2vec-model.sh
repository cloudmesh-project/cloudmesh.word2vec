#!/bin/bash
#spark-submit --master spark://usl03917.local:7077  --files=/Users/Avadhoot/msdatascience/course524/cloudmesh/cloudmesh.word2vec/code/perflog/metrics.properties --conf spark.metrics.conf=/Users/Avadhoot/msdatascience/course524/cloudmesh/cloudmesh.word2vec/code/perflog//metrics.properties create-word2vec-model.py

spark-submit --master spark://usl03917.local:7077  create-word2vec-model.py &> temp.out &
python ../perfmonitor/monitor_spark_app.py
