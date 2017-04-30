from __future__ import print_function
from pyspark.ml.feature import Word2VecModel
from pyspark.sql import SparkSession

import csv

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('/opt/word2vec/config.properties')

# get config data
spark_master = config.get('SparkSection', 'spark_master')
spark_executor_memory = sys.argv[3]
min_word_count = sys.argv[4]
num_iterations = sys.argv[5]
vector_size = sys.argv[6]
debug_flag = sys.argv[7]
relations_result_file = config.get('DataSection', 'relations_result_file')


spark = SparkSession \
    .builder \
    .appName("WikiFindSynonyms") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.driver.maxResultSize", "1g") \
    .config("spark.default.parallelism", "4") \
    .getOrCreate()

model = Word2VecModel.load(sys.argv[1])
modelDF = model.getVectors()
modelDF.show()
print("Total number of records in modelDF = %d" % modelDF.count())
modelDF = modelDF.repartition(1000, 'word')


testDataDF = spark.read.csv(sys.argv[2], header=True)
testDataDF.show()
print("Total number of records in testDataDF = %d" % testDataDF.count())

testDataDF = testDataDF.join(modelDF, testDataDF.word1 == modelDF.word,'inner')\
                    .select(testDataDF.word1, testDataDF.word2, \
                            testDataDF.word3, modelDF.vector)
testDataDF.show()
testDataDF = testDataDF.withColumnRenamed('vector', 'vec1')

testDataDF = testDataDF.join(modelDF, testDataDF.word2 == modelDF.word,'inner')\
                    .select(testDataDF.word1, testDataDF.word2, \
                            testDataDF.word3, testDataDF.vec1, \
                            modelDF.vector)

testDataDF = testDataDF.withColumnRenamed('vector', 'vec2')
testDataDF.show()

testDataDF = testDataDF.join(modelDF, testDataDF.word3 == modelDF.word,'inner')\
                    .select(testDataDF.word1, testDataDF.word2, \
                            testDataDF.word3, testDataDF.vec1, \
                            testDataDF.vec2, modelDF.vector)

testDataDF = testDataDF.withColumnRenamed('vector', 'vec3')
testDataDF.show()

testDataPDDF = testDataDF.toPandas()
testDataPDDF['vec4'] = (testDataPDDF['vec1'] - testDataPDDF['vec2'] + \
                       testDataPDDF['vec3'])


with open(relations_result_file, 'w') as rf:
    writer = csv.writer(rf)

    for index, row in testDataPDDF.iterrows():
        lstSynonyms = model.findSynonyms(row['vec4'], 10).collect()
        print("Synonyms count = %d " % len(lstSynonyms))
        for s in lstSynonyms:
            print(row['word1'], row['word2'], \
                   row['word3'], s)
            templst = []
            templst.append(row['word1'])
            templst.append(row['word2'])
            templst.append(row['word3'])
            templst.append(s['word'])
            writer.writerow(templst)
    rf.close()

spark.stop()
