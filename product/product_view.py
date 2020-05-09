from flask import Blueprint, jsonify, g
from flask_request_validator import (
    GET,
    PATH,
    JSON,
    Param,
    Pattern,
    MinLength,
    MaxLength,
    validate_params
)

from .product_service import ProductService
from connection import get_db_connection
from utils import login_required


class ProductView:
    product_app = Blueprint('product_app', __name__, url_prefix='/product')

    @product_app.route('', methods=['GET'], endpoint='get_product_list')
    @validate_params(
        Param('id', GET, int, required=False),
        Param('name', GET, str, required=False),
        Param('offset', GET, int, required=False),
        Param('limit', GET, int, required=False)
    )
    def get_product_list(*args):
        product_keyword_search = {
            'id': args[0],
            'name': args[1],
            'offset': args[2] if args[2] else 0,
            'limit': args[3] if args[3] else 10
        }

        if product_keyword_search['limit'] > 5000:
            return jsonify({'message': 'INVALID_REQUEST'}), 400

        try:
            db_connection = get_db_connection()
            if db_connection:
                product_service = ProductService()
                product_list = product_service.get_product_list(product_keyword_search, db_connection)
                return product_list
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/<int:product_id>', methods=['GET'], endpoint='get_product_detail')
    @validate_params(
        Param('product_id', PATH, int)
    )
    def get_product_detail(*args):
        product_id = {
            'product_id': args[0]
        }
        print(product_id)

        # 데이터베이스 연결
        try:
            db_connection = get_db_connection()
            if db_connection:
                product_service = ProductService()
                product_detail = product_service.get_product_detail(product_id, db_connection)
                return product_detail
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/<int:product_id>/cart', methods=['POST'], endpoint='add_to_cart')
    @login_required
    @validate_params(
        Param('product_id', PATH, int)
    )
    def add_to_cart(*args):
        user = g.account_info
        cart_info = {
            'user_account_id': user.get('user_account_id', None),
            'product_id': args[0]
        }

        try:
            db_connection = get_db_connection()
            if db_connection:
                product_service = ProductService()
                add_to_cart_result = product_service.add_to_cart(cart_info, db_connection)
                return add_to_cart_result
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/<int:product_id>/cart', methods=['DELETE'], endpoint='delete_from_cart')
    @login_required
    @validate_params(
        Param('product_id', PATH, int)
    )
    def delete_from_cart(*args):
        user = g.account_info
        cart_info = {
            'user_account_id': user.get('user_account_id', None),
            'product_id': args[0]
        }

        try:
            db_connection = get_db_connection()
            if db_connection:
                product_service = ProductService()
                add_to_cart_result = product_service.delete_from_cart(cart_info, db_connection)
                return add_to_cart_result
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @product_app.route('/<int:product_id>/cart', methods=['PUT'], endpoint='edit_unit_from_cart')
    @login_required
    @validate_params(
        Param('product_id', PATH, int)
    )
    def edit_unit_from_cart(*args):
        user = g.account_info
        cart_info = {
            'user_account_id': user.get('user_account_id', None),
            'product_id': args[0]
        }

        try:
            db_connection = get_db_connection()
            if db_connection:
                product_service = ProductService()
                add_to_cart_result = product_service.edit_unit_from_cart(cart_info, db_connection)
                return add_to_cart_result
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500