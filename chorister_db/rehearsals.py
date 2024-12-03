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
        'SELECT * FROM rehearsal ORDER BY rehearsalId DESC'
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

@bp.route('/startattendance/<int:rehearsalId>', methods=("GET","POST"))
def startattendance(rehearsalId):
    db = get_db()
    rehearsalDate = db.execute(
        'SELECT rehearsalDate FROM rehearsal WHERE rehearsalId = ?',
        (rehearsalId,)
    ).fetchone()
    attendanceStatuses = db.execute(
        'SELECT * FROM attendancestatus'
    ).fetchall()
    if request.method == "POST":
        if request.form['section'] == "Soprano":
            section1 = 1
            section2 = 2
        elif request.form['section'] == "Alto":
            section1 = 3
            section2 = 4
        elif request.form['section'] == "Tenor":
            section1 = 5
            section2 = 6
        elif request.form['section'] == "Bass":
            section1 = 7
            section2 = 8
        members = db.execute(
            'SELECT * FROM chorister WHERE (sectionId = ? OR sectionId = ?) AND statusId = 1 ORDER BY chorister.lastName',
            (section1, section2)
        ).fetchall()
        existing_data = db.execute(
            'SELECT attends.choristerId '
            ' FROM attends JOIN chorister ON attends.choristerId = chorister.choristerId'
            ' WHERE attends.rehearsalId = ?' 
            ' AND (chorister.sectionId = ? OR chorister.sectionId = ?)',
            (rehearsalId, section1, section2,)
        ).fetchall()
        if existing_data:
            flash("Attendance has already been taken for this section for this rehearsal.  Retaking attendance will overwrite previous data.")

        return render_template('rehearsals/take_attendance.html', rehearsalId=rehearsalId, attendanceStatuses = attendanceStatuses, rehearsalDate = rehearsalDate, members = members)
    
    return render_template('rehearsals/take_attendance.html', rehearsalId=rehearsalId, attendanceStatuses = attendanceStatuses, rehearsalDate = rehearsalDate, members = None)

@bp.route('/takeattendance/<int:rehearsalId>', methods=("GET","POST"))
def takeattendance(rehearsalId):
    db = get_db()
    for entry in request.form.to_dict():
        db.execute(
            'INSERT INTO attends (choristerId, rehearsalId, attendanceId) VALUES (?, ?, ?)',
            (entry, rehearsalId, request.form[entry][1],)
        )
    db.commit()
    return redirect(url_for('rehearsals.meetings'))

@bp.route('/reviewattendance/<int:rehearsalId>', methods=("GET","POST"))
def reviewattendance(rehearsalId):
    db = get_db()
    attendees = db.execute(
        'SELECT attends.choristerId, attends.attendanceId, attendancestatus.attendanceStatus, chorister.firstName, chorister.lastName\
        FROM attends\
        LEFT JOIN chorister ON attends.choristerId = chorister.choristerId\
        LEFT JOIN rehearsal ON attends.rehearsalId=rehearsal.rehearsalId\
        LEFT JOIN attendancestatus ON attends.attendanceId=attendancestatus.attendanceId\
        WHERE attends.rehearsalId=?',
        (rehearsalId,)
    ).fetchall()
    statuses = db.execute(
        'SELECT * FROM attendancestatus'
    ).fetchall()
    rehearsalDate = db.execute(
        'SELECT rehearsalDate FROM rehearsal WHERE rehearsalId = ?', (rehearsalId,)
    ).fetchone()
    #return redirect(url_for('rehearsals.meetings'))
    return render_template('rehearsals/review_attendance.html', attendees=attendees, statuses=statuses, rehearsalId=rehearsalId, rehearsalDate=rehearsalDate)


@bp.route('/updateattendance/<int:rehearsalId>', methods=("GET","POST"))
def updateattendance(rehearsalId):
    db = get_db()
    db.execute(
        'UPDATE attends'
        ' SET attendanceId = ?'
        ' WHERE rehearsalId = ? AND choristerId = ?',
        (request.form['statusId'], rehearsalId, request.form['ctrl'],)
    )
    db.commit()
    
    return redirect(url_for('rehearsals.reviewattendance', rehearsalId=rehearsalId))

@bp.route('/addattendance/<int:rehearsalId>', methods=("GET","POST"))
def addattendance(rehearsalId):
    print(request.form['choristerId'])
    db = get_db()
    chorister = db.execute(
        'SELECT choristerId from chorister WHERE choristerId = ?', (request.form['choristerId'],)
    ).fetchone()
    if chorister:
        db.execute(
            'INSERT INTO attends(choristerId, rehearsalId, attendanceId) VALUES (?, ?, ?)',
            (request.form['choristerId'], rehearsalId, request.form['statusId'])
        )
        db.commit()
    else:
        flash("Entered ID does not match any existing chorister.")

    return redirect(url_for('rehearsals.reviewattendance', rehearsalId=rehearsalId))