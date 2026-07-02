from factory import db
from utils.response_schema import OrmBase
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class Subject(db.Model):
    __tablename__ = "subject"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    tasks = db.relationship("StudyTask", back_populates="subject", lazy="dynamic", cascade="all, delete-orphan")

    @property
    def total_tasks(self):
        return self.tasks.count()
    
    @property
    def completed_tasks(self):
        return self.tasks.filter_by(completed=True).count()
    
    @property
    def progress_percentage(self):
        total = self.total_tasks

        if total == 0:
            return 0.0
        
        return round((self.completed_tasks / total) * 100, 2)
    
    @property
    def next_due_date(self):
        from models import StudyTask

        next_task = self.tasks.filter_by(completed=False).order_by(StudyTask.due_date.asc()).first()

        return next_task.due_date if next_task else None
    

# O que a gente envia DA API
class SubjectResponse(OrmBase):
    name: str
    description: Optional[str] = None

    total_tasks: int
    completed_tasks: int
    progress_percentage: float
    next_due_date: Optional[datetime] = None

class SubjectResponseList(BaseModel):
    subjects: list[SubjectResponse]

# O que a gente quer que a API RECEBA
class SubjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None