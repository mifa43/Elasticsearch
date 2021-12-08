from pydantic import BaseModel
from typing import Optional

class SearchModels(BaseModel):
    model: Optional[str]