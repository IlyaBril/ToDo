import pytest
from flask import template_rendered
from app.models import (User, Task, db as _db)
from app import create_app
from app.config import TestingConfig


@pytest.fixture
def app():
    _app = create_app(TestingConfig)

    with _app.app_context():
        _db.create_all()
        user = User(id=1,
                    username='username',
                    password='password')

        task = Task(description='description',
                          category='category',
                          remind_date='2024-01-01')

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


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db