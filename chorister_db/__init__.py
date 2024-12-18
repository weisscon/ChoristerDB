import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'choristerdb.sqlite'),
        USERS=os.path.join(app.instance_path, 'dbusers.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Welcome to the choir attendance app'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import general
    app.register_blueprint(general.bp)
    app.add_url_rule('/', endpoint='index')

    from . import choristers
    app.register_blueprint(choristers.bp)

    from . import dbadmin
    app.register_blueprint(dbadmin.bp)

    from . import rehearsals
    app.register_blueprint(rehearsals.bp)

    from . import treasurer
    app.register_blueprint(treasurer.bp)

    return app