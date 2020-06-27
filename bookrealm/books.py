from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from bookrealm.auth import login_required
from bookrealm.db import get_db

bp = Blueprint('books', __name__)


@bp.route('/')
def index():
    return render_template('books/index.html')