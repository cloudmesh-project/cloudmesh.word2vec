from __future__ import print_function
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

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('/opt/word2vec/config.properties')



# get config data
data_location = config.get('DataSection', 'data_location')
model_location = config.get('DataSection', 'model_location')
spark_master = config.get('SparkSection', 'spark_master')
spark_executor_memory = config.get('SparkSection', 'spark_executor_memory')
min_word_count = config.get('ModelSection', 'min_word_count')
num_iterations = config.get('ModelSection', 'num_iterations')
vector_size = config.get('ModelSection', 'vector_size')
debug_flag = config.get('Debug', 'debug')

conf = (SparkConf()
         .setMaster(spark_master)
         .setAppName("WikiWord2Vec")
         .set("spark.executor.memory", spark_executor_memory))
sc = SparkContext(conf = conf)


# DataFrame Mechanism
spark = SparkSession.builder.master(spark_master) \
        .appName("WikiWord2Vec") \
        .config("spark.executor.memory", spark_executor_memory) \
        .getOrCreate()


inp = sc.textFile(data_location).map(lambda text: re.sub('[^a-zA-Z0-9\n\.]',' ', text))
row = Row("text")
df = inp.map(row).toDF()
tokenizer = Tokenizer(inputCol="text", outputCol="words")
tokDF = tokenizer.transform(df)
remover = StopWordsRemover(inputCol="words", outputCol="filteredWords")
filteredDF = remover.transform(tokDF)

word2vec = Word2Vec(inputCol="words", outputCol="word2vec")
word2vec.setVectorSize(int(vector_size))
word2vec.setMinCount(int(min_word_count))
model = word2vec.fit(filteredDF)
model.write().save(model_location)

if debug_flag == 1:
    synonyms = model.findSynonyms('sachin',10)
    synonyms.show()

spark.stop()
