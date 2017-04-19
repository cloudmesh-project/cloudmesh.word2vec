from googleapiclient.discovery import build
from goose import Goose
from requests import get
import csv
import myutils
import sys

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../config.properties')

# get config data
data_location = config.get('DataSection', 'data_location')
seed_list_file = config.get('CrawlerSection', 'news_seed_list')
my_api_key = config.get('CrawlerSection', 'google_api_key')
my_cse_id = config.get('CrawlerSection', 'google_cx')

#my_api_key = "AIzaSyAa4M2DRIJpJY8IrSQMmPjPDl2cdnO6Pwk"
#my_cse_id = "005168333629529190436:jscixdribpm"

print(seed_list_file)


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id).execute()
    return res['items']


with open(seed_list_file, 'r') as f:
    reader = csv.reader(f)
    seedlist = list(reader)


    for x in seedlist:
        print(x[0])
        try:
            print("Searching information of: %s" % x[0])
            results = google_search(x[0], my_api_key, my_cse_id, num=50)
            for result in results:
                title = result['title']
                content = result['title'] + "\n" + result['snippet'] + "\n"
                link = result['link']
                try:
                    response = get(link)
                    extractor = Goose()
                    article = extractor.extract(raw_html=response.content)
                    content = content + article.cleaned_text
                except:
                    print("Could not download page: %s" %link)
                myutils.insert_doc(title, content, data_location)
        except:
            print("Didn't get Wiki link")




#results = google_search(
#    'sachin and anjali tendulkar', my_api_key, my_cse_id, num=50)

#for result in results:
#    print(result['title'])
#    print(result['snippet'])
#    print(result['link'])