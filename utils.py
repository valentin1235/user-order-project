import jwt
from psycopg2 import OperationalError
from sqlalchemy.orm import sessionmaker
from flask import request, jsonify, g
from user.user_dao import User, engine
from config import SECRET


def login_required(func):
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if access_token:
            try:
                payload = jwt.decode(access_token, SECRET['secret_key'], algorithm=SECRET['algorithm'])
                id = payload['id']

                Session = sessionmaker(bind=engine)
                try:
                    session = Session()
                    user_info_db = session.query(User.auth_type_id, User.is_deleted).filter(User.id == payload['id']).one()

                    if user_info_db:
                        if not user_info_db[1]:
                            g.user_info = {
                                'user_id': id,
                                'auth_type_id': user_info_db[0]
                            }
                            return func(*args, **kwargs)
                        return jsonify({'message': 'DELETED_ACCOUNT'}), 400
                    return jsonify({'message': 'ACCOUNT_DOES_NOT_EXIST'}), 404

                except TypeError:
                    return jsonify({'message': 'NON_EXISTS'}), 400

                except Exception as e:
                    print(e)
                    return jsonify({'message': e}), 400

                finally:
                    try:
                        session.close()
                    except Exception as e:
                        print(e)
                        return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

            except jwt.InvalidTokenError:
                return jsonify({'message': 'INVALID_TOKEN'}), 401

        return jsonify({'message': 'INVALID_TOKEN'}), 401
    return wrapper
