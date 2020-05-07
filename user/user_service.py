import bcrypt
import jwt
from flask import jsonify, g
from datetime import datetime, timedelta
from config import SECRET
from connection import DatabaseConnection, get_redis_connection

from .user_dao import UserDao


class UserService:
    def sign_up(self, user_info, db_connection, redis_connection):
        user_dao = UserDao()
        try:
            # email 중복 체크
            check_overlap_email_result = user_dao.check_overlap_email(user_info['email'], db_connection)
            print(check_overlap_email_result)
            if check_overlap_email_result:
                return jsonify({'message': 'EXISTING_EMAIL'}), 400

            # nick name 중복 체크
            check_overlap_nick_name_result = user_dao.check_overlap_nick_name(user_info['nick_name'], db_connection)
            print(check_overlap_nick_name_result)
            if check_overlap_nick_name_result:
                return jsonify({'message': 'EXISTING_NICK_NAME'}), 400

            # 중복체크까지 모두 끝나면 암호화된 비밀번호 생성
            bcrypted_password = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt())
            user_info['password'] = bcrypted_password

            # 회원가입 절차 진행
            sign_up_result = user_dao.sign_up(user_info, db_connection, redis_connection)
            return sign_up_result

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def sign_in(self, user_account_info, db_connection, redis_connection):

        # SellerDao 에서 가져온 정보를 담는 seller_dao 인스턴스 생성
        user_dao = UserDao()
        try:
            # seller_dao 에 있는 get_account_info 함수로 account_info 와 db_connection 을 인자로 넘겨줌
            user_account_result = user_dao.get_account_info(user_account_info, db_connection)

            # 만약 DB 에 login_id 가 존재하면
            if user_account_result:

                # bcrypt.checkpw 를 통해 암호화 된 password 와 인자로 받아 온 password 를 비교
                if bcrypt.checkpw(user_account_info['password'].encode('utf-8'),
                                  user_account_result['password'].encode('utf-8')):

                    # 두 password 가 일치하면 token 을 발급하는데 현재시간 + 3일 만큼 유효하도록 지정해 줌
                    token = jwt.encode({'user_account_id': user_account_result['id'],
                                        'exp': datetime.utcnow() + timedelta(days=3)},
                                       SECRET['secret_key'], algorithm=SECRET['algorithm'])

                    random_key = user_dao.gen_random_name()
                    redis_connection.set(random_key, token)
                    return jsonify({'key': random_key}), 200

                else:
                    # 만약 두 password 가 불일치하면 에러 메세지 return
                    return jsonify({'message': 'INVALID_PASSWORD'}), 401

            else:
                # DB에 login_id 가 존재하지 않으면 에러 메세지 return
                return jsonify({'message': 'INVALID_EMAIL'}), 400

        # 명시하지 않은 모든 에러를 잡아서 return
        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    # noinspection PyMethodMayBeStatic
    def get_user_list(self, user_search_keywords, user, db_connection):
        if user.get('auth_type_id', None) != 1:
            return jsonify({'message': 'NO_AUTHORIZATION'}), 403

        user_dao = UserDao()
        user_list_result = user_dao.get_user_list(user_search_keywords, db_connection)
        return user_list_result

    def get_user_info(self, target_user_id, user, db_connection):
        user_dao = UserDao()
        account_auth_type_id = user['auth_type_id']

        if account_auth_type_id == 1:
            get_user_info_result = user_dao.get_user_info(target_user_id, db_connection)
            return get_user_info_result

        return jsonify({'message': 'NO_AUTHORIZATION'}), 400

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