from typing import Literal, Optional, Union
from pydantic import BaseModel, constr

EMAIL = constr(regex=r'.*@undp.org$', to_lower=True)


class Config(BaseModel):
    task_idx: int = 0
    task_ids: list[Union[str, None]]  # track doc ids user has seen in this session
    session_email: EMAIL
    session_language: Literal['ar', 'en', 'fr', 'es', 'ru', 'zh']

    def get_task_id(self) -> Union[str, None]:
        task_id = self.task_ids[self.task_idx]
        return task_id

    def set_task_id(self, task_id: str):
        self.task_ids[self.task_idx] = task_id
        return self


class Annotation(BaseModel):
    email: EMAIL
    labels: list[int]
    comment: Optional[str]
