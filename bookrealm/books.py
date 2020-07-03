from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from bookrealm.auth import login_required
from bookrealm.db import get_db

bp = Blueprint('books', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    books = None
    if request.method == 'POST':
        query = request.form['query']
        db = get_db()
        books = db.execute(
            """
        SELECT *
        FROM books 
        WHERE LOWER(isbn) LIKE CONCAT('%',:query,'%')
        OR LOWER(title) LIKE CONCAT('%',:query,'%')
        OR LOWER(author) LIKE CONCAT('%',:query,'%')
        """, {"query": query}
        ).fetchall()
    return render_template('books/index.html', books=books)


@bp.route('/book/<int:id>', methods=('GET', 'POST'))
def book(id):
    db = get_db()

    if request.method == 'POST':
        body = request.form['body']
        rating = request.form['rating']

        error = None
        if db.execute("""
        SELECT * FROM reviews 
        WHERE user_id = :user_id and book_id = :book_id
        """, {"user_id": g.user[0], "book_id": id}).fetchone() is not None:
            error = "User {} already posted a review for this book".format(
                g.user
            )

        if error is None:
            db.execute("""
            INSERT INTO reviews (book_id, user_id, body, rating)
            VALUES (:book_id, :user_id, :body, :rating)
            """, {"book_id": id,
                  "user_id": g.user[0],
                  "body": body,
                  "rating": rating})
            db.commit()

    book_info = db.execute(
        """
        SELECT title, author, isbn, year
        FROM books
        WHERE id = :id
        """,
        {"id": id}
    ).fetchone()

    reviews = db.execute(
        """
        SELECT r.body AS body,
               r.created AS created,
               u.name AS name,
               r.rating AS rating
        FROM books b
        JOIN reviews r
        ON b.id = r.book_id
        JOIN users u
        ON r.user_id = u.id
        WHERE b.id = :id
        """,
        {"id": id}
    ).fetchall()

    return render_template('books/book.html',
                           book_info=book_info,
                           reviews=reviews)
