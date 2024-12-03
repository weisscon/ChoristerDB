from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash

from chorister_db.db import get_users, get_db

bp = Blueprint('dbadmin', __name__, url_prefix='/users')

@bp.route('/user_management')
def useradmin():
    usersdb = get_users()
    users = usersdb.execute(
        'SELECT * FROM account'
    ).fetchall()

    return render_template('dbadmin/useradmin.html', users = users)

@bp.route('/reset_forgot/<int:userId>', methods=('GET', 'POST'))
def reset_forgot(userId):
    users = get_users()

    user = users.execute(
        'SELECT * FROM account WHERE accountId = ?',
        (userId,)
    ).fetchone()
    
    if request.method == "POST":
        password = request.form['password']    
        try:
            users.execute(
                'UPDATE account SET password = ? WHERE accountId = ?',
                (generate_password_hash(password), userId,)
            )
            users.execute(
                'UPDATE account SET userset = \'0\' WHERE accountId=?',
                (userId,)
            )
            users.commit()
            flash("Password update.  Notify the user of new password and instruct them to change it on login.")
        except Exception as error:
            flash(error)

    return render_template('dbadmin/reset_forgot.html', user = user)

@bp.route('/set_permissions/<int:userId>')
def set_permissions(userId):

    userdb = get_users()

    permissionList = userdb.execute(
        'SELECT * FROM permissions'
    ).fetchall()

    allowed = userdb.execute(
        'SELECT * FROM allowed WHERE accountid = ?',
        (userId,)
    ).fetchall()

    permissions = []

    for permission in permissionList:
        present = 0
        for allowance in allowed:
            if allowance['permissionId'] == permission['permissionId']:
                present = 1
        permissions.append([permission['permissionId'], permission['permissionDesc'], present])

    user = userdb.execute(
        'SELECT * FROM account WHERE accountId = ?',
        (userId,)
    ).fetchone()

    return render_template('dbadmin/set_permissions.html', permissions = permissions, user = user)

@bp.route('/remove_permission/<int:permissionId>/<int:userId>')
def remove_permission(permissionId, userId):
    userdb = get_users()

    userdb.execute(
        'DELETE FROM allowed WHERE accountId = ? and permissionId = ?',
        (userId, permissionId,)
    )
    userdb.commit()

    return redirect(url_for('dbadmin.set_permissions', userId = userId))
    

@bp.route('/add_permission/<int:permissionId>/<int:userId>')
def add_permission(permissionId, userId):
    userdb = get_users()

    userdb.execute(
        'INSERT INTO allowed (accountId, permissionId) VALUES(?, ?)',
        (userId, permissionId,)
    )
    userdb.commit()
    
    return redirect(url_for('dbadmin.set_permissions', userId = userId))


@bp.route('/add_user', methods=('GET','POST'))
def add_user():
    if request.method=='POST':
        users = get_users()
        username = request.form['username']
        password = request.form['password']

        try:
            users.execute(
                'INSERT INTO account(username, password, userset) VALUES (?, ?, 0)',
                (username, generate_password_hash(password))
            )
            users.commit()
            flash("New user created.  Make sure to update permissions and get user to update password on login.")
        except Exception as error:
            flash(error)

    return render_template('dbadmin/add_user.html')

@bp.route('/delete_user/<int:userId>', methods=('GET','POST'))
def delete_user(userId):
    users = get_users()

    users.execute(
        'DELETE FROM account WHERE accountId=?',
        (userId,)
    )
    users.commit()
    flash("The user has been deleted from the list of DB users")
    
    #return render_template('dbadmin/delete_user.html', userId = userId)
    return redirect(url_for('dbadmin.useradmin'))

@bp.route('/add_values')
def add_values():
    db = get_db()

    sections = db.execute(
        'SELECT * FROM section'
    ).fetchall()

    statuses = db.execute(
        'SELECT * FROM status'
    ).fetchall()

    payment_methods = db.execute(
        'SELECT * FROM paymentmethod'
    ).fetchall()

    attendance = db.execute(
        'SELECT * FROM attendancestatus'
    ).fetchall()

    return render_template('dbadmin/add_values.html', sections = sections, statuses = statuses, payment_methods = payment_methods, attendance = attendance)

@ bp.route('/update_sections', methods=['POST'])
def update_sections():
    new_section = request.form['new_section']
    
    db = get_db()

    db.execute(
        'INSERT INTO section(sectionName) VALUES (?)',
        (new_section,)
    )

    db.commit()

    return redirect(url_for('dbadmin.add_values'))

@ bp.route('/update_statuses', methods=['POST'])
def update_statuses():
    new_status = request.form['new_status']
    
    db = get_db()

    db.execute(
        'INSERT INTO status(statusName) VALUES (?)',
        (new_status,)
    )

    db.commit()

    return redirect(url_for('dbadmin.add_values'))

@ bp.route('/update_paymethods', methods=['POST'])
def update_paymethods():
    new_method = request.form['new_method']
    
    db = get_db()

    db.execute(
        'INSERT INTO paymentmethod(methodDescription) VALUES (?)',
        (new_method,)
    )

    db.commit()

    return redirect(url_for('dbadmin.add_values'))

@ bp.route('/update_attendance', methods=['POST'])
def update_attendance():
    new_attendance = request.form['new_attendance']
    
    db = get_db()

    db.execute(
        'INSERT INTO attendancestatus(attendanceStatus) VALUES (?)',
        (new_attendance,)
    )

    db.commit()

    return redirect(url_for('dbadmin.add_values'))