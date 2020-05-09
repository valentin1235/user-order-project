import bcrypt
import jwt
from flask import jsonify, g
from datetime import datetime, timedelta
from config import SECRET

from .user_dao import UserDao


class UserService:
    def sign_up(self, user_info, db_connection, redis_connection):
        user_dao = UserDao()
        try:
            # email overlap check
            check_overlap_email_result = user_dao.check_overlap_email(user_info['email'], db_connection)
            if check_overlap_email_result:
                return jsonify({'message': 'EXISTING_EMAIL'}), 400

            # nick name overlap check
            check_overlap_nick_name_result = user_dao.check_overlap_nick_name(user_info['nick_name'], db_connection)
            if check_overlap_nick_name_result:
                return jsonify({'message': 'EXISTING_NICK_NAME'}), 400

            bcrypted_password = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt())
            user_info['password'] = bcrypted_password

            # sign up procedure
            sign_up_result = user_dao.sign_up(user_info, db_connection, redis_connection)
            return sign_up_result

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def sign_in(self, user_account_info, db_connection, redis_connection):
        user_dao = UserDao()

        try:
            user_account_result = user_dao.get_account_info(user_account_info, db_connection)
            if user_account_result:
                if bcrypt.checkpw(user_account_info['password'].encode('utf-8'),
                                  user_account_result['password'].encode('utf-8')):

                    token = jwt.encode({'user_account_id': user_account_result['id'],
                                        'exp': datetime.utcnow() + timedelta(days=3)},
                                       SECRET['secret_key'], algorithm=SECRET['algorithm'])

                    random_key = user_dao.gen_random_name()
                    redis_connection.set(random_key, token)
                    return jsonify({'key': random_key}), 200
                else:
                    return jsonify({'message': 'INVALID_PASSWORD'}), 401
            else:
                return jsonify({'message': 'INVALID_EMAIL'}), 400

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def get_user_list(self, user_search_keywords, user, db_connection):
        if user.get('auth_type_id', None) != 1:
            return jsonify({'message': 'NO_AUTHORIZATION'}), 403

        user_dao = UserDao()
        user_list_result = user_dao.get_user_list(user_search_keywords, db_connection)
        return user_list_result

    def get_user_info(self, target_user_info, user, db_connection):
        user_dao = UserDao()
        account_auth_type_id = user['auth_type_id']
        if account_auth_type_id != 1:
            return jsonify({'message': 'UNAUTHORIZED'}), 403

        # get user information from dao
        user_info = user_dao.get_user_info(target_user_info, db_connection)

        # get order receipt of the user from dao
        try:
            with db_connection.cursor() as db_cursor:
                db_cursor.execute("""
                    select cart_id from receipts where id = %(receipt_id)s
                """, target_user_info)
                cart_id = db_cursor.fetchone()
                if not cart_id:
                    return jsonify({'message': 'INVALID_RECEIPT'}), 400

                target_user_info['checked_out_cart_id'] = cart_id.get('cart_id', None)
                receipt_detail = user_dao.get_order_receipt(target_user_info, db_connection)
                user_info['receipt_detail'] = receipt_detail
                return jsonify({'user_info': user_info}), 200

        except KeyError as e:
            print(f'KEY_ERROR WITH {e}')
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Exception as e:
            print(e)
            return jsonify({'message': f'{e}'}), 500

    def get_my_page(self, user_account_id, db_connection):
        user_dao = UserDao()

        try:
            getting_seller_info_result = user_dao.get_user_info(user_account_id, db_connection)
            return getting_seller_info_result

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def get_my_cart(self, cart_info, db_connection):
        user_dao = UserDao()

        try:
            get_my_cart_result = user_dao.get_cart_info(cart_info, db_connection)
            return get_my_cart_result

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def make_order(self, order_info, db_connection):
        user_dao = UserDao()

        try:
            make_order_result = user_dao.make_order(order_info, db_connection)
            return make_order_result

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def get_my_order_receipt(self, receipt_info, db_connection):
        user_dao = UserDao()

        try:
            receipt_detail = user_dao.get_order_receipt(receipt_info, db_connection)
            return jsonify({'receipt': receipt_detail}), 200

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500
