import pymysql, redis
import mysql.connector

from flask import jsonify

from mysql.connector.errors import InterfaceError, ProgrammingError, NotSupportedError
from config import DATABASES, REDIS


class DatabaseConnection:
    def __init__(self):

        self.db_config = {
            'database': DATABASES['database'],
            'user': DATABASES['user'],
            'password': DATABASES['password'],
            'host': DATABASES['host'],
            'port': DATABASES['port'],
            'charset': DATABASES['charset'],
            'collation': DATABASES['collation'],
        }
        try:
            self.db_connection = mysql.connector.connect(**self.db_config)

        except InterfaceError as e:
            print(f'INTERFACE_ERROR_WITH {e}')

        except ProgrammingError as e:
            print(f'PROGRAMMING_ERROR_WITH {e}')

        except NotSupportedError as e:
            print(f'NOT_SUPPORTED_ERROR_WITH {e}')

    def __enter__(self):
        try:
            self.cursor = self.db_connection.cursor(buffered=True, dictionary=True)
            return self.cursor

        except AttributeError as e:
            print(e)
            return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

    def __exit__(self, exc_type, exc_value, exc_trance):
        try:
            self.cursor.close()
        except AttributeError as e:
            print(e)
            return jsonify({'message': 'NO_DATABASE_CONNECTION'}), 500

    def close(self):
        return self.db_connection.close()

    def commit(self):
        return self.db_connection.commit()

    def rollback(self):
        return self.db_connection.rollback()


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
