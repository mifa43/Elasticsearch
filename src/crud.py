from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
import time
from elasticsearch.exceptions import ConnectionError
from datetime import datetime
import csv
import json
import pyarrow.parquet as parquet
import pandas
import pyarrow as pa
class ElasticClass():
    def __init__(self):
        self.es = es = Elasticsearch(host="elastic_container", port= "9200", connection_class=RequestsHttpConnection, max_retries=30,
                       retry_on_timeout=True, request_timeout=30)

    def createIndex(self, name: str, id:int, doc:dict, alias: str) -> str:
        """
        :name predstavlja index name
        :id document_id
        :doc dokumenti u index-u
        :alias index

        - Za id moze da se koristi uuid ali nije obavezno jer elastic takodje i sam definise id
        """
        mapping = {
                "mappings": {
                    "properties": {
                        
                        "ime":{
                            "type": "text"
                        },
                        "prezime": {
                            "type": "text"
                        },
                        "plata": {
                            "type": "integer"
                        }
                    }
                }
            }
        response = self.es.index(index=name, id=id, body=doc)
        alias = self.es.indices.put_alias(index=name, name=alias)
        return {"status": f"index {name} kreiran"}
    def deleteIndex(self, name: str) -> str:
        """
        :name index_name

        - Brisanje index-a uzima parametar name sto predstavlja index_name
        """
        self.es.indices.delete(index=name)
        return {"status": f"index {name} je izbrisan"}
    def getIndexs(self) -> str:
        """
        - Vraca listu svih index-a
        """
        index = self.es.indices.get_alias("*")
        return {"status": index} # lista svih index-a
    def indexCheck(self, name) -> str:
        """
        :name index_name

        - Za parametar uzima index_name i vraca True ako postoji 
        """
        exists = self.es.indices.exists(index=name)
        return {"status": f"{name}: {exists}"}
    def getDocument(self, name: str, id: int) -> str:
        """
        :name index_name
        :id index_id

        - Uzimanje vrednosti iz index-a
        """
        response = self.es.get(index=name, id=id)

        return {"status": response["_source"]}
    def updateDocument(self, name:str, id: int, doc: dict) -> str:
        """
        :name predstavlja index name
        :id index_id
        :doc dokumenti u index-u

        - Param doc predstavlja dokumente i koristimo dict za update row/coll
        - *U body se salje dict {doc: param}
        """
        update = self.es.update(index=name, id=id, body={"doc": doc})
        return {"status": f"updejtovan je index:{name}, {doc}"}
    def bulkInsert(self) -> str:
        """
        - Otvaranje i citanje csv fajla upisivanje u elastik uz bulk
        """
        with open("nike_2020_04_13.csv", "r") as csv_file:
            reader = csv.DictReader(csv_file)
            mapping = {
                "mappings": {
                    "properties": {
                        
                        "URL":{
                            "type": "text"
                        },
                        "Product Name": {
                            "type": "text"
                        },
                        "Product ID": {
                            "type": "text"
                        },
                        "Listing Price": {
                            "type": "text"
                        },
                        "Sale Price": {
                            "type": "integer",
                        },
                        "Discount": {
                            "type": "text"
                        },
                        "Brand": {
                            "type": "text"
                        },
                        "Description": {
                            "type": "text"
                        },
                        "Rating": {
                            "type": "text"
                        },
                        "Reviews": {
                            "type": "text"
                        },
                        "Images": {
                            "type": "text"
                        },
                    }
                }
            }
            self.es.indices.create(index="product", body=mapping)
            checker = self.es.indices.exists(index="product")
            print(checker)
            
            return helpers.bulk(self.es, reader, index="product")
    def bulkUpdate(self) -> str:
        doc = {"doc": {"date": "1/1/2017"}}
        return helpers.bulk(self.es, dict(doc), index="product")


    def searchData(self, *args: str) -> str:
        """
        :args param
        :body_query (range)
            - pretraga po imenu produkta
            - filtriranje po visini cene 
            - parametri za polja <filedName> 
            
                - gt - vece od
                - gte - veci ili jednak
                - lt - manji od
                - lte - manje ili jednako
                - format - (optciono: str) :format datuma zamenjuje format u maperu 
        - pretrazivanje podataka
        # *parametri za polja nisu obavezna
        """
        # ovaj query se koristi samo kada zelimo sortirati vrednosti :asc od manjeg ka vecem, :des od veceg ka manjem 
        ## sort="_score,Sale Price:asc"
        match_all = {
            "from":0,
            "size":50,
            "query": {
                "match_all": {}
            }
        }

        # pretraga po imenu produkta
        body = {
            "from":0,
            "size":50,
            "query": {
                "match": {
                    "ime":f"{args}"
                    }
            }
        }
    
        body_query = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "Product Name":f"{args}"
                        },
                    },
                    "filter":{
                        "range":{"Sale Price": {
                            "gte": "111",
                            "lte": "9990"
                            }
                        }
                    }
                }
            }
        }
        #query filter
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
        
        result = self.es.search(index="product", body=match_all, size=999, sort="_score,Sale Price:asc")
        
        l = []
        print(result)
        for i in range(len(result["hits"]["hits"])):
        #     l.append({"ime": result["hits"]["hits"][i]["_source"]["ime"],
        #         "prezime": result["hits"]["hits"][i]["_source"]["prezime"],
        #         "plata": result["hits"]["hits"][i]["_source"]["plata"]})
        # return l


            l.append({"Model name": result["hits"]["hits"][i]["_source"]["Product Name"],
                    "Model url": result["hits"]["hits"][i]["_source"]["URL"],
                    "Model price": result["hits"]["hits"][i]["_source"]["Sale Price"]})
            return l
    def create_parquet(self):
        """
        - Kreiranje parquet tabele
        """
        # kreiranje data frejma 
        ## ime - row
        ## milos - column
        ## 123 - index 
        df = pandas.DataFrame({
            "ime": ["Milos", "Nikola", "Jovan"],
            "prezime": ["Zlatkovic", "Djokic", "Kokic"],
            "godine": [21, 44, 38]
        }, index = list('123'))
        # pyarrow kreira tabelu i iz pandasa kao argument uzima df(dataFrame)
        table = pa.Table.from_pandas(df)
        #kreiranje tabele i imenovanje
        parquet.write_table(table, "exemple.parquet")
        # citanje tabele
        table2 = parquet.read_table("exemple.parquet")
        # tabelu saljemo u pandas
        table2.to_pandas()
        # citamo tabelu, column kolone koje prikazujemo
        table3 = parquet.read_pandas("exemple.parquet", columns=["ime", "prezime", "godine"]).to_pandas()
        print(table3)
        return {"table": table}
    def write_parquet_to_elastic(self):
        table = self.create_parquet()
        s = table["table"]["ime"]
        for i in range(len(s)):
            # print(table["table"]["ime"][i], table["table"]["prezime"][i], table["table"]["godine"][i])
            # print("ASD".lower())
            l = []
            l.append(str(table["table"]["ime"][i]))
            
            dic = {"ime": str(table["table"]["ime"][i]),"prezime": str(table["table"]["prezime"][i]),"godine": str(table["table"]["godine"][i])}
            self.createIndex(f"{l[0]}".lower(),s, dic, "zaposleni-".join(l))
            