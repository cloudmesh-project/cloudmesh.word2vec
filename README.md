### Pre-requisites

If you have a cluster already deployed you can skip this section. To deploy a 3 node chameleon cluster, use the following:

    cm reset
    pip uninstall cloudmesh_client
    pip install -U cloudmesh_client
    cm key add --ssh
    cm refresh on
    cm cluster define --count 1 --image CC-Ubuntu14.04 --flavor m1.medium
    cm hadoop define spark pig
    cm hadoop sync
    cm hadoop deploy
    cm cluster cross_ssh

### clone or download repository

git clone https://github.com/cloudmesh/cloudmesh.word2vec.git 

### update hosts file with ip of your primary node on your cluster 
  (Note: On the cluster, first node becomes master)

```sh
cd ansible-word2vec
vi hosts
```

### execute script to deploy and run spark job

    ansible-word2vec/run.sh

run script will: 
- deploy code
- run the crawler for collecting the training set
- submit the job on spark


## Appendix:

### Manual steps for running the crawler and spark job

##### Setup Crawler
 - Configure various properties in config.properties. For crawler, the
important parameters are A)data_location B)seed_list C)max_pages
 -  configure the seed pages in wiki_crawl_seedlist.csv
 - create folder 'crawldb' under 'code'
 - execute crawler
```sh
    python wikicrawl.py
```
#### Create Word2Vec Model
 - create folder 'model' under 'code' for saving the model
 - Configure various properties in config.properties
 - start your spark cluster
 - configure the spark-master URL in create-word2vec-model.sh.
 - execute the create-word2vec-model
```sh
    bash create-word2vec-model.sh
```

#### Query Word2Vec Model
 - execute use_word2vec_model.py
 - The test file location can be defined in config.properties
(synonym_test_file). The default value is stest.csv
 - The generated result file will be stored in stestresult.csv by default. It
 can be changed using config.properties
```sh
    spark-submit use_word2vec_model.py
```
