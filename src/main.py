from fastapi import FastAPI
import logging, uvicorn


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()

@app.get("/")
async def helth_check():
    return {"Helth": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, loop="asyncio")