from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from werkzeug.security import check_password_hash, generate_password_hash

from chorister_db.auth import login_required
from chorister_db.db import get_db
from chorister_db.db import get_users

bp = Blueprint('treasurer', __name__, url_prefix="/treasurer")

@bp.route('/addpayment', methods=("GET","POST"))
def addpayment():
    db = get_db()

    methods = db.execute(
        'SELECT * FROM paymentmethod'
    ).fetchall()

    if request.method == "POST":
        chorId = request.form['choristerId']
        method = request.form['methodId']
        amount = request.form['amount']

        '''
        validation = db.execute('SELECT choristerId FROM chorister WHERE )
        '''

        try:
            db.execute(
                'INSERT INTO payment (choristerId, methodId, amount) VALUES (?, ?, ?)',
                (chorId, method, amount,)
            )
            db.commit()
            flash("Payment added.")
        except Exception as error:
            flash(error)
    
    return render_template('treasurer/addpayment.html', methods = methods)

@bp.route('/reviewmember', methods=("GET","POST"))
def reviewmemberlanding():
    if request.method=="POST":
        return redirect(url_for("treasurer.reviewmember", choristerId = request.form['choristerId']))
    return render_template('treasurer/reviewmember.html', member = None, payments = None)

@bp.route('/<choristerId>/reviewmember')
def reviewmember(choristerId):
    
    member = None
    payments = None
    
    db = get_db()

    member = db.execute(
        'SELECT * FROM chorister WHERE choristerId = ?',
        (choristerId,)
    ).fetchone()

    payments = db.execute(
        'SELECT p.paymentId, p.amount, pm.methodDescription, m.month, m.year'
        ' FROM payment as p JOIN paymentmethod as pm ON p.methodId = pm.methodId'
        ' LEFT JOIN paymentmonth ON p.paymentId = paymentmonth.paymentId'
        ' LEFT JOIN month as m on paymentmonth.monthId =m.monthId'
        ' WHERE p.choristerId = ?',
        (choristerId,)
    ).fetchall()

    return render_template('treasurer/reviewmember.html', member = member, payments = payments)

@bp.route('/paymentmonths/<int:paymentId>', methods=("GET", "POST"))
def paymentmonths(paymentId):
    db = get_db()

    if request.method == "POST":
        monthId = db.execute('SELECT monthId from month WHERE month = ? AND year = ?', (request.form['month'], request.form['year'],)).fetchone()
        while not monthId:
            prev_max = db.execute('SELECT * from month ORDER BY monthId DESC LIMIT 1').fetchone()
            next_month = prev_max['month']+1
            next_year = prev_max['year']
            if next_month > 12: 
                next_month = next_month - 12
                next_year = next_year + 1
            try:
                db.execute(
                    'INSERT INTO month(month, year) VALUES (?, ?)',
                    (next_month, next_year,)
                )
                db.commit()
            except Exception:
                flash("Fatal Month Error")
                break
            monthId = db.execute('SELECT monthId from month WHERE month = ? AND year = ?', (request.form['month'], request.form['year'],)).fetchone()
        try:
            db.execute(
                'INSERT INTO paymentmonth(paymentId, monthId) VALUES (?, ?)',
                (paymentId, monthId['monthId'],)
            )
            db.commit()
            flash("Payment applied to month")
        except Exception as error:
            flash(error)
        
    paymonths = db.execute(
        'SELECT p.paymentId, p.choristerId, p.amount, pm.methodDescription, m.month, m.year'
        ' FROM payment as p JOIN paymentmethod as pm ON p.methodId = pm.methodId'
        ' LEFT JOIN paymentmonth ON p.paymentId = paymentmonth.paymentId'
        ' JOIN month as m on paymentmonth.monthId =m.monthId'
        ' WHERE p.paymentId = ?',
        (paymentId,)
    ).fetchall()
    
    return render_template('treasurer/paymentmonths.html', paymonths = paymonths)

@bp.route('/reviewmonth', methods=("GET","POST"))
def reviewmonthlanding():
    if request.method == 'POST':
        db = get_db()
        monthId = db.execute('SELECT monthId from month WHERE month = ? AND year = ?', (request.form['month'], request.form['year'],)).fetchone()
        try:
            return redirect(url_for('treasurer.reviewmonth', monthId = monthId['monthId']))
        except Exception:
            flash("Month error")

    return render_template('treasurer/reviewmonth.html', payments = None)

@bp.route('/<int:monthId>/reviewmonth')
def reviewmonth(monthId):
    db = get_db()

    payments = db.execute(
        'SELECT p.paymentId, c.choristerId, c.firstName, c.lastName, p.amount, pm.methodDescription'
        ' FROM payment as p, chorister as c, paymentmethod as pm, paymentmonth'
        ' WHERE p.choristerId = c.choristerId'
        ' AND p.methodId = pm.methodId'
        ' AND p.paymentId = paymentmonth.paymentId'
        ' AND paymentmonth.monthId = ?'
        ' ORDER BY c.lastName',
        (monthId,)
    ).fetchall()

    return render_template('treasurer/reviewmonth.html', payments = payments)