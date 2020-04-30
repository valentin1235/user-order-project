import bcrypt, jwt
from datetime import datetime, timedelta

from .user_dao import User
from connection import get_db_connection

from config import SECRET

from flask import jsonify
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker


class UserService:
    def sigh_up(self, user_info):
        engine = get_db_connection()
        user = User()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if session.query(exists().where(User.email == user_info['email'])).one()[0]:
                return jsonify({'message': 'USER_EXISTS'}), 400
            hashed_password = bcrypt.hashpw(user_info.get('password', None).encode('utf-8'), bcrypt.gensalt()).decode()
            user.full_name = user_info['full_name']
            user.email = user_info['email']
            user.password = hashed_password
            user.auth_type_id = user_info['auth_type_id']
            session.add(user)
            session.commit()
            token = jwt.encode({'id': user.id,
                                'exp': datetime.utcnow() + timedelta(days=6)},
                               SECRET['secret_key'], algorithm=SECRET['algorithm'])

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
                try:
                    session.close()
                except Exception as e:
                    print(e)
                    return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

        return jsonify({'token': token}), 200

    def sign_in(self, user_info):
        engine = get_db_connection()
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            user_info_db = session.query(User.password, User.id).filter(User.email == user_info['email']).all()

            if len(user_info_db) == 0:
                return jsonify({'message': 'USER_NOT_EXISTS'}), 400

            # if session.query(exists().where(User.email == user_info['email'])).one()[0]:
            elif bcrypt.checkpw(user_info['password'].encode('utf-8'),
                              user_info_db[0][0].encode('utf-8')):
                token = jwt.encode({'id': user_info_db[0][1],
                    'exp': datetime.utcnow() + timedelta(days=6)},
                    SECRET['secret_key'], algorithm=SECRET['algorithm'])

                return jsonify({'token': token}), 200
            return jsonify({'message': 'INVALID_REQUEST'}), 401

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500
