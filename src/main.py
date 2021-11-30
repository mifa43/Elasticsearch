from fastapi import FastAPI
import logging, uvicorn
from elasticsearch import Elasticsearch, RequestsHttpConnection
import time
from elasticsearch.exceptions import ConnectionError
from datetime import datetime


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()
#es = Elasticsearch(HOST="http://localhost", PORT="9200")
#es = Elasticsearch()
@app.get("/")
async def helth_check():
    es = Elasticsearch(host="elastic_container", port= "9200", connection_class=RequestsHttpConnection, max_retries=30,
                       retry_on_timeout=True, request_timeout=30)
    # es.indices.create(index="kokile")
    # print(es)
    doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
    }
    res = es.index(index="test-index", id=1, document=doc)
    print(res['result'])

    res = es.get(index="test-index", id=1)
    print(res['_source'])

    es.indices.refresh(index="test-index")

    res = es.search(index="test-index", query={"match_all": {}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


    return {"Helth": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, loop="asyncio")