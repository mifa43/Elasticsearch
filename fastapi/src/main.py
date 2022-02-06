from pydoc import doc
from typing import AsyncContextManager
from fastapi import FastAPI, HTTPException
import logging, uvicorn
from crud import ElasticClass
from models import *

# kreiranje logera https://docs.python.org/3/library/logging.html
logger = logging.getLogger(__name__) 
logger.setLevel("DEBUG")

# kreiranje logger consol
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# format
formatter = logging.Formatter('%(levelname)s:     %(name)s.%(funcName)s: %(message)s')

# dodaj format u consol-u
ch.setFormatter(formatter)

# dodaj consol-u logger
logger.addHandler(ch)

app = FastAPI()

@app.get("/")
async def helth_check():
    logger.info("{Health : OK}, 200")

    return {"Health": "OK"}

@app.post("/create-index")
async def create_index(index: CreateIndexModel):
    el = ElasticClass().createIndex(index.indices)
    if el["exists"] == False:
        logger.info("{message : '%s'}, 200"%(el["status"]))
    else:
        logger.exception("index '%s' vec postoji"%(index.indices))
        raise HTTPException(status_code=409, detail="index '{0}' vec postoji".format(index.indices))
    return {"messasge": el["status"]}

# @app.post("/create-index-bulk")
# async def create_index_bulk(model: CreateIndexModel):
#     s = ElasticClass().create_index_bulk(model.indices)
#     print(s["name"])
#     return {"indices": "kreiran"}
    
@app.post("/create-document-bulk")
async def create_document_bulk(model: CreateDocumentBulk):
    add = ElasticClass().create_document_bulk(model.indices, model.document)
    logger.info("{Kreiran novi index: %s}, 200"%model.indices)
    return{"message": "Kreiran novi index"}

@app.post("/create-document-bulk-job")
async def create_document_bulk_job_request(model: CreateDocumentBulkJob):
    job = ElasticClass().create_document_bulk_job(model.indices, model.document)
    logger.info("{Kreiran novi index: %s}, 200"%model.indices)
    return {"message": "Kreiran novi index"}
    
@app.delete("/delete-index")
async def delete_index(index: DeleteIndexModel):
    delete = ElasticClass().deleteIndex(index.name)
    if delete["exists"] == True:
        logger.info("{izbrisan je index: %s}, 200"%index.name)
    else:
        logger.exception("index %s nije pronadjen, 404"%index.name)
        raise HTTPException(status_code=404, detail="index %s nije pronadjen"%index.name)
    return {"message": delete["status"]}

@app.get("/get-indexs")
async def get_indexs():
    index = ElasticClass().getIndexs()
    if index["exists"] == True:
        logger.info("pronadjeni su postojeci index-i, 200")
    else:
        logger.exception("nema postojecih indexa, 404")
        raise HTTPException(status_code=404, detail="nema postojecih indexa")
    return {"message": f"index {index['status']} found"}

@app.post("/get-document")
async def get_document(index: GetDocument):
    document = ElasticClass().getDocument(index.name, index.id)
    if document["exists"] ==  True:
        logger.info("pronadjen je document: %s, 200"%index.name)
        # if not index.id:
        #    pass
    else:
        logger.exception("document/document_id nije pronadjen, 404")
        raise HTTPException(status_code=404, detail="document: %s ili document_id: %s nije pronadjen"%(index.name,index.id))
    return {"message": f"{document['status']}"}

@app.put("/update-document")
async def update_document(document: UpdateDocument):
    update = ElasticClass().updateDocument(document.name, document.id, document.doc)
    if update["exists"] ==  True:
        logger.info("pronadjen je document: %s, 200"%document.name)
        
    else:
        logger.exception("document/document_id nije pronadjen, 404")
        raise HTTPException(status_code=404, detail="document: %s ili document_id: %s nije pronadjen"%(document.name,document.id))
    return {"message": f"{update['status']}"}


@app.post("/bulk")
async def bulk_insert(model: bulk):
    bulk = ElasticClass().bulkInsert(model.indices, model.document)
    print(bulk)
    return {"message": "data inserted"}

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