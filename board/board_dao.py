from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASES
from user.user_dao import User

Base = declarative_base()
engine = create_engine(f'postgresql://{DATABASES["user"]}:{DATABASES["password"]}@{DATABASES["host"]}/{DATABASES["database"]}', echo=True)


class Board(Base):
    __tablename__ = 'boards'

    id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
    uploader = Column('uploader', Integer(), ForeignKey(User.id), nullable=False)
    modifier = Column('modifier', Integer(), ForeignKey(User.id), nullable=True)
    name = Column('name', String(20), nullable=False)
    create_at = Column('created_at', DateTime(timezone=True), server_default=func.now())
    updated_at = Column('updated_at', DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column('is_deleted', Boolean(), default=False)


class Article(Base):
    __tablename__ = 'articles'

    id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
    board_id = Column(ForeignKey('boards.id'), nullable=False)
    uploader = Column('uploader', Integer(), ForeignKey(User.id), nullable=False)
    modifier = Column('modifier', Integer(), ForeignKey(User.id), nullable=True)
    title = Column('title', String(50), nullable=False)
    content = Column('content', Text(), nullable=False)
    create_at = Column('created_at', DateTime(timezone=True), server_default=func.now())
    updated_at = Column('updated_at', DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column('is_deleted', Boolean(), default=False)

# Base.metadata.create_all(bind=engine)


