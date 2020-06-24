import functools
from bookrealm.queries import insert_user

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from bookrealm.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        if not username:
            error = 'Please select a username.'
        elif not password:
            error = 'Please select a password.'
        elif db.execute(
                'SELECT id FROM users WHERE username = :username',
                {"username": username}).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                insert_user, {'name': name,
                              'username': username,
                              'password': password,
                              'email': email}
            )
            db.commit()

        flash(error)
    return render_template('auth/register.html')
