from factory import db, api
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from spectree import Response
from models.subject import Subject, SubjectResponseList, SubjectResponse, SubjectCreate, SubjectUpdate
from models.user import User
from utils.response_schema import GenericResponse
from sqlalchemy import select

subject_controller = Blueprint("subject_controller", __name__, url_prefix="/subjects")

@subject_controller.get("/")
@api.validate(resp=Response(HTTP_200=SubjectResponseList, HTTP_404=GenericResponse), tags=["subjects"])
@jwt_required()
def get_subjects():
    """
    Get all subjects
    """

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    stmt = select(Subject).filter_by(user_id=user.id)
    subjects_list = db.session.scalars(stmt).all()

    response = SubjectResponseList(subjects=[SubjectResponse.model_validate(sub) for sub in subjects_list]).to_response_dict()

    return response, 200

@subject_controller.post("/")
@api.validate(json=SubjectCreate, resp=Response(HTTP_201=GenericResponse), tags=["subjects"])
@jwt_required()
def post_subject():
    """
    Create a subject
    """

    data = request.context.json.model_dump(exclude_none=True)

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    new_subject = Subject(**data, user_id=user.id)

    db.session.add(new_subject)
    db.session.commit()

    response = GenericResponse(msg="Materia criada com sucesso!")
    return response, 201

@subject_controller.get("/<int:subject_id>")
@api.validate(resp=Response(HTTP_200=SubjectResponse, HTTP_404=GenericResponse), tags=["subjects"])
@jwt_required()
def get_subject(subject_id):
    """
    Get a subject by id
    """

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    subject = db.session.get(Subject, subject_id)

    if not subject or subject.user_id != user.id:
        response = GenericResponse(msg="Materia nao encontrada")
        return response, 404

    response = SubjectResponse.model_validate(subject).to_response_dict()
    return response, 200

@subject_controller.put("/<int:subject_id>")
@api.validate(json=SubjectUpdate, resp=Response(HTTP_200=GenericResponse, HTTP_404=GenericResponse, HTTP_403=GenericResponse), tags=["subjects"])
@jwt_required()
def put_subject(subject_id):
    """
    Updata a subject
    """

    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    subject = db.session.get(Subject, subject_id)

    if subject is None:
        response = GenericResponse(msg=f"Materia com id {subject_id} nao foi encontrada")
        return response, 404
    
    if subject.user_id != user.id:
        response = GenericResponse(msg="Só é possivel atualizar as proprias máterias")
        return response, 403
    
    data = request.context.json.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(subject, key, value)

    db.session.commit()
    response = GenericResponse(msg="Materia atualizada com sucesso")
    return response, 200


@subject_controller.delete("/<int:subject_id>")
@api.validate(resp=Response(HTTP_200=GenericResponse, HTTP_404=GenericResponse, HTTP_403=GenericResponse), tags=["subjects"])
@jwt_required()
def delete_subject(subject_id):
    """
    Delete a subject by id
    """

    subject = db.session.get(Subject, subject_id)

    if subject is None:
        response = GenericResponse(msg=f"Nao encontramos a materia com id {subject_id}")
        return response, 404
    
    current_user_identify = get_jwt_identity()
    user = db.session.scalars(select(User).filter_by(email=current_user_identify)).first()

    if subject.user_id != user.id:
        response = GenericResponse(msg="Só é possivel deletar suas proprias materias")
        return response, 403
    
    db.session.delete(subject)
    db.session.commit()

    response = GenericResponse(msg="Materia deletada com sucesso")
    return response, 200