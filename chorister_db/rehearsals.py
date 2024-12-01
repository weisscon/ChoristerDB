import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from chorister_db.db import get_db

bp = Blueprint('rehearsals', __name__, url_prefix='/rehearsals')

@bp.route('/meetings', methods=('GET', 'POST'))
def meetings():
    rehearsals = get_db()
    rehearsal = rehearsals.execute(
        'SELECT * FROM rehearsal'
    ).fetchall()

    return render_template('rehearsals/meetings.html', rehearsal=rehearsal)

@bp.route('/add_meeting', methods=('GET', 'POST'))
def add_meeting():
    rehearsals = get_db()

    if request.method=="POST":
        rehearsalDate = request.form['rehearsalDate']

        print(rehearsalDate)

        try:
            rehearsals.execute(
                'INSERT INTO rehearsal (rehearsalDate)\
                VALUES (?)',
                (rehearsalDate,)
            )
            rehearsals.commit()
            flash("New rehearsal added")
        except Exception as err:
            flash(err)
        return redirect(url_for('rehearsals.meetings'))

    return render_template('rehearsals/add_meeting.html')    
