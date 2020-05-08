import uuid, jwt

from datetime import datetime, timedelta
from flask import jsonify
from mysql.connector.errors import Error

from config import SECRET


class UserDao:
    def gen_random_name(self):
        random_name = str(uuid.uuid4())
        return random_name

    def sign_up(self, user_info, db_connection, redis_connection):
        try:
            with db_connection.cursor() as db_cursor:

                insert_user_accounts_statement = """
                    INSERT INTO user_accounts(
                        email,
                        password
                    ) VALUES (
                        %(email)s,
                        %(password)s
                    )"""

                db_cursor.execute(insert_user_accounts_statement, user_info)

                user_account_id = db_cursor.lastrowid
                user_info['user_account_id'] = user_account_id

                # user_infos 생성
                # 셀러정보 INSERT 문
                insert_user_infos_statement = """
                    INSERT INTO user_infos(
                        name,
                        nick_name,
                        contact_number,
                        gender_id,
                        user_account_id
                    ) VALUES (
                        %(name)s,
                        %(nick_name)s,
                        %(contact_number)s,
                        %(gender_id)s,
                        %(user_account_id)s
                    )"""

                # 데이터 sql 명령문과 셀러 데이터 바인딩
                db_cursor.execute(insert_user_infos_statement, user_info)
                db_connection.commit()

            if user_info['user_account_id']:
                token = jwt.encode({'user_account_id': user_info['user_account_id'],
                                    'exp': datetime.utcnow() + timedelta(days=6)},
                                   SECRET['secret_key'], algorithm=SECRET['algorithm'])
                random_key = self.gen_random_name()
                redis_connection.set(random_key, token)
                return jsonify({'key': random_key}), 200
            return jsonify({'message': 'USER_ACCOUNT_NOT_EXISTS'}), 400

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def check_overlap_email(self, email, db_connection):

        try:
            with db_connection.cursor() as db_cursor:

                # 계정 SELECT 문
                select_user_account_statement = """
                    SELECT id
                    FROM user_accounts
                    WHERE email = %(email)s
                    AND is_deleted = 0
                """

                # service 에서 넘어온 셀러 데이터
                input_email = {
                    'email': email
                }

                # 데이터 sql 명령문과 셀러 데이터 바인딩
                db_cursor.execute(select_user_account_statement, input_email)

                # 쿼리로 나온 계정번호를 저장
                select_result = db_cursor.fetchone()
                return select_result

        # 데이터베이스 error
        except Exception as e:
            print(f'DAO_DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'error': 'DB_CURSOR_ERROR'}), 500

    # noinspection PyMethodMayBeStatic
    def check_overlap_nick_name(self, nick_name, db_connection):

        try:
            with db_connection.cursor() as db_cursor:

                # 셀러정보 SELECT 문
                select_user_info_statement = """
                    SELECT id
                    FROM user_infos
                    WHERE nick_name = %(nick_name)s
                    AND is_deleted = 0
                """

                # service 에서 넘어온 셀러 데이터
                input_nick_name = {
                    'nick_name': nick_name
                }

                # 데이터 sql 명령문과 셀러 데이터 바인딩
                db_cursor.execute(select_user_info_statement, input_nick_name)

                # 쿼리로 나온 셀러정보 번호를 저장
                select_result = db_cursor.fetchone()
                return select_result

        except KeyError as e:
            print(f'KEY_ERROR_WITH {e}')
            db_connection.rollback()
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Exception as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'error': 'DB_CURSOR_ERROR'}), 500

    def get_account_info(self, user_account_info, db_connection):

        try:
            # db_cursor 는 db_connection 에 접근하는 본체 (가져온 정보는 cursor 가 가지고 있다)
            with db_connection as db_cursor:

                # sql 문 작성 (원하는 정보를 가져오거나 집어넣거나)
                select_user_account_statement = """
                    SELECT id, password                    
                    FROM user_accounts  
                    WHERE email = %(email)s 
                    AND is_deleted = 0
                """

                # SELECT 문 실행
                db_cursor.execute(select_user_account_statement, user_account_info)

                # DB 에 저장하는 로직 작성 (fetchone, fetchall, fetchmany)
                user_account_result = db_cursor.fetchone()

                # DB 에서 꺼내온 정보를 return
                return user_account_result

        except KeyError as e:
            print(f'KEY_ERROR WITH {e}')
            return jsonify({'message': 'INVALID_KEY'}), 400

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def get_user_list(self, user_search_keywords, db_connection):
        select_user_list_statement = '''
            SELECT 
            ua.id as user_id,
            ua.email as email,
            ua.created_at as created_at,
            ui.name as name,
            ui.nick_name as nick_name,
            ui.contact_number as contact_number,
            gd.gender as gender
            FROM user_infos as ui
            right JOIN user_accounts as ua ON ua.id = ui.user_account_id
            LEFT JOIN genders as gd ON gd.id = ui.gender_id
            WHERE ui.close_time = '2037-12-31 23:59:59.0'
            AND ui.is_deleted = 0
            AND ua.is_deleted = 0
            AND ua.auth_type_id = 2
        '''

        filter_query_values_count_statement = '''
            SELECT COUNT(0) as filtered_user_count
            FROM user_infos
            right JOIN user_accounts ON user_accounts.id = user_infos.user_account_id
            WHERE user_infos.close_time = '2037-12-31 23:59:59.0'
            AND user_infos.is_deleted = 0 
            AND user_accounts.is_deleted = 0
            AND user_accounts.auth_type_id = 2
        '''

        if user_search_keywords.get('user_id', None):
            select_user_list_statement += " AND ua.id = %(user_id)s"
            filter_query_values_count_statement += " AND user_accounts.id = %(user_id)s"

        email = user_search_keywords.get('email', None)
        if email:
            user_search_keywords['email'] = '%' + email + '%'
            select_user_list_statement += " AND ua.email LIKE %(email)s"
            filter_query_values_count_statement += " AND user_accounts.email LIKE %(email)s"

        name = user_search_keywords.get('name', None)
        if name:
            user_search_keywords['name'] = '%'+name+'%'
            select_user_list_statement += " AND ui.name LIKE %(name)s"
            filter_query_values_count_statement += " AND name LIKE %(name)s"

        nick_name = user_search_keywords.get('nick_name', None)
        if nick_name:
            user_search_keywords['nick_name'] = '%' + nick_name + '%'
            select_user_list_statement += " AND ui.nick_name LIKE %(nick_name)s"
            filter_query_values_count_statement += " AND nick_name LIKE %(nick_name)s"

        contact_number = user_search_keywords.get('contact_number', None)
        if contact_number:
            user_search_keywords['contact_number'] = '%'+contact_number+'%'
            select_user_list_statement += " AND ui.contact_number LIKE %(contact_number)s"
            filter_query_values_count_statement += " AND user_infos.contact_number LIKE %(contact_number)s"

        if user_search_keywords.get('gender_id', None):
            select_user_list_statement += " AND ui.gender_id = %(gender_id)s"
            filter_query_values_count_statement += " AND user_infos.gender_id = %(gender_id)s"

        start_time = user_search_keywords.get('start_time')
        close_time = user_search_keywords.get('close_time')
        if start_time and close_time:
            user_search_keywords['start_time'] = start_time + ' 00:00:00'
            user_search_keywords['close_time'] = close_time + ' 23:59:59'
            select_user_list_statement += " AND ua.created_at > %(start_time)s AND ua.created_at < %(close_time)s"
            filter_query_values_count_statement += " AND user_accounts.created_at > %(start_time)s AND user_accounts.created_at < %(close_time)s"

        # sql 명령문에 키워드 추가가 완료되면 정렬, limit, offset 쿼리문을 추가해준다.
        select_user_list_statement += " ORDER BY ui.user_account_id DESC LIMIT %(limit)s OFFSET %(offset)s"

        try:
            with db_connection as db_cursor:

                # sql 쿼리와 pagination 데이터 바인딩
                db_cursor.execute(select_user_list_statement, user_search_keywords)
                user_info = db_cursor.fetchall()

                # pagination 을 위해서 전체 셀러가 몇명인지 count 해서 기존의 seller_info 에 넣어줌.
                user_count_statement = '''
                    SELECT 
                    COUNT(user_account_id) as total_user_count
                    FROM user_infos
                    LEFT JOIN user_accounts ON user_infos.user_account_id = user_accounts.id 
                    WHERE close_time = '2037-12-31 23:59:59.0' 
                    AND user_accounts.is_deleted = 0
                    AND user_infos.is_deleted = 0
                    AND user_accounts.auth_type_id = 2
                '''
                db_cursor.execute(user_count_statement)
                user_count = db_cursor.fetchone()

                db_cursor.execute(filter_query_values_count_statement, user_search_keywords)
                filter_query_values_count = db_cursor.fetchone()
                user_count['filtered_user_count'] = filter_query_values_count['filtered_user_count']
                return jsonify({'user_list': user_info, 'user_count': user_count}), 200

        # 데이터베이스 error
        except Exception as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'error': 'DB_CURSOR_ERROR'}), 500

    def get_user_info(self, target_user_id, db_connection):
        try:
            with db_connection.cursor() as db_cursor:

                select_target_user_statement = """
                    SELECT 
                    ua.id as id,
                    ua.email as email,
                    ua.created_at as created_at,
                    ui.name as name,
                    ui.nick_name as nick_name,
                    ui.contact_number as contact_number,
                    gd.gender as gender
                    FROM user_accounts AS ua
                    LEFT JOIN user_infos AS ui ON ua.id = ui.user_account_id
                    LEFT JOIN genders AS gd ON gd.id = ui.gender_id
                    WHERE ua.id = %(target_user_id)s
                    AND ua.is_deleted = 0
                    AND ui.is_deleted = 0
                    AND ui.close_time = '2037-12-31 23:59:59'
                    AND ua.auth_type_id = 2
                """

                # SELECT 문 실행
                db_cursor.execute(select_target_user_statement, target_user_id)

                # seller_info_result 에 쿼리 결과 저장
                target_user_info = db_cursor.fetchone()

                # 해당 번호의 셀러가 없으면 에러 리턴
                if not target_user_info:
                    return jsonify({'message': 'USER_NOT_EXISTS'}), 404

                return target_user_info

        except KeyError as e:
            print(f'KEY_ERROR WITH {e}')
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def get_cart_info(self, cart_info, db_connection):
        try:
            with db_connection.cursor() as db_cursor:

                # get recent cart id
                db_cursor.execute("""
                    SELECT id 
                    FROM carts 
                    WHERE user_account_id = %(user_account_id)s
                    AND is_checked_out = 0
                """, cart_info)

                recent_cart_id = db_cursor.fetchone()
                if not recent_cart_id:
                    return ({'message': 'CART_NOT_EXISTS'}), 404
                cart_id = recent_cart_id.get('id', None)
                cart_info['cart_id'] = cart_id

                # get product information in a cart
                db_cursor.execute("""
                    SELECT 
                        (select id from orders where products.id = orders.product_id order by created_at limit 1) as order_id,
                        (select created_at from orders where products.id = orders.product_id order by created_at limit 1) as created_at,
                        (select COUNT(0) from orders where products.id = orders.product_id and carts.id = orders.cart_id) as units,
                        products.id AS product_id,
                        products.name AS product_name    
                    FROM carts
                    RIGHT JOIN orders ON carts.id = orders.cart_id 
                    LEFT JOIN products ON products.id = orders.product_id
                    WHERE carts.is_checked_out = 0
                    AND carts.id = %(cart_id)s
                    AND orders.is_checked_out = 0
                    GROUP BY orders.product_id
                    LIMIT %(limit)s OFFSET %(offset)s
                """, cart_info)

                cart_product_list = db_cursor.fetchall()
                return jsonify({'cart_products': cart_product_list, 'cart_id': cart_id}), 200

        except KeyError as e:
            print(f'KEY_ERROR WITH {e}')
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def make_order(self, order_info, db_connection):
        try:
            with db_connection.cursor() as db_cursor:

                # check existence of the cart matching to user_account_id
                db_cursor.execute('''
                    SELECT 
                    EXISTS(SELECT id FROM carts WHERE id = %(cart_id)s AND is_checked_out = 0) as existence
                ''', order_info)
                if db_cursor.fetchone().get('existence', None) == 0:
                    return jsonify({'message': 'CART_NOT_EXISTS'}), 404

                # check out cart
                db_cursor.execute("""
                    UPDATE carts
                    SET is_checked_out = 1
                    WHERE id = %(cart_id)s
                """, order_info)
                order_info['order_number'] = self.gen_random_name()

                db_cursor.execute("""
                    UPDATE orders
                    SET is_checked_out = 1
                    WHERE cart_id = %(cart_id)s
                """, order_info)

                # make an order
                db_cursor.execute("""
                    INSERT INTO receipts
                    (
                        cart_id,
                        order_number
                    ) VALUES (
                        %(cart_id)s,
                        %(order_number)s
                    )
                """, order_info)

                recent_receipt_id = db_cursor.lastrowid
                db_connection.commit()

                return jsonify({
                    'checked_out_cart_id': order_info.get('cart_id', None),
                    'receipt_id': recent_receipt_id
                }), 200

        except KeyError as e:
            print(f'KEY_ERROR WITH {e}')
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500

    def get_order_receipt(self, receipt_info, db_connection):
        try:
            with db_connection.cursor() as db_cursor:
                db_cursor.execute('''
                    SELECT * 
                    FROM receipts
                    LEFT JOIN carts ON receipts.cart_id = carts.id
                    WHERE carts.id = %(checked_out_cart_id)s
                    AND receipts.id = %(receipt_id)s
                    AND user_account_id = %(user_account_id)s
                ''', receipt_info)
                receipt_detail = db_cursor.fetchone()
                if not receipt_detail:
                    return jsonify({'message': 'ORDER_NOT_EXISTS'}), 404

                db_cursor.execute("""
                    SELECT 
                        (select COUNT(0) from orders where products.id = orders.product_id and carts.id = orders.cart_id) as units,
                        products.id AS product_id,
                        products.name AS product_name    
                    FROM carts
                    RIGHT JOIN orders ON carts.id = orders.cart_id 
                    LEFT JOIN products ON products.id = orders.product_id
                    WHERE carts.is_checked_out = 1
                    AND carts.id = %(checked_out_cart_id)s
                    AND orders.is_checked_out = 1
                    GROUP BY orders.product_id
                    LIMIT %(limit)s OFFSET %(offset)s
                """, receipt_info)
                order_list = db_cursor.fetchall()
                receipt_detail['order_list'] = order_list

                return jsonify({'receipt': receipt_detail}), 200

        except KeyError as e:
            print(f'KEY_ERROR WITH {e}')
            return jsonify({'message': 'INVALID_KEY'}), 500

        except Error as e:
            print(f'DATABASE_CURSOR_ERROR_WITH {e}')
            return jsonify({'message': 'DB_CURSOR_ERROR'}), 500