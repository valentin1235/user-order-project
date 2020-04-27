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

from .board_service import BoardService
from utils import login_required


class BoardView:
    board_app = Blueprint('board_app', __name__, url_prefix='/board')

    @board_app.route("", methods=["POST"], endpoint='make_board')
    @login_required
    def make_board():
        user_info = g.user_info
        print(user_info)
        board_service = BoardService()
        # result = board_service.make_board(request)
        return jsonify({'message': user_info}), 200



