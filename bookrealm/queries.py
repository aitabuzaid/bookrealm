delete_db = "DROP TABLE IF EXISTS books ;"

create_db = """CREATE TABLE IF NOT EXISTS books (
id      SERIAL PRIMARY KEY,
isbn    VARCHAR NOT NULL,
title   VARCHAR NOT NULL,
author  VARCHAR NOT NULL,
year    INTEGER NOT NULL
);
"""

insert_row = """INSERT INTO books (isbn, title, author, year)
                            VALUES (:isbn, :title, :author, :year)
"""

copy_data = "COPY books FROM STDIN WITH (FORMAT CSV, HEADER TRUE,DELIMITER ',');"
