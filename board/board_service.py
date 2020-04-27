from flask import jsonify, g
from .board_dao import engine, Board
from sqlalchemy.orm import sessionmaker


class BoardService:
    def make_board(self, request):
        data = request.json
        board = Board()
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            board.full_name = data['full_name']
            board.email = data['email']
            board.password = data['password']
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
