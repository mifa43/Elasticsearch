from pydantic import BaseModel
from typing import List, Optional

class CreateIndexModel(BaseModel):
    indices: str
  
class CreateDocumentBulk(BaseModel):
    indices: str
    document: list

class CreateDocumentBulkJob(BaseModel):
    indices: str
    document: list

class DeleteIndexModel(BaseModel):
    name: str

class IndexExistsModel(BaseModel):
    name: str

class GetDocument(BaseModel):
    name: str
    id: str

class UpdateDocument(BaseModel):
    name: str
    id: int
    doc: dict
    
class SearchModels(BaseModel):
    model: Optional[str]

class bulk(BaseModel):
    indices: str
    document: list