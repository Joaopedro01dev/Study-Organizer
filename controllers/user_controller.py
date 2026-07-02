from factory import api
from flask import Blueprint
from models.user import UserResponse
from utils.response_schema import GenericResponse
from spectree import Response
from flask_jwt_extended import jwt_required, current_user

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.get("/me")
@api.validate(resp=Response(HTTP_200=UserResponse, HTTP_404=GenericResponse), tags=["users"])
@jwt_required()
def get_user():
    """
    Get logged user
    """

    response = UserResponse.model_validate(current_user).to_response_dict()

    return response, 200
