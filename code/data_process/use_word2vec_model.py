from __future__ import print_function
from pyspark import SparkConf, SparkContext
from pyspark.ml.feature import Word2VecModel
from pyspark.sql import SparkSession
import pandas as pd

import csv

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('/opt/word2vec/config.properties')

# get config data
spark_master = config.get('SparkSection', 'spark_master')
spark_executor_memory = sys.argv[2]
min_word_count = sys.argv[3]
num_iterations = sys.argv[4]
vector_size = sys.argv[5]
debug_flag = sys.argv[6]
synonym_test_file = config.get('DataSection', 'synonym_test_file')
synonym_result_file = config.get('DataSection', 'synonym_result_file')


conf = (SparkConf()
         .setMaster(spark_master)
         .setAppName("WikiFindSynonyms")
         .set("spark.executor.memory", spark_executor_memory))
sc = SparkContext(conf = conf)


spark = SparkSession.builder.master(spark_master) \
        .appName("WikiWord2Vec") \
        .config("spark.executor.memory", spark_executor_memory) \
        .getOrCreate()

model = Word2VecModel.load(sys.argv[1])



with open(synonym_test_file, 'r') as f:
    reader = csv.reader(f)
    orig_words = list(reader)
    f.close()


listPDDF = []
for orig_word in orig_words:
    try:
        synonymsDF = model.findSynonyms(orig_word[0], 10)
        synonymsPDDF = synonymsDF.toPandas()

        lst = []
        for i in synonymsPDDF['word']:
            lst.append(orig_word[0])
        synonymsPDDF['original_word'] = lst

        listPDDF.append(synonymsPDDF)
    except:
        print("Error in word - %s" % word)

resultPDDF = pd.concat(listPDDF)

with open(synonym_result_file, 'w') as rf:
    writer = csv.writer(rf)
    resultPDDF.to_csv(rf)
    rf.close()

spark.stop()
