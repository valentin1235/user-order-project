from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASES

Base = declarative_base()
engine = create_engine(
    f'postgresql://{DATABASES["user"]}:{DATABASES["password"]}@{DATABASES["host"]}/{DATABASES["database"]}',
    echo=True
)


class AuthType(Base):
    __tablename__ = 'auth_types'

    id = Column('id', Integer(), primary_key=True, autoincrement=True, nullable=False)
    name = Column('name', String(10), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer(), primary_key=True, autoincrement=True, nullable=False)
    full_name = Column('full_name', String(15), nullable=False)
    email = Column('email', String(200), nullable=False)
    password = Column('password', String(300), nullable=False)
    auth_type_id = Column('auth_type_id', Integer(), ForeignKey('auth_types.id'), nullable=False)
    create_at = Column('created_at', DateTime(timezone=True), server_default=func.now())
    updated_at = Column('updated_at', DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column('is_deleted', Boolean(), default=False)


class RandomKey(Base):
    __tablename__ = 'random_keys'

    id = Column('id', Integer(), primary_key=True, autoincrement=True, nullable=False)
    key = Column('key', String(50), nullable=False)


