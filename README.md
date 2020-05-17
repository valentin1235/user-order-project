# How to run
 1. 프로젝트를 클론합니다 
> 1. Clone the project
2. 가상환경을 만듭니다(작성자는 pycharm venv 사용) 
> 2. Create virtual environment(this project was made under the pycharm venv)

3. 가상환경 안에서 pip install -r requirements.txt 명령어를 통해서 필요 라이브러리를 다운받습니다. 또는 docker pull valentin1235/my_image:0.1 를 통해서 docker 이미지를 가져옵니다. 
> 3. download required library through 'pip install -r requirements.txt' or you can import an image through 'docker pull valentin1235/my_image:0.1' commandline

4. docker 이미지를 pull 한 경우 sudo docker run -d -p 5000:5000 valentin1235/my_image:0.1 (리눅스 한정)명령어를 통해서 컨테이너를 만듭니다.
> 4. If you are about to run the project via dockr, you want to create container based on the imported image. follow the command below
sudo docker run -d -p 5000:5000 valentin1235/my_image:0.1

5. config.py 파일을 connection.py 파일과 같은 디렉토리에 생성해주고 아래와같은 config 내용을 넣습니다(이프로젝트는 mysql을 데이터베이스로 사용하고 redis를 세션 저장공간으로 사용합니다)
> 5. create config.py at the same dicrectory as connection.py and put the content as followed(in order to run the project, mysql for database and redis for caching database are required)

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
         
