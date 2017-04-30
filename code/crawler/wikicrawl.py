import os
import wikipedia
import csv
import myutils
import sys
import traceback

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('/opt/word2vec/config.properties')

# get config data
data_location = config.get('DataSection', 'data_location')
seed_list_file = config.get('CrawlerSection', 'seed_list')
debug_flag = sys.argv[2]

if len(sys.argv) > 1:
    max_pages = sys.argv[1]
else:
    max_pages = config.get('CrawlerSection', 'max_pages')

print "max_pages:" + max_pages

with open(seed_list_file, 'r') as f:
    reader = csv.reader(f)
    seedlist = list(reader)

    index = 0

    for x in seedlist:
        if(index > int(max_pages)):
            break
        try:
            w = wikipedia.page(x)
            print("Inserting information of: %s" %w.title)
            myutils.insert_doc(w.title, w.content, data_location)
            index = index + 1
            #add links in the queue
            for link in w.links:
                if link not in seedlist:
                    seedlist.append(link)
        except:
            print(traceback.format_exc())
            print("Didn't get Wiki link")

myutils.concat_files(data_location, "crawler_all_data.txt")

