from flask import (
    Blueprint, flash, g, redirect,
    render_template, request, url_for, jsonify
)

from werkzeug.exceptions import abort

from bookrealm.auth import login_required
from bookrealm.db import get_db
import requests, os

bp = Blueprint('books', __name__)
gr_key = os.environ['GR_KEY']


@bp.route('/', methods=('GET', 'POST'))
def index():
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
    else:
        db = get_db()
        books = db.execute(
            """
        SELECT *
        FROM books 
        ORDER BY year DESC
        LIMIT 20;
        """
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
            db.execute("""
            UPDATE reviews
            SET book_id = :book_id, 
                user_id = :user_id,
                body = :body,
                rating = :rating
            WHERE user_id = :user_id and book_id = :book_id
            """, {"book_id": id,
                  "user_id": g.user[0],
                  "body": body,
                  "rating": rating})
            db.commit()
        else:
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

    review_stats = db.execute(
        """
        SELECT COUNT(*) as count,
               ROUND(AVG(rating), 2) AS avg_rating
        from reviews
        WHERE book_id = :id
        """,
        {"id": id}
    ).fetchone()

    gr_book_info = requests.get("https://www.goodreads.com/book/review_counts.json",
                                params={"key": gr_key, "isbns": book_info['isbn']}).json()

    return render_template('books/book.html',
                           book_info=book_info,
                           reviews=reviews,
                           review_stats=review_stats,
                           gr_book_info=gr_book_info['books'][0])


@bp.route("/api/books/<string:isbn>")
def book_api(isbn):
    """Return info about a single book"""

    db = get_db()
    book_info = db.execute("""
    SELECT *
    FROM books
    WHERE isbn = :isbn;
    """, {"isbn": isbn}).fetchone()

    if book_info is None:
        return jsonify({"error": "Invalid ISBN or ISBN is not available"}), 404

    review_stats = db.execute(
            """
            SELECT COUNT(*) as count,
                   ROUND(AVG(rating), 2) AS avg_rating
            from reviews
            WHERE book_id = :id
            """,
            {"id": book_info['id']}
        ).fetchone()

    return jsonify({
        "title": book_info['title'],
        "author": book_info['author'],
        "year": book_info['year'],
        "isbn": isbn,
        "review_count": review_stats['count'],
        "average_score": float(review_stats['avg_rating'])
    })
