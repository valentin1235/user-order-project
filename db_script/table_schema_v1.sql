drop database user;

create database user character set utf8mb4 collate utf8mb4_general_ci;
use user;


-- auth_types Table Create SQL
CREATE TABLE auth_types
(
    `id`    INT           NOT NULL    AUTO_INCREMENT COMMENT 'PK', 
    `name`  VARCHAR(8)    NOT NULL    COMMENT '권한 종류 이름', 
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '권한 종류 테이블';


INSERT INTO auth_types
(
	id,
	name
) VALUES (
	1,
	'master'
),(
	2,
	'general'
);

-- genders Table Create SQL
CREATE TABLE genders
(
    `id`      INT           NOT NULL    AUTO_INCREMENT COMMENT 'PK', 
    `gender`  VARCHAR(15)   NOT NULL    COMMENT '성별', 
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '성별 테이블';


INSERT INTO genders
(
	id,
	gender
) VALUES (
	1,
	'male'
),(
	2,
	'female'
);

-- user_accounts Table Create SQL
CREATE TABLE user_accounts
(
    `id`            INT             NOT NULL    AUTO_INCREMENT COMMENT 'PK', 
    `email`         VARCHAR(100)    NOT NULL    UNIQUE COMMENT '로그인 이메일', 
    `password`      VARCHAR(80)     NOT NULL    COMMENT '로그인 비밀번호', 
    `auth_type_id`  INT             NULL        DEFAULT 2 COMMENT '유저 권한 타입 FK', 
    `is_deleted`    TINYINT         NULL        DEFAULT FALSE COMMENT '삭제여부', 
    `created_at`    DATETIME        NULL        DEFAULT CURRENT_TIMESTAMP COMMENT '생성일자', 
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '유저 로그인 어카운트 전용 테이블';


ALTER TABLE user_accounts
    ADD CONSTRAINT FK_user_accounts_auth_type_id_auth_types_id FOREIGN KEY (auth_type_id)
        REFERENCES auth_types (id) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- user_infos Table Create SQL
CREATE TABLE user_infos
(
    `id`               INT            NOT NULL    AUTO_INCREMENT COMMENT 'PK', 
    `name`             VARCHAR(20)    NOT NULL    COMMENT '이름', 
    `nick_name`        VARCHAR(30)    NOT NULL    UNIQUE COMMENT '별명', 
    `contact_number`   VARCHAR(20)    NOT NULL    COMMENT '전화번호', 
    `gender_id`        INT            NOT NULL    COMMENT '성별 FK', 
    `user_account_id`  INT            NOT NULL    COMMENT '유저 어카운트 FK', 
    `start_time`       DATETIME       NULL        DEFAULT CURRENT_TIMESTAMP COMMENT '선분이력 시작일시', 
    `close_time`       DATETIME       NULL        DEFAULT '2037-12-31 23:59:59' COMMENT '선분이력 종료일시', 
    `modifier`         INT            NULL        COMMENT '수정자 FK', 
    `is_deleted`       TINYINT        NULL        DEFAULT FALSE COMMENT '삭제여부', 
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '유저정보테이블';


ALTER TABLE user_infos
    ADD CONSTRAINT FK_user_infos_gender_id_genders_id FOREIGN KEY (gender_id)
        REFERENCES genders (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE user_infos
    ADD CONSTRAINT FK_user_infos_user_account_id_user_accounts_id FOREIGN KEY (user_account_id)
        REFERENCES user_accounts (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE user_infos
    ADD CONSTRAINT FK_user_infos_modifier_user_accounts_id FOREIGN KEY (modifier)
        REFERENCES user_accounts (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- products Table Create SQL
CREATE TABLE products
(
    `id`          INT            NOT NULL    AUTO_INCREMENT COMMENT 'PK', 
    `name`        VARCHAR(100)    NOT NULL    COMMENT '상품 이름', 
    `created_at`  DATETIME       NULL        DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '상품 테이블';

INSERT INTO products 
(
	id,
	name
	
) VALUES (
	1,
	'상품1'
), (
	2,
	'상품2'
), (
	3,
	'상품3'
), (
	4,
	'상품4'
), (
	5,
	'상품5'
), (
	6,
	'상품6'
), (
	7,
	'상품7'
), (
	8,
	'상품8'
), (
	9,
	'상품9'
);


-- carts Table Create SQL
CREATE TABLE carts
(
    `id`               INT         NOT NULL    AUTO_INCREMENT COMMENT 'PK', 
    `user_account_id`  INT         NOT NULL    COMMENT 'user FK', 
    `created_at`       DATETIME    NULL        DEFAULT CURRENT_TIMESTAMP COMMENT '결제일시', 
    `is_checked_out`   TINYINT     NULL        DEFAULT 0 COMMENT '장바구니 결제 여부',
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '장바구니';

ALTER TABLE carts
    ADD CONSTRAINT FK_carts_user_account_id_user_accounts_id FOREIGN KEY (user_account_id)
        REFERENCES user_accounts (id) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- orders Table Create SQL
CREATE TABLE orders
(
    `id`               INT         NOT NULL    AUTO_INCREMENT COMMENT 'PK', 
    `created_at`       DATETIME    NULL        DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시', 
    `cart_id`          INT         NOT NULL    COMMENT 'cart FK', 
    `product_id`       INT         NOT NULL    COMMENT 'product FK',
    `is_checked_out`   TINYINT     NULL        DEFAULT 0 COMMENT '장바구니 내 상품 결제 여부', 
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '상품하나의 주문을 담은 테이블';

ALTER TABLE orders
    ADD CONSTRAINT FK_orders_product_id_products_id FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE orders
    ADD CONSTRAINT FK_orders_cart_id_carts_id FOREIGN KEY (cart_id)
        REFERENCES carts (id) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- receipts Table Create SQL
CREATE TABLE receipts
(
    `id`            INT            NOT NULL    AUTO_INCREMENT COMMENT 'PK', 
    `cart_id`       INT            NOT NULL    COMMENT 'cart FK', 
    `order_number`  VARCHAR(45)    NOT NULL    COMMENT '주문번호', 
    `created_at`    DATETIME       NULL        DEFAULT CURRENT_TIMESTAMP COMMENT '결제일시', 
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '결제된 주문번호 관리';

ALTER TABLE receipts
    ADD CONSTRAINT FK_receipts_cart_id_carts_id FOREIGN KEY (cart_id)
        REFERENCES carts (id) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- master token 6days : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2FjY291bnRfaWQiOjEsImV4cCI6MTU4OTQzODM3MX0.vSHevnWPxXulMBL2Opjz_JdRe8gwJX2CA2G5syCQJpU
-- user1 token 6days : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2FjY291bnRfaWQiOjIsImV4cCI6MTU4OTQzODQ2M30.qn60pQdQnHELqXqb4WjrAh25_v208KkkIbDk4ir7I1M
-- user2 token 6days : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2FjY291bnRfaWQiOjMsImV4cCI6MTU4OTQzODUxN30.BFSHKF2udcMe5nR7ck7fZlIbl6rNWBtEfih6tjQLHIM
-- user3 token 6days : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2FjY291bnRfaWQiOjQsImV4cCI6MTU4OTQzODU1M30.p7m9Gl-HnUFhWiFCxMQSFuBqaZzAlOezwyqsAjiaCxo



