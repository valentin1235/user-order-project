from flask import jsonify, g
from .board_dao import engine, Board
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker


class BoardService:
    def make_board(self, board_info):
        board = Board()
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if session.query(exists().where(Board.name == board_info['name'])).one()[0]:
                return jsonify({'message': 'DUPLICATE_NAME'}), 400

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

            if session.query(exists().where(Board.name == board_info['new_name'])).one()[0]:
                return jsonify({'message': 'DUPLICATE_NAME'}), 400

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

            (session
             .query(Board)
             .filter(Board.id == board_info['board_id'])
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