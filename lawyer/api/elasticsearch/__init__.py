from elasticsearch import Elasticsearch
from datetime import datetime
import json


def print_json(obj, debug=True):
    str = json.dumps(obj, sort_keys=True, indent=4, separators=(', ', ': '))
    if debug:
        print(str)
    return str


es_host = "http://192.168.42.131:9200"
es = Elasticsearch(hosts=es_host)
print_json(es.info())
print_json(es.indices.create(index='my-index', ignore=400))
print(es.index(index="my-index", doc_type="test-type", id=124, body={"any": "data124", "timestamp": datetime.now()}))
print(es.get(index="my-index", doc_type="test-type", id=124)['_source'])


class ElasticsearchManager(object):
    def __init__(self):
        self.es = es


manager = ElasticsearchManager()

print(id(manager.es))
manager2 = ElasticsearchManager()
print(id(manager2.es))
