from pydantic import BaseModel
from uuid import UUID


class ScheduleBase(BaseModel):
    term_id: UUID
    department_id: UUID


