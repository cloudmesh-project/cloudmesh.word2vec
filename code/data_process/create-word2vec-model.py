from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('/opt/word2vec/config.properties')

import pyspark
from pyspark import SparkConf, SparkContext
from pyspark.sql import Row
from pyspark.ml.feature import Tokenizer, RegexTokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import Word2Vec
from pyspark.sql import SparkSession

import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import os

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('/opt/word2vec/config.properties')

sys.path.append(os.path.abspath('/opt/word2vec/perfmonitor'))
import monitor_spark_app
#from ../perfmonitor import monitor_spark_app

# get config data
spark_master = config.get('SparkSection', 'spark_master')
spark_executor_memory = config.get('SparkSection', 'spark_executor_memory')
spark_driver_memory = config.get('SparkSection', 'spark_driver_memory')
max_result_size = config.get('SparkSection', 'max_result_size')
default_parallelism = config.get('SparkSection', 'default_parallelism')

min_word_count = config.get('ModelSection', 'min_word_count')
num_iterations = config.get('ModelSection', 'num_iterations')
vector_size = config.get('ModelSection', 'vector_size')
debug_flag = config.get('Debug', 'debug')

conf = SparkConf().setAppName("WikiWord2Vec")
sc = SparkContext(conf = conf)


# DataFrame Mechanism
spark = SparkSession.builder.master(spark_master) \
        .appName("WikiWord2Vec") \
        .config("spark.executor.memory", spark_executor_memory) \
        .config("spark.driver.memory", spark_driver_memory) \
        .config("spark.driver.maxResultSize", max_result_size) \
        .getOrCreate()


spark = SparkSession.builder.master(spark_master) \
        .appName("WikiWord2Vec") \
        .config("spark.executor.memory", spark_executor_memory) \
        .getOrCreate()


inp = sc.textFile(sys.argv[1]).map(lambda text: re.sub('[^a-zA-Z0-9\n\.]',' ', text))
inp.persist(pyspark.StorageLevel.MEMORY_AND_DISK)

row = Row("text")
df = inp.map(row).toDF()
df.persist(pyspark.StorageLevel.MEMORY_AND_DISK)

tokenizer = Tokenizer(inputCol="text", outputCol="words")
tokDF = tokenizer.transform(df)
tokDF.persist(pyspark.StorageLevel.MEMORY_AND_DISK)

#remover = StopWordsRemover(inputCol="words", outputCol="filteredWords")
#filteredDF = remover.transform(tokDF)

word2vec = Word2Vec(inputCol="words", outputCol="word2vec")
word2vec.setVectorSize(int(vector_size))
word2vec.setMinCount(int(min_word_count))

#model = word2vec.fit(filteredDF)
model = word2vec.fit(tokDF)

model.write().save(sys.argv[2])

#get app stats
monitor_spark_app.get_app_status_once("create-word2vec-model.py", sys.argv[3])

if debug_flag == 1:
    synonyms = model.findSynonyms('sachin',10)
    synonyms.show()

spark.stop()
