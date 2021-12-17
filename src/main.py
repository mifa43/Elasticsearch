from os import PRIO_PGRP
from fastapi import FastAPI
import logging, uvicorn
from crud import ElasticClass
from models import CreateIndexModel, DeleteIndexModel, GetDocument, IndexExistsModel, SearchModels, UpdateDocument

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()

@app.get("/")
async def helth_check():    
    return {"Helth": "OK"}

@app.post("/create-index")
async def create_index(index: CreateIndexModel):
    el = ElasticClass().createIndex(index.name, index.id, index.doc, index.alias)
    print(el)

    return {"messasge": el["status"]}

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

@app.post("/search")
async def search(dataModel: SearchModels):
    search_data = ElasticClass().searchData(dataModel.model)
    print(search_data)
    return search_data

@app.post("/update-document")
async def updateDocument():
    update = ElasticClass().updateDoc()
    print(update)
    return {"message": f"Document updated {update}"}


if __name__ == "__main__":
    uvicorn.run(app, port=8080, loop="asyncio")