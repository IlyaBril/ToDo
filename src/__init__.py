import os
import logging
from flask import Flask
from .app.config import DevelopmentConfig
from .app.todo import first_row_check

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')

def create_app(mode=None):
    app = Flask(__name__)
    DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    if mode is None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(mode)

    from .app.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
        #first_row_check(db)
       

    from .app import auth
    app.register_blueprint(auth.bp)
    logger.info('auth bp registered')

    from .app import todo
    app.register_blueprint(todo.todobp)
    logger.info('todo bp registered')

    

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
