import os
import wikipedia
import csv
import myutils
import sys

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../config.properties')

# get config data
data_location = config.get('DataSection', 'data_location')
max_pages = config.get('CrawlerSection', 'max_pages')
seed_list_file = config.get('CrawlerSection', 'seed_list')
debug_flag = config.get('Debug', 'debug')


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
            print("Didn't get Wiki link")

