from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GameProgressCreate(BaseModel):
    user_id: int = Field(..., description="사용자 PK")
    game_type: str = Field(..., description="게임 종류")
    current_stage: int = Field(default=1, description="진행도")
    game_state_json: Optional[str] = Field(None, description="게임 상태 json")
    image_path: Optional[str] = Field(None, description="게임에서 사용된 이미지 경로")
    audio_path: Optional[str] = Field(None, description="게임에서 사용된 음성파일 경로")


class GameProgressUpdate(BaseModel):
    current_stage: Optional[int] = None
    game_state_json: Optional[str] = None
    image_path: Optional[str] = None
    audio_path: Optional[str] = None


class GameProgressOut(BaseModel):
    id: int
    user_id: int
    game_type: str
    current_stage: int
    last_played_at: datetime
    game_state_json: Optional[str]
    image_path: Optional[str]
    audio_path: Optional[str]

    class Config:
        from_attributes = True
