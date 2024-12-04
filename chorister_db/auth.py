import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from chorister_db.db import get_users

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        error = None
        user = users.execute(
            'SELECT * FROM account WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['accountId']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_users().execute(
            'SELECT * FROM account WHERE accountId = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def dbadmin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        permissions = get_users().execute(
            'SELECT * FROM allowed WHERE permissionId = 1 AND accountId = ?',
            (g.user['accountId'],)
        ).fetchone()
        if permissions is None:
            flash("You do not have permission to view this page.")
            return redirect(url_for('general.index'))
    
        return view(**kwargs)
    
    return wrapped_view

def choradmin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        permissions = get_users().execute(
            'SELECT * FROM allowed WHERE permissionId = 2 AND accountId = ?',
            (g.user['accountId'],)
        ).fetchone()
        if permissions is None:
            flash("You do not have permission to view this page.")
            return redirect(url_for('general.index'))
    
        return view(**kwargs)
    
    return wrapped_view

def attendadmin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        permissions = get_users().execute(
            'SELECT * FROM allowed WHERE permissionId = 3 AND accountId = ?',
            (g.user['accountId'],)
        ).fetchone()
        if permissions is None:
            flash("You do not have permission to view this page.")
            return redirect(url_for('general.index'))
    
        return view(**kwargs)
    
    return wrapped_view

def treasurer_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        permissions = get_users().execute(
            'SELECT * FROM allowed WHERE permissionId = 4 AND accountId = ?',
            (g.user['accountId'],)
        ).fetchone()
        if permissions is None:
            flash("You do not have permission to view this page.")
            return redirect(url_for('general.index'))
    
        return view(**kwargs)
    
    return wrapped_view

    
