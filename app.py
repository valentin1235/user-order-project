from datetime import timedelta, datetime
from decimal import Decimal

from flask import Flask
from flask_cors import CORS
from flask.json import JSONEncoder

from user.user_view import UserView
from product.product_view import ProductView


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):

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

    # set flask object
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config['DEBUG'] = True
    CORS(app)
    app.register_blueprint(UserView.user_app)
    app.register_blueprint(ProductView.product_app)

    return app


