import pytest
from flask import template_rendered
from src.app.models import User, Task, db as _db
from src import create_app
from src.app.config import TestingConfig
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def app():
    _app = create_app(TestingConfig)

    with _app.app_context():
        _db.create_all()
        user = User(id=1, username='username', password='password')
        task = Task(user_id=1)

        _db.session.add(user)
        _db.session.add(task)

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


#@pytest.fixture
#def db(app):
 #   with app.app_context():
  #      yield _db