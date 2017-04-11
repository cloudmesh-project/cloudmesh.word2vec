(1) Pre-requisites

(1.a) You have cluster already deployed. To deploy a 3 node chameleon cluster, use the
following:

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

(1.b) Python Dependencies
Version supported - Python 2.7.13

	pip install -r requirements.txt

(2) update ansible-word2vec/hosts file with ip of you cluster VM. Note that on
the cluster first node becomes master

(3) execute

    ansible-word2vec/install.sh

This should deploy code and run the crawler for collecting the training set


Appendix:

Steps for running the crawler and spark job

Setup Crawler
1. Configure various properties in config.properties. For crawler, the
important parameters are A)data_location B)seed_list C)max_pages
2. configure the seed pages in wiki_crawl_seedlist.csv
3. create folder 'crawldb' under 'code'
4. execute crawler
	
	python wikicrawl.py

Create Word2Vec Model
1. create folder 'model' under 'code' for saving the model
2. Configure various properties in config.properties
3. start your spark cluster
3. configure the spark-master URL in create-word2vec-model.sh.
4. execute the create-word2vec-model

	bash create-word2vec-model.sh


Query Word2Vec Model
1. execute use_word2vec_model.py
2. The test file location can be defined in config.properties
(synonym_test_file). The default value is stest.csv
3. The generated result file will be stored in stestresult.csv by default. It
 can be changed using config.properties

	spark-submit use_word2vec_model.py




