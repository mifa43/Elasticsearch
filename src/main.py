from fastapi import FastAPI
import logging, uvicorn
from crud import ElasticClass


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()

@app.get("/")
async def helth_check():
    el = ElasticClass().createindex()
    print(el)
    index = ElasticClass().indexExists()
    print(index)
    return {"Helth": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, loop="asyncio")