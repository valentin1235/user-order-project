from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



def get_db_connection():
    # base = declarative_base()
    engine = create_engine('postgresql://heechul:va1467@localhost/elice', echo=True)
    return engine
