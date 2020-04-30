import redis

from flask import jsonify
from config import DATABASES, REDIS
from sqlalchemy import create_engine


def get_db_connection():
    try:
        engine = create_engine(
            f'postgresql://{DATABASES["user"]}:{DATABASES["password"]}@{DATABASES["host"]}/{DATABASES["database"]}',
            echo=True
        )
        return engine

    except Exception as e:
        print(e)
        return jsonify({'message': 'DB_CONNECTION_ERROR'}), 500


def get_redis_connection():
    try:
        redis_connection = redis.Redis(host=REDIS['host'], port=REDIS['port'])
        return redis_connection

    except Exception as e:
        print(e)
        return jsonify({'message': 'REDIS_CONNECTION_ERROR'})