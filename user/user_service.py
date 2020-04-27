from flask import jsonify, g
from .user_dao import engine
from sqlalchemy.orm import sessionmaker
from .user_dao import User


class UserService:
    def sigh_up(self, request):
        data = request.json
        user = User()
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            user.full_name = data['full_name']
            user.email = data['email']
            user.password = data['password']
            session.add(user)
            session.commit()

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
                try:
                    session.close()
                except Exception as e:
                    print(e)
                    return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

        return jsonify({'message': 'SUCCESS'}), 200
