import factory
import factory.fuzzy as fuzzy
import random

from src.app.models import db
from src.app.models import User, Task


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    username = factory.Faker('name')
    password = 'password'


class TaskFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Task
        sqlalchemy_session = db.session

    description = factory.Faker('sentence', nb_words=2)
