from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
import time
from elasticsearch.exceptions import ConnectionError
from datetime import datetime
import csv
import json
class ElasticClass():
    def __init__(self):
        self.es = es = Elasticsearch(host="elastic_container", port= "9200", connection_class=RequestsHttpConnection, max_retries=30,
                       retry_on_timeout=True, request_timeout=30)

    def createIndex(self):
        #self.es.indices.create(index="product")
        document = {"type": "prehrana", "bdp": 219919}
        #return self.es.index(index="product")
        return self.es.indices.exists(index="first_index")
    def getIndex(self):
        
        result = self.es.get(index="product", id=1)
        print(result, result["_source"])
        #return self.es.indices.get_alias("*")
    def deleteIndex(self):
        return self.es.indices.delete(index="product")
    
    def bulkInsert(self):
        with open("nike_2020_04_13.csv", "r") as csv_file:
            reader = csv.DictReader(csv_file)
            self.es.indices.create(index="product")
            # checker = self.es.indices.exists(index="first_index")
            # print(checker)
            # if checker == True:
            return helpers.bulk(self.es, reader, index="product")
            # else:
            #     return self.es.indices.create(index="industry")
    def searchData(self, *args):
        
        body = {
            "from":0,
            "size":50,
            "query": {
                "match": {
                    "Product Name":f"{args}"
                    }
            }
        }
        body_query = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "Sale Price": "2495"
                        }
                    }
                }
            }
        }
        filters = {
            "query": {
                "constant_score": { # ubrzaj query, kes  wrpaed
                    "filter": {
                        "term": {
                            "Sale Price": "2495"
                        }
                    }
                }
            }
        }
        query_range = {
            "query": {
                "range": {
                    "Sale Price": {
                        "gte": "2495",
                        "lte": "7495"
                    }
                }

            }
        }
        result = self.es.search(index="product", body=query_range, size=50)
        l = []
        for i in range(len(result["hits"]["hits"])):
            l.append({"Model name": result["hits"]["hits"][i]["_source"]["Product Name"],
                "Model url": result["hits"]["hits"][i]["_source"]["URL"],
                "Model price": result["hits"]["hits"][i]["_source"]["Sale Price"]})
        return l
        # return{
        #     "Model name": result["hits"]["hits"][i]["_source"]["Product Name"],
        #     "Model url": result["hits"]["hits"][i]["_source"]["URL"],
        #     "Model price": result["hits"]["hits"][i]["_source"]["Sale Price"]
        #     }