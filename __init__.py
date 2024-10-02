import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    from .db import db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    # create and configure the app

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'todo.sqlite'),
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


    from . import db
    db.init_app(app)


    from . import auth
    app.register_blueprint(auth.bp)
    logger.info('auth bp registered')

    from . import todo
    app.register_blueprint(todo.todobp)
    logger.info('todo bp registered')


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app