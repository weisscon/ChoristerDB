import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from chorister_db.db import get_users

bp = Blueprint('dbadmin', __name__, url_prefix='/users')

@bp.route('/user_management')
def useradmin():
    usersdb = get_users()
    users = usersdb.execute(
        'SELECT * FROM account'
    ).fetchall()

    return render_template('dbadmin/useradmin.html', users = users)

@bp.route('/reset_forgot')
def reset_forgot():
    print("Not yet implemented")
    return redirect(url_for('index'))

@bp.route('/set_permissions')
def set_permissions():
    print('Not yet implemented')
    return redirect(url_for('index'))

@bp.route('/add_user')
def add_user():
    print("Not yet implemented")
    return redirect(url_for('index'))
