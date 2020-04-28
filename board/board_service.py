from flask import jsonify, g
from .board_dao import engine, Board, Article
from user.user_dao import User
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker


class BoardService:
    def make_board(self, board_info):
        board = Board()
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            board.uploader = board_info['uploader']
            board.name = board_info['name']
            session.add(board)
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

    def get_board_list(self):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            board_list = session.query(Board.id, Board.name, Board.uploader, Board.create_at).filter(Board.is_deleted == False).all()
            boards = [{
                    'id': board[0],
                    'name': board[1],
                    'uploader': board[2],
                    'created_at': board[3]
                } for board in board_list]

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

        return jsonify({'boards': boards}), 200

    def edit_board(self, board_info):
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

    def delete_board(self, board_info):
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

    def make_article(self, article_info):
        article = Article()
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

    def get_article_list(self, board_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if session.query(Board.is_deleted).filter(Board.id == board_id).one()[0]:
                return  jsonify({'message': 'BOARD_NOT_EXISTS'}), 404

            article_list = (session
                            .query(Article.id, Article.title, Article.create_at, User.full_name)
                            .join(User, User.id == Article.uploader)
                            .filter(Article.board_id == board_id, Article.is_deleted == False)
                            .order_by(Article.create_at.asc())
                            .all())

            articles = [{
                    'id': article[0],
                    'title': article[1],
                    'created_at': article[2],
                    'author': article[3]
                } for article in article_list]

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

        return jsonify({'boards': articles}), 200

    def get_article_detail(self, article_info):
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

        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500

        finally:
            try:
                session.close()
            except Exception as e:
                print(e)
                return jsonify({'message': 'SESSION_CLOSE_ERROR'}), 500

        return jsonify({'boards': article_detail}), 200

    def edit_article(self, article_info):
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
             .filter(Article.board_id == article_info['board_id'], Article.id == article_info['article_id'])
             .update({'title': article_info['new_title'], 'content': article_info['new_content'], 'modifier': article_info['modifier']}))

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

    def delete_article(self, article_info):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            print(article_info)
            uploader_db = session.query(Article.uploader).filter(Article.id == article_info['article_id']).one()[0]
            print(uploader_db)
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