import pymysql, redis
from flask import jsonify

from mysql.connector.errors import InterfaceError, ProgrammingError, NotSupportedError
from config import DATABASES, REDIS


def get_db_connection():
    db_config = {
        'database': DATABASES['database'],
        'user': DATABASES['user'],
        'password': DATABASES['password'],
        'host': DATABASES['host'],
        'port': DATABASES['port'],
        'charset': DATABASES['charset'],
        'cursorclass': pymysql.cursors.DictCursor,
    }
    db = pymysql.connect(**db_config)
    return db


def get_redis_connection():
    try:
        redis_connection = redis.Redis(host=REDIS['host'], port=REDIS['port'])
        return redis_connection

    except Exception as e:
        print(e)
        return jsonify({'message': 'REDIS_CONNECTION_ERROR'})
