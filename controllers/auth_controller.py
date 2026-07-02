from factory import api, db
from sqlalchemy import select
from pydantic import BaseModel
from spectree import Response

from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from models import User
from utils.response_schema import GenericResponse

auth_controller = Blueprint("auth_controller", __name__, url_prefix="/auth")

# O que a gente precisa rceber
class LoginMessage(BaseModel):
    email: str
    password: str

# O que a gente devolve
class LoginResponseMessage(BaseModel):
    access_token: str


@auth_controller.post("/login")
@api.validate(json=LoginMessage, resp=Response(HTTP_200=LoginResponseMessage, HTTP_401=GenericResponse), tags=["auth"], security={})
def login():
    """
    Login in the system
    """

    data = request.json

    user = db.session.scalars(select(User).filter_by(email=data["email"])).first()

    if user and user.verify_password(data["password"]):
        return {"access_token": create_access_token(identity=user.email, expires_delta=None)}

    return {"msg": "Email and password do not match."}, 401
