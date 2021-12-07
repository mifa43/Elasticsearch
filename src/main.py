from fastapi import FastAPI
import logging, uvicorn
from crud import ElasticClass
from models import SearchModels

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()

@app.get("/")
async def helth_check():    
    return {"Helth": "OK"}

@app.post("/create-index")
async def create_index():
    el = ElasticClass().createIndex()
    print(el)

    return {"messasge": "index created"}

@app.delete("/delete-index")
async def delete_index():
    delete = ElasticClass().deleteIndex()
    print(delete) 

    return {"message": f"deleted index {delete}"}

@app.get("/get-index")
async def get_index():
    index = ElasticClass().getIndex()
    print(index)
    return {"message": "index found"}

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


if __name__ == "__main__":
    uvicorn.run(app, port=8080, loop="asyncio")