from __future__ import print_function
from pyspark.ml.feature import Word2VecModel

def getAnalogy(s, model):
    qry = model.transform(s[0]) - model.transform(s[1]) - model.transform(s[2])
    res = model.findSynonyms((-1)*qry,5) # return 5 "synonyms"
    res = [x[0] for x in res]
    for k in range(0,3):
        if s[k] in res:
            res.remove(s[k])
    return res[0]