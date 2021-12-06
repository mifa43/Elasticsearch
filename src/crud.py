from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
import time
from elasticsearch.exceptions import ConnectionError
from datetime import datetime
import csv

class ElasticClass():
    def __init__(self):
        self.es = es = Elasticsearch(host="elastic_container", port= "9200", connection_class=RequestsHttpConnection, max_retries=30,
                       retry_on_timeout=True, request_timeout=30)

    def createIndex(self):
        #self.es.indices.create(index="industry")
        document = {"type": "prehrana", "bdp": 219919}
        #return self.es.index(index="industry")
        return self.es.indices.exists(index="first_index")
    def getIndex(self):
        
        result = self.es.get(index="industry", id=1)
        print(result, result["_source"])
        #return self.es.indices.get_alias("*")
    def deleteIndex(self):
        return self.es.indices.delete(index="industry")
    
    def bulkInsert(self):
        with open("annual-enterprise-survey-2020-financial-year-provisional-csv.csv", "r") as csv_file:
            reader = csv.DictReader(csv_file)
            self.es.indices.create(index="industry")
            # checker = self.es.indices.exists(index="first_index")
            # print(checker)
            # if checker == True:
            return helpers.bulk(self.es, reader, index="industry")
            # else:
            #     return self.es.indices.create(index="industry")
    def searchData(self):
        body = {
                "from":0,
                "size":1000,
                "query": {
                    "match": {
                        "Value":"1"
                    }
                }
            }


        return self.es.search(index="industry", body=body, size=1000)