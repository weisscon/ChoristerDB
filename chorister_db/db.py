import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def init_db():
    db = get_db()

    with current_app.open_resource('choristerdb.sql') as f:
        db.executescript(f.read().decode('utf8'))

    
def init_users():
    users = get_users()

    with current_app.open_resource('dbusers.sql') as h:
        users.executescript(h.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    init_users()
    click.echo('Initialized admin accounts.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def get_users():
    if 'users' not in g:
        g.users = sqlite3.connect(
            current_app.config['USERS'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.users.row_factory = sqlite3.Row

    return g.users

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
    users = g.pop('users', None)

    if users is not None:
        users.close()