from pydantic import BaseModel
from typing import Optional

class CreateIndexModel(BaseModel):
    name: str
    id: int
    doc: dict
    alias: str

class DeleteIndexModel(BaseModel):
    name: str

class IndexExistsModel(BaseModel):
    name: str

class GetDocument(BaseModel):
    name: str
    id: int

class UpdateDocument(BaseModel):
    name: str
    id: int
    doc: dict
    
class SearchModels(BaseModel):
    model: Optional[str]