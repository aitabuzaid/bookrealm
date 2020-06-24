delete_books = "DROP TABLE IF EXISTS books;"
delete_reviews = "DROP TABLE IF EXISTS reviews;"
delete_users = "DROP TABLE IF EXISTS users;"

create_books = """CREATE TABLE IF NOT EXISTS books (
id      SERIAL PRIMARY KEY,
isbn    VARCHAR NOT NULL,
title   VARCHAR NOT NULL,
author  VARCHAR NOT NULL,
year    INTEGER NOT NULL
);
"""

create_reviews = """CREATE TABLE reviews (
id      SERIAL PRIMARY KEY,
book_id INTEGER REFERENCES books,
user_id INTEGER REFERENCES users,
body    VARCHAR NOT NULL,
created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""

create_users = """CREATE TABLE users (
id       SERIAL PRIMARY KEY,
name     VARCHAR NOT NULL,
username VARCHAR NOT NULL,
password VARCHAR NOT NULL,
email    VARCHAR NOT NULL
);"""


insert_book = """INSERT INTO books (isbn, title, author, year)
                            VALUES (:isbn, :title, :author, :year)
"""

insert_user = """INSERT INTO users (name, username, password, email)
                            VALUES (:name, :username, :password, :email)
"""

copy_books = "COPY books FROM STDIN WITH (FORMAT CSV, HEADER TRUE,DELIMITER ',');"

delete_tables = [delete_users, delete_reviews]#, delete_books]
create_tables = [create_users, create_reviews]#, create_books]







