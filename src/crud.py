from elasticsearch import Elasticsearch, RequestsHttpConnection
import time
from elasticsearch.exceptions import ConnectionError
from datetime import datetime

class ElasticClass():
    def __init__(self):
        self.es = es = Elasticsearch(host="elastic_container", port= "9200", connection_class=RequestsHttpConnection, max_retries=30,
                       retry_on_timeout=True, request_timeout=30)

    def createindex(self):
        self.es.indices.create(index="industry")

    def indexExists(self):
        self.es.indices.exists(index="industry")
        return 