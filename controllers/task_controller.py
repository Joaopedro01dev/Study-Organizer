from factory import db, api
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from spectree import Response
from models.study_task import StudyTask, TaskResponse, TaskResponseList, TaskCreate, TaskSearchModel, TaskUpdate
from models.subject import Subject
from models.user import User
from utils.response_schema import GenericResponse
from sqlalchemy import select
from datetime import datetime, timezone

task_controller = Blueprint("task_controller", __name__, url_prefix="/tasks")

@task_controller.get("/")
@api.validate(query=TaskSearchModel, resp=Response(HTTP_200=TaskResponseList), tags=["tasks"])
@jwt_required()
def get_tasks(query: TaskSearchModel):
    """
    Get all tasks
    """

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    stmt = select(StudyTask).join(Subject).filter(Subject.user_id == user.id).order_by(StudyTask.due_date.asc())

    if query.subject_id is not None:
        stmt = stmt.filter(StudyTask.subject_id == query.subject_id)

    if query.completed is not None:
        stmt = stmt.filter(StudyTask.completed == query.completed)


    tasks_list = db.session.scalars(stmt).all()

    response = TaskResponseList(tasks=[TaskResponse.model_validate(task) for task in tasks_list]).to_response_dict()
    return response, 200

@task_controller.post("/")
@api.validate(json=TaskCreate, resp=Response(HTTP_201=GenericResponse, HTTP_404=GenericResponse), tags=["tasks"])
@jwt_required()
def post_task():
    """
    Create a task
    """

    data = request.context.json.model_dump(exclude_none=True)

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    subject = db.session.get(Subject, data["subject_id"])

    if not subject or subject.user_id != user.id:
        response = GenericResponse(msg="Materia nao encontrada ou usuario negado")
        return response, 404
    
    new_task = StudyTask(**data)

    db.session.add(new_task)
    db.session.commit()

    response = GenericResponse(msg="Tarefa criada com sucesso")
    return response, 201

@task_controller.get("/<int:task_id>")
@api.validate(resp=Response(HTTP_200=TaskResponse, HTTP_404=GenericResponse), tags=["tasks"])
@jwt_required()
def get_task(task_id):
    """
    Get task by id
    """

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    stmt = select(StudyTask).join(Subject).filter(StudyTask.id == task_id, Subject.user_id == user.id)

    task = db.session.scalars(stmt).first()

    if not task:
        response = GenericResponse(msg="Tarefa nao encontrada")
        return response, 404

    return TaskResponse.model_validate(task).to_response_dict(), 200


@task_controller.put("/<int:task_id>")
@api.validate(json=TaskUpdate, resp=Response(HTTP_200=GenericResponse, HTTP_404=GenericResponse), tags=["tasks"])
@jwt_required()
def put_task(task_id):
    """
    Update a task by id
    """

    data = request.context.json.model_dump(exclude_unset=True, mode="python")

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    stmt = select(StudyTask).join(Subject).filter(StudyTask.id == task_id, Subject.user_id == user.id)
    task = db.session.scalars(stmt).first()

    if not task:
        response = GenericResponse(msg="Tarefa nao encontrada ou acesso negado")
        return response, 404
    
    if "completed" in data:
        task.completed_at = datetime.utcnow() if data["completed"] else None

    for key, value in data.items():
        setattr(task, key, value)

    db.session.commit()

    response = GenericResponse(msg="Tarefa atualizada com sucesso")
    return response, 200

@task_controller.delete("/<int:task_id>")
@api.validate(resp=Response(HTTP_200=GenericResponse, HTTP_404=GenericResponse), tags=["tasks"])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task by id
    """

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    stmt = select(StudyTask).join(Subject).filter(StudyTask.id == task_id, Subject.user_id == user.id)
    task = db.session.scalars(stmt).first()

    if not task:
        response = GenericResponse(msg="Tarefa nao encontrada ou acesso negado")
        return response, 404
    
    db.session.delete(task)
    db.session.commit()

    response = GenericResponse(msg="Tarefa deletada com sucesso")
    return response, 200