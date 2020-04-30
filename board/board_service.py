from .board_dao import Board, Article
from connection import get_db_connection
from user.user_dao import User

from flask import jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters


class BoardService:
    def make_board(self, board_info):
        board = Board()
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            board.uploader = board_info['uploader']
            board.name = board_info['name']
            session.add(board)
            session.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
                try:
                    session.close()
                except Exception as e:
                    print(e)
                    return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

    def get_board_list(self, board_info):
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            filter_list = [
                {'model': 'Board', 'field': 'is_deleted', 'op': '==', 'value': False},
            ]
            if board_info.get('name', None):
                filter_list.append({'model': 'Board', 'field': 'name', 'op': 'like', 'value': '%'+board_info['name']+'%'})

            board_query = (session
                          .query(Board.id, Board.name, Board.uploader, Board.create_at))
            board_list = apply_filters(board_query, filter_list).slice(board_info['offset'], board_info['limit']).all()
            boards = [{
                    'id': board[0],
                    'name': board[1],
                    'uploader': board[2],
                    'created_at': board[3]
                } for board in board_list]
            return boards

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

    def edit_board(self, board_info):
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if session.query(Board.is_deleted).filter(Board.id == board_info['board_id']).one()[0]:
                return jsonify({'message': 'BOARD_NOT_EXISTS'}), 404

            (session
             .query(Board)
             .filter(Board.id == board_info['board_id'])
             .update({'name': board_info['new_name'], 'modifier': board_info['modifier']}))

            session.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

    def delete_board(self, board_info):
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if session.query(Board.is_deleted).filter(Board.id == board_info['board_id']).one()[0]:
                return  jsonify({'message': 'BOARD_NOT_EXISTS'}), 404

            (session
             .query(Board)
             .filter(Board.id == board_info['board_id'])
             .update({'is_deleted': board_info['is_deleted'], 'modifier': board_info['modifier']}))

            (session
             .query(Article)
             .filter(Article.board_id == board_info['board_id'])
             .update({'is_deleted': board_info['is_deleted'], 'modifier': board_info['modifier']}))

            session.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

    def make_article(self, article_info):
        article = Article()
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if session.query(Board.is_deleted).filter(Board.id == article_info['board_id']).one()[0]:
                return  jsonify({'message': 'BOARD_NOT_EXISTS'}), 404

            article.board_id = article_info['board_id']
            article.uploader = article_info['uploader']
            article.title = article_info['title']
            article.content = article_info['content']
            session.add(article)
            session.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

    def get_article_list(self, article_info):
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if session.query(Board.is_deleted).filter(Board.id == article_info['board_id']).one()[0]:
                return  jsonify({'message': 'BOARD_NOT_EXISTS'}), 404

            filter_list = [
                {'model': 'Article', 'field': 'is_deleted', 'op': '==', 'value': False},
                {'model': 'Article', 'field': 'board_id', 'op': '==', 'value': article_info['board_id']}
            ]
            if article_info.get('title', None):
                filter_list.append(
                    {'model': 'Article', 'field': 'title', 'op': 'like', 'value': '%' + article_info['title'] + '%'})
            if article_info.get('uploader', None):
                filter_list.append(
                    {'model': 'Article', 'field': 'uploader', 'op': 'like', 'value': '%' + article_info['uploader'] + '%'})

            article_query = (session
                .query(Article.id, Article.title, User.full_name, Article.create_at, Article.updated_at, Article.is_deleted)
                .join(User, User.id == Article.uploader))

            article_list = apply_filters(article_query, filter_list).order_by(Article.create_at.desc()).slice(article_info['offset'], article_info['limit']).all()

            articles = [{
                'id': article[0],
                'title': article[1],
                'author': article[2],
                'created_at': article[3],
                'updated_at': article[4],
                'is_deleted': article[5]
            } for article in article_list]
            return articles

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

    def get_article_detail(self, article_info):
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if session.query(Board.is_deleted).filter(Board.id == article_info['board_id']).one()[0]:
                return  jsonify({'message': 'BOARD_NOT_EXISTS'}), 404
            if session.query(Article.is_deleted).filter(Article.id == article_info['article_id']).one()[0]:
                return  jsonify({'message': 'ARTICLE_NOT_EXISTS'}), 404

            article_detail = (session
                .query(Article.title, Article.content, Article.create_at, Article.updated_at, User.full_name)
                .join(User, User.id == Article.uploader)
                .filter(Article.id == article_info['article_id'], Article.board_id == article_info['board_id'], Article.is_deleted == False)
                .one())

            article_detail = {
                'title': article_detail[0],
                'content': article_detail[1],
                'author': article_detail[4],
                'created_at': article_detail[2],
                'updated_at': article_detail[3],
            }
            return jsonify({'boards': article_detail}), 200

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

    def edit_article(self, article_info):
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            uploader_db = session.query(Article.uploader).filter(Article.id == article_info['article_id']).one()[0]
            if uploader_db != article_info['modifier']:
                return jsonify({'message': 'UNAUTHORIZED_ACTION'}), 403

            if session.query(Board.is_deleted).filter(Board.id == article_info['board_id']).one()[0]:
                return jsonify({'message': 'BOARD_NOT_EXISTS'}), 404
            if session.query(Article.is_deleted).filter(Article.id == article_info['article_id']).one()[0]:
                return  jsonify({'message': 'ARTICLE_NOT_EXISTS'}), 404

            (session
             .query(Article)
             .filter(Article.board_id == article_info['board_id'], Article.id == article_info['article_id'])
             .update({'title': article_info['new_title'], 'content': article_info['new_content'], 'modifier': article_info['modifier']}))

            session.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

    def delete_article(self, article_info):
        engine = get_db_connection()

        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            uploader_db = session.query(Article.uploader).filter(Article.id == article_info['article_id']).one()[0]
            if (uploader_db != article_info['modifier']) and (article_info['auth_type_id'] != 1):
                return jsonify({'message': 'UNAUTHORIZED_ACTION'}), 403

            if session.query(Board.is_deleted).filter(Board.id == article_info['board_id']).one()[0]:
                return jsonify({'message': 'BOARD_NOT_EXISTS'}), 404
            if session.query(Article.is_deleted).filter(Article.id == article_info['article_id']).one()[0]:
                return  jsonify({'message': 'ARTICLE_NOT_EXISTS'}), 404

            (session
             .query(Article)
             .filter(Article.id == article_info['article_id'])
             .update({'is_deleted': article_info['is_deleted'], 'modifier': article_info['modifier']}))

            session.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500