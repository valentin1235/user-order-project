import re
import json

from flask import request, Blueprint, jsonify, g
from flask_request_validator import (
    GET,
    FORM,
    PATH,
    JSON,
    Param,
    Pattern,
    MinLength,
    MaxLength,
    validate_params
)

from .user_service import UserService
from connection import get_db_connection, DatabaseConnection, get_redis_connection
from utils import login_required


class UserView:

    user_app = Blueprint('user_app', __name__, url_prefix='/user')

    @user_app.route('', methods=['POST'], endpoint='sign_up')
    @validate_params(
        Param('email', JSON, str,
              rules=[Pattern(r'^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$')]),
        Param('password', JSON, str,
              rules=[MaxLength(10)]),
        Param('password', JSON, str,
              rules=[MinLength(4)]),
        Param('contact_number', JSON, str,
              rules=[MaxLength(20)]),
        Param('name', JSON, str,
              rules=[MaxLength(20)]),
        Param('nick_name', JSON, str,
              rules=[MaxLength(30)]),
        Param('gender_id', JSON, int),
    )
    def sign_up(*args):
        if args[6] not in range(1,3):
            return jsonify({'message': 'INVALID_GENDER_ID'}), 400

        user_info = {
            'email': args[0],
            'password': args[1],
            'contact_number': args[3],
            'name': args[4],
            'nick_name': args[5],
            'gender_id': args[6]
        }

        # 데이터베이스 연결
        try:
            db_connection = get_db_connection()
            redis_connection = get_redis_connection()

            if db_connection:
                user_service = UserService()
                sign_up_result = user_service.sign_up(user_info, db_connection, redis_connection)
                return sign_up_result
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
                redis_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @user_app.route('/sign-in', methods=['POST'], endpoint='sign_in')
    @validate_params(
        Param('email', JSON, str,
              rules=[Pattern(r'^[a-zA-Z0-9]{1}[a-zA-Z0-9_-]{4,19}')]),
        Param('password', JSON, str,
              rules=[MaxLength(10)]),
        Param('password', JSON, str,
              rules=[MinLength(4)])
    )
    def sign_in(*args):
        # validation 확인이 된 data 를 account_info 로 재정의
        user_account_info = {
            'email': args[0],
            'password': args[2]
        }

        try:
            # DB에 연결
            db_connection = get_db_connection()
            redis_connection = get_redis_connection()
            if db_connection:

                # service 에 있는 SellerService 를 가져와서 seller_service 라는 인스턴스를 만듦
                seller_service = UserService()

                # 로그인 함수를 실행한 결과값을 login_result 에 저장
                signin_result = seller_service.sign_in(user_account_info, db_connection, redis_connection)
                return signin_result

            # DB가 열리지 않았을 경우
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        # 정의하지 않은 모든 error 를 잡아줌
        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        # try 랑 except 에 상관없이 무조건 실행
        finally:
            try:
                db_connection.close()
                redis_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @user_app.route('/log-out', methods=['POST'], endpoint='log_out')
    @login_required
    @validate_params(
        Param('key', JSON, str)
    )
    def log_out(*args):
        redis_connection = get_redis_connection()
        redis_connection.delete(args[0])
        return jsonify({'message': 'SUCCESS'}), 200

    @user_app.route('', methods=['GET'], endpoint='get_user_list')
    @login_required
    @validate_params(
        Param('user_id', GET, int, required=False),
        Param('email', GET, str, required=False),
        Param('name', GET, str, required=False),
        Param('nick_name', GET, str, required=False),
        Param('contact_number', GET, str, required=False),
        Param('gender_id', GET, str, required=False),
        Param('start_time', GET, str, required=False),
        Param('close_time', GET, str, required=False),
        Param('offset', GET, int, required=False),
        Param('limit', GET, int, required=False)
    )
    def get_user_list(*args):
        user = g.account_info

        # 유효성 확인 위해 기간 데이터 먼저 정의
        start_time = args[6]
        close_time = args[7]

        # 두 값이 모두 들어왔을 때, 시작 기간이 종료 기간보다 늦으면 시작기간 = 종료기간
        if start_time and close_time:
            if start_time > close_time:
                start_time = close_time

        user_search_keywords = {
            'user_id': args[0],
            'email': args[1],
            'name': args[2],
            'nick_name': args[3],
            'contact_number': args[4],
            'gender_id': args[5],
            'start_time': start_time,
            'close_time': close_time,
            'offset': args[8] if args[8] else 0,
            'limit': args[9] if args[9] else 10
        }

        if user_search_keywords['limit'] > 5000:
            return jsonify({'message': 'INVALID_REQUEST'}), 400

        # 데이터베이스 커넥션을 열어줌.
        try:
            db_connection = DatabaseConnection()
            if db_connection:
                user_service = UserService()
                seller_list_result = user_service.get_user_list(user_search_keywords, user, db_connection)
                return seller_list_result
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @user_app.route('/<int:user_id>', methods=['GET'], endpoint='get_user_info')
    @login_required
    @validate_params(
        Param('user_id', PATH, int)
    )
    def get_user_info(*args):
        user = g.account_info
        target_user_id = {'target_user_id': args[0]}

        try:
            db_connection = get_db_connection()
            if db_connection:
                user_service = UserService()
                getting_seller_info_result = user_service.get_user_info(target_user_id, user, db_connection)
                return getting_seller_info_result

            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @user_app.route('/mypage', methods=['GET'], endpoint='get_my_page')
    @login_required
    def get_my_page():
        user = g.account_info
        user_account_id = {
            'target_user_id': user['user_account_id']
        }

        try:
            db_connection = get_db_connection()
            if db_connection:
                user_service = UserService()
                getting_seller_info_result = user_service.get_my_page(user_account_id, db_connection)

                return getting_seller_info_result

            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()

            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @user_app.route('/my-cart', methods=['GET'], endpoint='get_my_cart')
    @login_required
    @validate_params(
        Param('offset', GET, int, required=False),
        Param('limit', GET, int, required=False)
    )
    def get_my_cart(*args):
        user = g.account_info
        cart_info = {
            'user_account_id': user.get('user_account_id', None),
            'offset': args[0] if args[0] else 0,
            'limit': args[1] if args[1] else 10
        }

        try:
            db_connection = get_db_connection()
            if db_connection:
                user_service = UserService()
                get_my_cart_result = user_service.get_my_cart(cart_info, db_connection)
                return get_my_cart_result
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @user_app.route('/my-cart/order', methods=['POST'], endpoint='check_out_cart')
    @login_required
    @validate_params(
        Param('cart_id', JSON, int)
    )
    def make_order(*args):
        user = g.account_info
        order_info = {
            'user_account_id': user.get('user_account_id'),
            'cart_id': args[0]
        }
        try:
            db_connection = get_db_connection()
            if db_connection:
                user_service = UserService()
                make_order_result = user_service.make_order(order_info, db_connection)
                return make_order_result
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500

    @user_app.route('/my-cart/order', methods=['GET'], endpoint='get_order_receipt')
    @login_required
    @validate_params(
        Param('receipt_id', GET, int),
        Param('checked_out_cart_id', GET, int)
    )
    def get_order_receipt(*args):
        user = g.account_info
        receipt_info = {
            'receipt_id': args[0],
            'checked_out_cart_id': args[1],
            'user_account_id': user.get('user_account_id', None),
            'offset': 0,
            'limit': 10
        }
        try:
            db_connection = get_db_connection()
            if db_connection:
                user_service = UserService()
                get_order_receipt_result = user_service.get_order_receipt(receipt_info, db_connection)
                return get_order_receipt_result
            else:
                return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

        finally:
            try:
                db_connection.close()
            except Exception as e:
                return jsonify({'message': f'{e}'}), 500
