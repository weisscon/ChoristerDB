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
    choristerId = 
    firstName = 
    l
