# How to run
1. 프로젝트를 클론합니다
2. 가상환경을 만듭니다
3. pip install -r requirements.txt 명령어를 통해서 필요 라이브러리를 다운받습니다.
4. config.py 파일을 connection.py 파일과 같은 디렉토리에 생성해주고 아래와같은 config 내용을 넣습니다

         DATABASES = {
             'user': 'database_user_name',
             'password': 'database_password',
             'host': 'host',
             'port': 3306,
             'database': 'database_name',
         }

         REDIS = {
             'host': 'host',
             'port': 6379
         }

         SECRET = {
             'secret_key':'secret_key',
             'algorithm': 'HS256'
         }
5. alembic upgrade head 명령어를 실행해서 데이터베이스에 테이블을 생성합니다.
6. [API document](https://documenter.getpostman.com/view/10893095/SzmYA237?version=latest)를 참조해서 sign-up 부터 차례로 api를 호출할 수 있습니다.

# Project Introduction

Simple board and article create, read, update and delete project. 

+ Project Period  : 5 days

+ Member         : (back) Heechul Yoon
         

# Features
+ [POST] Sign-in and Sign-up features.
+ [POST] Log out feature.
+ [POST] Create board under the master authorization.
+ [GET] Display all board list.
+ [PUT] Edit board name under the master authorization.
+ [DELETE] Delete board under the master authorization.
+ [POST] Create an article in a board.
+ [GET] Display all articles in a board.
+ [PUT] Edit article title or contents belong to a user. 
+ [DELETE] Delete article belong to a user.
+ [GET] Display recent articles belong to boards.

# Technologies(Backend)
+ Python 3.8.0 : language
+ Flask 1.1.2  : web framework
+ Git          : cooperation and version management tool
+ Redis        : Caching database
+ PostgreSQL   : Database
+ Alembic      : migration tool
+ SQLalchemy   : ORM(Object Relational Mapping)
+ Bcrypt       : password hashing
+ JWT          : token generating

# API Documentation
+ [Boards & Articles](https://documenter.getpostman.com/view/10893095/SzmYA237?version=latest)

# Database Modeling
![ERD](https://media.vlpt.us/images/valentin123/post/c5035d26-634d-4fd4-8a05-c72f19d2c9cb/boards_and_articles.png)
