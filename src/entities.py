from typing import Literal, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field

LANGUAGE_ISO = Literal['ar', 'en', 'fr', 'es', 'ru', 'zh']
LANGUAGE_NAME = Literal['Arabic', 'English', 'French', 'Spanish', 'Russian', 'Chinese']


class SessionConfig(BaseModel):
    task_idx: int = 0
    task_ids: list[Union[str, None]]  # track doc ids user has seen in this session
    user_id: str
    language: LANGUAGE_ISO

    def get_task_id(self) -> Union[str, None]:
        task_id = self.task_ids[self.task_idx]
        return task_id

    def set_task_id(self, task_id: str):
        self.task_ids[self.task_idx] = task_id
        return self


class Annotation(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    labels: list[int]
    comment: Optional[str]


class SustainableDevelopmentGoal(BaseModel):
    id: int
    name: str
    colour: str
    targets: list[str]
    indicators: list[str]


class User(BaseModel):
    id: str = Field(alias='_id')
    access_code: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    leaderboard: bool = Field(default=False, description='If False, name and team will be hidden on the leaderboard.')
    name: str = ''
    organisation: str
    team: str = ''
