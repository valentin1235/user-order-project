from datetime import timedelta, datetime
from decimal import Decimal

from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis
from flask.json import JSONEncoder
from user.user_view import UserView
from board.board_view import BoardView


class CustomJSONEncoder(JSONEncoder):

    """
    default JSONEncoder 에 필요한 자료형 추가
    """
    def default(self, obj):
        """

        Args:
            obj: json 형태로 반환하고자 하는 객체

        Returns: obj 를 json 형태로 변경하는 기능이 추가된 JSONEncoder

        Authors:
            leesh3@brandi.co.kr (이소헌)

        History:
            2020-03-25 (leesh3@brandi.co.kr): 초기 생성
        """

        if isinstance(obj, set):
            return list(obj)

        if isinstance(obj, timedelta):
            return str(obj)

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, bytes):
            return obj.decode("utf-8")

        if isinstance(obj, datetime):
            return datetime.strftime(obj+timedelta(hours=+9), '%Y-%m-%d %H:%M:%S')

        return JSONEncoder.default(self, obj)


def create_app():
    """

    Returns:
        생성된 플라스크 앱 객체

    Authors:
        leesh3@brandi.co.kr (이소헌)
        yoonhc@brandi.co.kr (윤희철)

    History:
        2020-03-25 (leesh3@brandi.co.kr): 초기 생성

    """
    # set flask object
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config['DEBUG'] = True
    CORS(app, resources={r"/*/*": {"origins": "*"}})
    flask_redis = FlaskRedis(app)
    flask_redis.init_app(app)
    app.register_blueprint(UserView.user_app)
    app.register_blueprint(BoardView.board_app)

    return app


