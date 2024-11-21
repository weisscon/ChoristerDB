from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from werkzeug.security import check_password_hash, generate_password_hash

from chorister_db.auth import login_required
from chorister_db.db import get_db
from chorister_db.db import get_users

bp = Blueprint('general', __name__)

@bp.route('/')
@login_required
def index():
    users = get_users()
    raw_permissions = users.execute(
        'SELECT permissionId'
        ' FROM allowed'
        ' WHERE accountID = ?',(g.user['accountId'],)
    ).fetchall()
    permissions = []
    for row in raw_permissions:
        permissions.append(row['permissionId'])
    return render_template('general/index.html', permissions = permissions)

@bp.route('/password-reset', methods=('GET', 'POST'))
@login_required
def reset_password():
    if request.method == 'POST':
        password = request.form['password']
        new_password = request.form['new_password']
        confirm_password = request.form['pass_confirm']
        error = None

        users = get_users()
        user = users.execute(
            'SELECT * FROM account WHERE accountId = ?',(g.user['accountId'],)
        ).fetchone()

        if not check_password_hash(user['password'], password):
            error = 'Previous password entered incorrectly'
        if new_password != confirm_password:
            error = 'New Password does not match confirmation'
        
        if error == None:
            try:
                users.execute(
                    'UPDATE account SET password = ? WHERE accountId = ?',
                    (generate_password_hash(new_password), g.user['accountId'],)
                )
                print('update completed')
                users.commit()
                flash('Password updated')
            except Exception as err:
                flash(err)
        else: 
            flash(error)
    
    return render_template('general/passwordreset.html')





