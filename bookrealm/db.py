import csv
import os
import click

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import current_app
from flask.cli import with_appcontext
from bookrealm.queries import delete_tables, create_tables, insert_book


def get_db():
    database_url = os.environ['DATABASE_URL']
    engine = create_engine(database_url)

    db = scoped_session(sessionmaker(bind=engine))
    return db


def init_db():
    db = get_db()

    for query in delete_tables:
        db.execute(query)

    for query in create_tables:
        db.execute(query)

    """
    f = open("books.csv")
    reader = csv.reader(f, )
    print(next(reader, None))
    for isbn, title, author, year in reader:
        db.execute(insert_book,
                   {"isbn": isbn, "title": title,
                    "author": author, "year": int(year)})
    """
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.cli.add_command(init_db_command)
