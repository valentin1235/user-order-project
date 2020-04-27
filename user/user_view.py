import json
from datetime import datetime

from flask import request, Blueprint, jsonify, g
from flask_request_validator import (
    GET,
    PATH,
    FORM,
    Param,
    Pattern,
    MaxLength,
    validate_params
)

from .user_service import UserService
from utils import login_required


class UserView:
    user_app = Blueprint('user_app', __name__, url_prefix='/user')

    @user_app.route("", methods=["POST"], endpoint='sign_up')
    def sign_up():
        user_service = UserService()
        result = user_service.sigh_up(request)
        return result



