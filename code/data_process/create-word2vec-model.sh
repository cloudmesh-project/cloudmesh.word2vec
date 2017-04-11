#!/bin/bash
spark_master=$1
spark-submit --master spark://${spark_master}:7077 /opt/word2vec/code/data_process/create-word2vec-model.py
