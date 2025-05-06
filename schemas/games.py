from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GameCreate(BaseModel):
    game_type: str = Field(..., min_length=2, max_length=50)
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    thumbnail_path: Optional[str] = None
    age_limit: Optional[int] = None


class GameUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    thumbnail_path: Optional[str] = None
    age_limit: Optional[int] = None


class GameOut(BaseModel):
    id: int
    game_type: str
    title: str
    description: Optional[str]
    thumbnail_path: Optional[str]
    age_limit: Optional[int]

    class Config:
        from_attributes = True
