Python Dependencies
Version supported - Python 2.7.13

	pip install -r requirements.txt


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




