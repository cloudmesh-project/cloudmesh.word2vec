### Pre-requisites

If you have a cluster already deployed you can skip this section. To deploy a 3 node chameleon 
cluster, use the following:

    cm reset
    pip uninstall cloudmesh_client
    pip install -U cloudmesh_client
    cm key add --ssh
    cm refresh on
    cm cluster define --count 3 \
        --image CC-Ubuntu14.04 --flavor m1.medium
    cm hadoop define spark pig
    cm hadoop sync
    cm hadoop deploy
    cm cluster cross_ssh

### clone or download repository

`git clone https://github.com/cloudmesh/cloudmesh.word2vec.git`

### update hosts file with ip of your primary node on your cluster 
  (Note: On the cluster, first node becomes master)

```sh
cd ansible-word2vec
vi hosts
```

### execute script to deploy and run spark job

```sh
cd ansible-word2vec
./run.sh
```
run script will: 
- deploy code
- run the crawler for collecting the training set
- submit the job on spark

[Execution log](benchmark/chameleon_2_node/executionlog.txt)

### Test results

[single node](benchmark/single_node/README.md)

[multinode node Chameleon](benchmark/chameleon_2_node/README.md)

[multinode node Jetstream](benchmark/jetstream_2_nodes/README.md)

### Cleanup
To cleanup installation from cluster
```sh
cd ansible-word2vec
ansible-playbook word2vec_cleanup.yaml
```

## Appendix:

### Troubleshooting

1. If the installation `run.sh` script fails in middle due to some reason, execute the 
cleanup script before re-triggering run script again. The run script may fail due to variety of 
reasons like failed to shh, hadoop not available etc

2. If the run script fails due to spark memory errors, you can modify the spark memory setting in
`code/config.properties` push the code to a git feature branch for example `spark_test`. Modify 
`word2vec_setup.yaml` git section `version=master` to point to `spark_test` branch and execute the 
run script.

3. If hadoop goes into safe mode, goto the cluster namenode and execute
```sh
    /opt/hadoop$ bin/hadoop dfsadmin -safemode leave
```
This will remove the cluster from safe mode.


### Manual steps for running the crawler and spark job

##### Setup Wiki Crawler
 - Configure various properties in config.properties. For crawler, the
important parameters are A)data_location B)seed_list C)max_pages
 - configure the seed pages in wiki_crawl_seedlist.csv
 - create folder 'crawldb' under 'code' (or the location specified in the config file)
 - execute crawler
```sh
    python wikicrawl.py
```

##### Setup News Crawler
 - configure various properties in config.properties. For news crawler, the
important parameters are A)data_location B)news_seed_list C)Google custom search API keys
 - configure the seed pages in news_crawl_seedlist.csv
 - get Google customer search API keys by following instructions in https://developers.google.com/custom-search/ 
 - create folder 'crawldb' under 'code' (or the location specified in config file)
 - execute crawler
```sh
    python newscrawl.py
```

#### Create Word2Vec Model
 - create folder 'model' under 'code' for saving the model
 - configure various properties in config.properties
 - start your spark cluster
 - configure the spark-master URL in create-word2vec-model.sh.
 - execute the create-word2vec-model
```sh
    bash create-word2vec-model.sh
```

#### Query Word2Vec Model
 - execute use_word2vec_model.py
 - the test file location can be defined in config.properties
(synonym_test_file). The default value is stest.csv
 - The generated result file will be stored in stestresult.csv by default. It
 can be changed using config.properties
```sh
    bash use_word2vec_model.sh
```

#### Find Relations using  Word2Vec Model
 - execute find_relations.py
 - the test file location can be defined in config.properties
(relations_test_file). The default value is relationstest.csv
 - The generated result file will be stored in relationsresult.csv by default. It
 can be changed using config.properties
```sh
    bash find_relations.sh
```

### Manual cleanup of deployment on cluster
login(ssh) to cluster and run the following

```sh
cd /opt
sudo unlink spark
sudo rm -rf spark-2.1.0-bin-hadoop2.6*
sudo ln -s /opt/spark-1.6.0-bin-hadoop2.6 spark
sudo rm -rf /tmp/word2vec*
sudo rm -rf /opt/word2vec*
```


