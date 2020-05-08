import uuid, jwt

from datetime import datetime, timedelta
from flask import jsonify
from mysql.connector.errors import Error

from config import SECRET


class ProductDao:
    def gen_random_name(self):
        random_name = str(uuid.uuid4())
        return random_name

    def get_product_list(self, product_keyword_search, db_connection):
        try:
            with db_connection.cursor() as db_cursor:

                get_product_list_statement = """
                    SELECT id, name
                    FROM products
                """

                id = product_keyword_search.get('id', None)
                if id:
                    get_product_list_statement += " AND id = %(id)s"

                name = product_keyword_search.get('name', None)
                if name:
                    product_keyword_search['name'] = '%' + name + '%'
                    get_product_list_statement += " AND name LIKE %(name)s"

                get_product_list_statement += " ORDER BY created_at DESC LIMIT %(limit)s OFFSET %(offset)s"

                # 데이터 sql 명령문과 셀러 데이터 바인딩
                db_cursor.execute(get_product_list_statement, product_keyword_search)
                product_list = db_cursor.fetchall()
                return jsonify({'product_list': product_list}), 200

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def get_product_detail(self, product_id, db_connection):
        try:
            with db_connection.cursor() as db_cursor:

                get_product_detail_statement = """
                    SELECT id, name, created_at
                    FROM products
                    WHERE id = %(product_id)s
                """

                # 데이터 sql 명령문과 셀러 데이터 바인딩
                db_cursor.execute(get_product_detail_statement, product_id)
                product_detail = db_cursor.fetchone()
                return jsonify({'product_list': product_detail}), 200

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def add_to_cart(self, cart_info, db_connection):
        try:
            with db_connection.cursor() as db_cursor:
                db_cursor.execute("""
                    SELECT id
                    FROM carts
                    WHERE user_account_id = %(user_account_id)s
                    AND is_checked_out = 0
                """, cart_info)
                current_cart_id = db_cursor.fetchone()
                if current_cart_id:
                    cart_info['cart_id'] = current_cart_id.get('id', None)

                elif not current_cart_id:
                    # create new cart
                    db_cursor.execute("""
                        INSERT INTO carts
                            (
                                user_account_id
                            ) VALUES (
                                %(user_account_id)s
                            )
                        """, cart_info)

                    cart_info['cart_id'] = db_cursor.lastrowid

                # create an order
                db_cursor.execute("""
                    INSERT INTO orders
                        (
                            cart_id,
                            product_id
                        ) VALUES (
                            %(cart_id)s,
                            %(product_id)s
                        )
                    """, cart_info)

                db_connection.commit()
                return jsonify({'message': 'SUCCESS'}), 200

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def delete_from_cart(self, cart_info, db_connection):
        try:
            with db_connection.cursor() as db_cursor:

                db_cursor.execute("""
                   DELETE FROM orders
                   WHERE cart_id = (select id from carts where user_account_id = %(user_account_id)s and is_checked_out = 0)
                   AND product_id = %(product_id)s
                   AND is_checked_out = 0
                """, cart_info)

                db_connection.commit()
                return jsonify({'message': 'SUCCESS'}), 200

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY_IN_DB'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def edit_unit_from_cart(self, cart_info, db_connection):

        try:
            with db_connection.cursor() as db_cursor:
                db_cursor.execute("""
                    select id 
                    from orders 
                    where product_id = %(product_id)s 
                    and is_checked_out = 0 
                    order by created_at desc 
                    limit 1
                """, cart_info)
                cart_info['recent_order_id'] = db_cursor.fetchone()['id']

                db_cursor.execute("""
                   DELETE FROM orders
                   WHERE cart_id = (select id from carts where user_account_id = %(user_account_id)s and is_checked_out = 0)
                   AND id = %(recent_order_id)s
                """, cart_info)

                db_connection.commit()
                return jsonify({'message': 'SUCCESS'}), 200

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY_IN_DB'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

