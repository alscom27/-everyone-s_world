from pydantic import BaseModel, Field
from typing import Optional


class GameStageCreate(BaseModel):
    game_id: int
    user_id: int
    stage_number: int = Field(..., ge=1)
    description: Optional[str]
    image_path: Optional[str]
    audio_path: Optional[str]


class GameStageUpdate(BaseModel):
    description: Optional[str]
    image_path: Optional[str]
    audio_path: Optional[str]


class GameStageOut(BaseModel):
    id: int
    game_id: int
    user_id: int
    stage_number: int
    description: Optional[str]
    image_path: Optional[str]
    audio_path: Optional[str]

    class Config:
        from_attributes = True
