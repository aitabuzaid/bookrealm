import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from queries import create_db, delete_db, copy_data, insert_row

database_url = os.environ['DATABASE_URL']
engine = create_engine(database_url)
db = scoped_session(sessionmaker(bind=engine))
conn = engine.raw_connection()
cur = conn.cursor()
file = open('books.csv')

#db.execute(delete_db)
def main():
    db.execute(delete_db)
    db.execute(create_db)

    """
    f = open("books.csv")
    reader = csv.reader(f, )
    print(next(reader,None))
    for isbn, title, author, year in reader:
        #print(year)
        db.execute(insert_row,
                   {"isbn": isbn, "title": title,
                    "author": author, "year": int(year)})
                    
    """
    #db.execute(copy_data)

    cur.copy_expert(copy_data, file)
    cur.commit()

    db.commit()

#


if __name__ == "__main__":
    main()