from .factories import UserFactory, TaskFactory
from app.models import Task, User


def test_create_user(client, db):
    user = ClientFactory()
    db.session.commit()
    assert user.id is not None
    assert len(db.session.query(User).all()) == 2


def test_create_task(client, db):
    task = TaskFactory()
    db.session.commit()
    assert task.id is not None
    assert len(db.session.query(Task).all()) == 2
