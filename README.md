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
