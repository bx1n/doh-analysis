import json
from pprint import pprint

def get_top_urls(x,y):

    with open("alexadomain.json") as jsf:
        data = json.load(jsf)

    urls = []
    
    # starting from index 0 
    for i in range(x-1,y):
        urls.append("http://www."+data[i]["DataUrl"])
    return urls


