from factory import db
from pydantic import BaseModel
from utils.response_schema import OrmBase
from typing import Optional
from datetime import datetime

class StudyTask(db.Model):
    __tablename__ = "study_task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)

    subject = db.relationship("Subject", back_populates="tasks")

class TaskResponse(OrmBase):
    title: str
    description: Optional[str] = None
    due_date: datetime
    completed: Optional[bool]
    completed_at: Optional[datetime] = None
    subject_id: int

class TaskResponseList(OrmBase):
    tasks: list[TaskResponse]

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    subject_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None

class TaskSearchModel(BaseModel):
    subject_id: Optional[int] = None
    completed: Optional[bool] = None