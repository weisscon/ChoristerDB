import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from chorister_db.db import get_db

bp = Blueprint('choristers', __name__, url_prefix='/choristers')

@bp.route('/members', methods=('GET', 'POST'))
def members():
    choristers = get_db()
    chorister = choristers.execute(
        'SELECT chorister.choristerId, chorister.firstName, chorister.lastName,\
        chorister.street1, chorister.street2, chorister.city, chorister.state,\
        chorister.zip, chorister.email, chorister.phone, chorister.sectionId,\
        chorister.statusId, section.sectionName, status.statusName FROM \
        chorister INNER JOIN section ON chorister.sectionId = section.sectionId \
        INNER JOIN status ON chorister.statusId=status.statusId'
    ).fetchall()

    return render_template('choristers/members.html', chorister=chorister)

@bp.route('/add_member', methods=('GET', 'POST'))
def add_member():

    choristers = get_db()

    if request.method=="POST":
        choristerId = request.form['choristerId'] #had to update this - originally had 'First Name' in the argument.
        firstName = request.form['First Name']
        lastName = request.form['Last Name']
        street1 = request.form['Street Address 1']
        street2 = request.form['Street Address 2']
        city = request.form['City']
        state = request.form['State']
        zip = request.form['ZIP Code']
        email = request.form['email']
        phone = request.form['Phone number']
        sectionId = request.form['Section ID']
        statusId = request.form['Status ID']
        try:
            choristers.execute(
                'INSERT INTO chorister (choristerId, firstName, lastName, street1, street2, city, state, zip, email, phone, sectionId, statusId)'
                 ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (choristerId, firstName, lastName, street1, street2, city, state, zip, email, phone, sectionId, statusId)
            )
            choristers.commit()
            flash("New chorister added")
        except Exception as err:
            flash(err)

    sections = choristers.execute("SELECT * FROM section").fetchall()
    statuses = choristers.execute("SELECT * FROM status").fetchall()

    return render_template('choristers/add_member.html', sections=sections, statuses=statuses) #, new_member=new_member <- took this out, since the member is created through the "POST" method.

    #   Took these two out, the actual singer just has the IDs.
    #    sectionName = request.form['Section name']
    #    statusName = request.form['Status']
'''        
        value_list = [choristerId, firstName, lastName, street1, street2, city,
        state, zip, email, phone, sectionId, statusId]
        value_statement = ', '.join(value_list)
        insert_statement = 'INSERT INTO chorister (choristerId, firstName, lastName, street1,\
            street2, city, state, zip, email, phone, sectionId, statusId) VALUES (' + value_statement + ')'
        print(insert_statement)
'''