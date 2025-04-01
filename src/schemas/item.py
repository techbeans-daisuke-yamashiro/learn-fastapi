from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
  id: Optional[int]
  name: str
  price: float
  