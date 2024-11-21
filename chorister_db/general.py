from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

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