6. [API document](https://documenter.getpostman.com/view/10893095/SzmfYHBu?version=latest)를 참조해서 sign-up 부터 차례로 api를 호출할 수 있습니다.
> 6. You could check the [API document](https://documenter.getpostman.com/view/10893095/SzmfYHBu?version=latest) as a description of the API



# Project Introduction
##### [프로젝트 후기](https://velog.io/@valentin123/Project5-About-User-Order-Project)


Simple user management and product order project. 

+ Project Period  : 2020.05.04 - 2020.05.10

+ Member         : (backend) Heechul Yoon
         

# Function Description
[프로젝트 설계]
+ model, service, view 레이어 간 의존성 설정 
+ 데이터베이스 모델링(aquery tools 사용)   
+ 초기 데이이터베이스 스크립트 생성 : 테이블, 외래키 관계, 기초 데이터 생성    
+ pycharm venv를 사용한 가상환경 설정(python3.8)
+ .gitignore 파일 생성
+ model : 데이터베이스와 통신
+ service : 비지니스 로직 
+ view : url 라우팅(블루프린트 사용) 및 유효성 검사
+ utils.py : 토큰 확인 데코레이터
+ config.py : 데이터베이스와 레디스 정보
+ connection.py :데이터베이스와 레디스 커넥션 관리
+ app.py : 플라스크 앱 생성 및 블루프린트 중앙 라우팅, jsonEncoder를 사용해서 datetime 리턴 형식 설정
+ manage.py : 프로젝트 실행
+ requirements.txt : 환경 공유
+ Dockerfile 을 통해서 이미지 생성

[회원가입]
+ json body 유효성검사
+ 마스터 권한부여는 데이터베이스에서 raw query로 업데이트
+ 이메일 및 닉네임 중복체크
+ 패스워드 bcrypt 암호화
+ 유저정보는 선분이력을 사용하기 때문에 어카운트 로그인정보 등록 후 유저정보 등록
+ 회원가입 성공 시 redis 접근 키 리턴
+ 토큰을 redis 저장공간에 key-vale 형태로 저장성

[로그인]
+ 이메일과 패스워드를 받아서 로그인
+ 데이터베이스에 있는 유저 정보와 input 정보 비교(bcrypt.checkpw 사용)
+ 로그인 성공 시 redis 접근 키 리턴
+ 토큰을 redis 저장공간에 key-vale 형태로 저장성

[토큰 확인 데코레이터]
+ header에서 가져온 토큰을 decode
+ 해당유저의 id를 가지고 데이터베이스에 권한정보, 존재여부, 삭제여부 확인
+ 토큰을 decode해서 나온 유저가 존재하면 flask g객체에 유저번호와 권한타입아이디를 저장

[로그아웃]
+ key를 json body로 받음
+ 받은 key를 redis에서 삭제

[유저 리스트 표출]
+ 마스터권한을 가진 유저가 유저 리스트와 유저의 최근 주문 내역 열람 가능(권한타입 유효성 검사)
+ 검색 키워드와 pagination을 위한 offset과 limit을 쿼리파라미터로 받음
+ 선분이력상 close_time이 2037-12-31(가장 최근정보에 해당됨)인 유저정보를 가져옴
+ 검색키워드가 들어오면 like를 사용해서 문자열이 하나라도 포함되면 값을 가져오도록 검색 구현
+ 전체중 몇명의 유저가 검색되었는지 확인하기 위해서 키워드로 필터된 유저 수와 전체유저 수를 같이 리턴


[유저 상세 정보 표출]
+ 마스터 권한으로 확인하고자 하는 유저의 id를 쿼리파라미터에 넣어서 요청
+ 권한 타입 유효성 검사
+ 선분이력상 close_time이 2037-12-31인 유저정보(가장 최근 이력에 해당되기 때문)를 가져옴
+ 유저의 가장 최근 주문내역 표출

[상품 리스트 표출]
+ 등록된 상품 리스트 표출
+ pagination : offset과 limit을 쿼리파라미터로 받아서 상품 표출, limit이 5000이상이면 애러리턴

[상품 상세정보 표출]
+ 하나의 상품의 상세정보 표출

[장바구니에 상품 추가]
+ 유저정보를 확인하고 해당유저의 장바구니가 없는 상태면 만들고 상품을 추가함(있으면 있는 장바구니에 추가)
+ 추가하고자 하는 상품 번호를 path parameter로 받음
+ check out(결제)되지 않은 장바구니에 상품을 추가함

[내 장바구니 표출]
+ 특정 유저의 장바구니를 표출해줌
+ 추가된 상품을 pagination 해서 보여줌
+ 토큰을 확인해서 누구의 장바구니인지 확인
+ 상품을 count하기 위해서 상품 id를 기준으로 group by해줌
+ 하나의 그룹에서 가져와야 하는 값이 하나여야 하기 때문에 서브쿼리에 limit을 1로 줘서 값을 하나만 가져옴
+ 하나의 그룹에 있는 상품의 갯수를 count하는 서브쿼리 사용

[장바구니에서 상품 삭제]
+ 장바구니에서 하나의 상품의 갯수에 상관없이 상품을 삭제함
+ order 테이블에서 cart_id를 가져오기 위해 서브쿼리 사용

[장바구니 갯수 수정]
+ 하나의 상품의 갯수를 줄일 때 사용(올릴때는 장바구니에 상품추가 기능 사용)
+ 같은 테이블의 경우 select delete 서브쿼리가 안되기 때문에 갯수를 줄이고자 하는 상품의 order 번호를 먼저 가져옴
+ 가장 최근 order 번호부터 순서대로 삭제

[주문서 생성(장바구니 상품 주문 기능)]
+ my-cart를 통해서 얻은 cart_id를 POST해서 해당 장바구니의 상태를 check out으로 바꿈
+ check out으로 바뀐 장바구니의 주문 명세서를 생성함(주문번호는 uuid로 생성)
+ 생성된 주문 명세서 번호, check out 한 장바구니 번호를 리턴


[주문서 표출]
+ 주문서를 생성하고 받은 명세서 번호와 장바구니 번호를 쿼리파라미터로 보냄
+ 유효성 검사 : 해당 주문명세서 번호, 장바구니 번호와 그것을 생성한 유저번호에 해당하는 주문명세서 번호가 없으면 404 리턴
+ is_checked_out 컬럼이 1인 장바구니의 상품목록과 해당 상품의 갯수를 가져옴


# API
+ [POST] Sign-in and Sign-up features.
+ [POST] Log out feature.
+ [GET] Show all user list with recent order information under the master authorization.
+ [GET] Show user detail with recent order detail under the master authorization.
+ [GET] Show my page to check my personal information.
+ [GET] Display all products.
+ [GET] Display picked product detail.
+ [POST] Add the product to my cart.
+ [DELETE] Delete the added product from my cart regardless of units. 
+ [PUT] Take the unit out of the added item .
+ [POST] Check out my cart.
+ [GET] Show my order receipt

# Technologies(Backend)
+ Python 3.8.0 : language
+ Pycharm venv : virtual environment
+ Docker       : image & container
+ Flask 1.1.2  : web framework
+ Git          : cooperation and version management tool
+ Redis        : Caching database
+ MySQL        : Database
+ Pymysql      : Database connection
+ Bcrypt       : password hashing
+ JWT          : token generating

# API Documentation
+ [User & Order](https://documenter.getpostman.com/view/10893095/SzmfYHBu?version=latest)

# Database Modeling
![ERD](https://brandi-intern.s3.ap-northeast-2.amazonaws.com/user%26order_modeling.png)
