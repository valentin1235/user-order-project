import bcrypt
import jwt
from flask import jsonify, g
from datetime import datetime, timedelta
from config import SECRET
from connection import DatabaseConnection, get_redis_connection

from .product_dao import ProductDao


class ProductService:
    def get_product_list(self, product_keyword_search, db_connection):
        product_dao = ProductDao()
        try:
            get_product_list = product_dao.get_product_list(product_keyword_search, db_connection)
            return get_product_list

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def get_product_detail(self, product_id, db_connection):
        product_dao = ProductDao()
        try:
            get_product_detail = product_dao.get_product_detail(product_id, db_connection)
            return get_product_detail

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def add_to_cart(self, cart_info, db_connection):
        product_dao = ProductDao()
        try:
            add_to_cart_result = product_dao.add_to_cart(cart_info, db_connection)
            return add_to_cart_result

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def delete_from_cart(self, cart_info, db_connection):
        product_dao = ProductDao()
        try:
            delete_from_cart_result = product_dao.delete_from_cart(cart_info, db_connection)
            return delete_from_cart_result

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

    def edit_unit_from_cart(self, cart_info, db_connection):
        product_dao = ProductDao()
        try:
            delete_from_cart_result = product_dao.edit_unit_from_cart(cart_info, db_connection)
            return delete_from_cart_result

        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

