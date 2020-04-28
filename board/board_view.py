import json
from datetime import datetime
from flask import request, Blueprint, jsonify, g
from flask_request_validator import (
    GET,
    PATH,
    FORM,
    JSON,
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
    @validate_params(
        Param('name', JSON, str,
              rules=[MaxLength(20)])
    )
    def make_board(*args):
        user_info = g.user_info
        if user_info.get('auth_type_id') != 1:
            return jsonify({'message': 'UNAUTHORIZED_ACTION'}), 400

        board_info = {
            'uploader': user_info['user_id'],
            'name': args[0]
        }
        board_service = BoardService()
        result = board_service.make_board(board_info)
        return result

    @board_app.route("", methods=["GET"], endpoint='get_board_list')
    @login_required
    def get_board_list():
        board_service = BoardService()
        result = board_service.get_board_list()
        return result

    @board_app.route("/<int:board_id>", methods=["PUT"], endpoint='edit_board')
    @login_required
    @validate_params(
        Param('board_id', PATH, int),
        Param('name', JSON, str,
              rules=[MaxLength(20)])
    )
    def edit_board(*args):
        user_info = g.user_info
        if user_info.get('auth_type_id') != 1:
            return jsonify({'message': 'UNAUTHORIZED_ACTION'}), 400

        board_info = {
            'modifier': user_info['user_id'],
            'board_id': args[0],
            'new_name': args[1]
        }
        board_service = BoardService()
        result = board_service.edit_board(board_info)
        return result

    @board_app.route("/<int:board_id>", methods=["DELETE"], endpoint='delete_board')
    @login_required
    @validate_params(
        Param('board_id', PATH, int),
        Param('is_deleted', JSON, int)
    )
    def delete_board(*args):
        user_info = g.user_info
        if user_info.get('auth_type_id') != 1:
            return jsonify({'message': 'UNAUTHORIZED_ACTION'}), 400

        board_info = {
            'modifier': user_info['user_id'],
            'board_id': args[0],
        }
        if args[1] == 1:
            board_info['is_deleted'] = True
        else:
            return jsonify({'message': 'INVALID_ACTION'}), 400

        board_service = BoardService()
        result = board_service.delete_board(board_info)
        return result

    @board_app.route("/<int:board_id>", methods=["POST"], endpoint='make_article')
    @login_required
    @validate_params(
        Param('board_id', PATH, int),
        Param('title', JSON, str,
              rules=[MaxLength(200)]),
        Param('content', JSON, str,
              rules=[MaxLength(10000)])
    )
    def make_article(*args):
        user_info = g.user_info

        article_info = {
            'board_id': args[0],
            'uploader': user_info['user_id'],
            'title': args[1],
            'content': args[2]
        }
        board_service = BoardService()
        result = board_service.make_article(article_info)
        return result

    @board_app.route("/<int:board_id>", methods=["GET"], endpoint='get_article_list')
    @login_required
    @validate_params(
        Param('board_id', PATH, int)
    )
    def get_article_list(*args):
        board_id = args[0]
        board_service = BoardService()
        result = board_service.get_article_list(board_id)
        return result

    @board_app.route("/<int:board_id>/<int:article_id>", methods=["GET"], endpoint='get_article_detail')
    @login_required
    @validate_params(
        Param('board_id', PATH, int),
        Param('article_id', PATH, int)
    )
    def get_article_detail(*args):
        article_info = {
            'board_id': args[0],
            'article_id': args[1]
        }
        board_service = BoardService()
        result = board_service.get_article_detail(article_info)
        return result

    @board_app.route("/<int:board_id>/<int:article_id>", methods=["PUT"], endpoint='edit_article')
    @login_required
    @validate_params(
        Param('board_id', PATH, int),
        Param('article_id', PATH, int),
        Param('title', JSON, str,
              rules=[MaxLength(200)]),
        Param('content', JSON, str,
              rules=[MaxLength(10000)])
    )
    def edit_article(*args):
        user_info = g.user_info
        article_info = {
            'board_id': args[0],
            'article_id': args[1],
            'new_title': args[2],
            'new_content': args[3],
            'modifier': user_info['user_id'],
            'auth_type_id': user_info['auth_type_id']
        }
        board_service = BoardService()
        result = board_service.edit_article(article_info)

        return result

    @board_app.route("/<int:board_id>/<int:article_id>", methods=["DELETE"], endpoint='delete_article')
    @login_required
    @validate_params(
        Param('board_id', PATH, int),
        Param('article_id', PATH, int),
        Param('is_deleted', JSON, int)
    )
    def delete_article(*args):
        user_info = g.user_info
        article_info = {
            'board_id': args[0],
            'article_id': args[1],
            'modifier': user_info['user_id'],
            'auth_type_id': user_info['auth_type_id']
        }
        if args[2] == 1:
            article_info['is_deleted'] = True
        else:
            return jsonify({'message': 'INVALID_ACTION'}), 400

        board_service = BoardService()
        result = board_service.delete_article(article_info)

        return result
