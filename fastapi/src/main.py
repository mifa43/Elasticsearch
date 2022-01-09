from os import PRIO_PGRP
from typing import AsyncContextManager
from fastapi import FastAPI
import logging, uvicorn
from crud import ElasticClass
from models import *

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()

@app.get("/")
async def helth_check():
    return {"Helth": "OK"}

@app.post("/create-index")
async def create_index(index: CreateIndexModel):
    el = ElasticClass().createIndex(index.indices) #index.id, index.doc, index.alias
    print(el)

    return {"messasge": el["status"]}

@app.post("/create-index-bulk")
async def create_index_bulk(model: CreateIndexModel):
    s = ElasticClass().create_index_bulk(model.indices)
    print(s["name"])
    return {"indices": "kreiran"}
    
@app.post("/create-document-bulk")
async def create_document_bulk(model: CreateDocumentBulk):
    add = ElasticClass().create_document_bulk(model.indices, model.document)
    print(add)
    return{"message":"dodat novi document"}
@app.post("/create-document-bulk-job")
async def create_document_bulk_job_request(model: CreateDocumentBulkJob):
    job = ElasticClass().create_document_bulk_job(model.indices, model.document)
    return {"message": "novi dokument je dodan"}
    
@app.delete("/delete-index")
async def delete_index(index: DeleteIndexModel):
    delete = ElasticClass().deleteIndex(index.name)
    print(delete) 

    return {"message": delete["status"]}
@app.get("/get-indexs")
async def get_indexs():
    index = ElasticClass().getIndexs()
    print(index)
    return {"message": f"index {index['status']} found"}

@app.post("/get-index-exists")
async def index_exits_check(index: IndexExistsModel):
    exists = ElasticClass().indexCheck(index.name)
    print(exists)
    return {"message": exists["status"]}

@app.post("/get-document")
async def get_document(index: GetDocument):
    document = ElasticClass().getDocument(index.name, index.id)
    print(document)
    return {"message": f"{document['status']}"}

@app.put("/update-document")
async def update_document(document: UpdateDocument):
    update = ElasticClass().updateDocument(document.name, document.id, document.doc)
    print(update)
    return {"message": f"{update['status']}"}


@app.post("/bulk")
async def bulk_insert():
    bulk = ElasticClass().bulkInsert()
    print(bulk)
    return {"message": "data inserted"}

@app.post("/bulk-update")
async def bulk_update():
    update = ElasticClass().bulkUpdate()
    return {"message": update}

@app.post("/search")
async def search(dataModel: SearchModels):
    search_data = ElasticClass().searchData(dataModel.model)
    print(search_data)
    return search_data

@app.get("/create-parquet")
async def parquet():
    parquet_read = ElasticClass().create_parquet()

    print(parquet_read)
    return{"message": "parquet file is created"}

@app.get("/write-parquet-to-elastic")
async def parquet_to_elastic():
    data = ElasticClass().write_parquet_to_elastic()
    print(data)

    return{"message": "file is writen"}


if __name__ == "__main__":
    uvicorn.run(app, port=8080, loop="asyncio")