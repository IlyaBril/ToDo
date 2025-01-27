import json
import pytest
from sqlalchemy import func, select, update
from app.models import User, Task
from .conftest import _db
from flask import current_app


def test_math_route(client) -> None:
    resp = client.get("/test_route?number=8")
    data = json.loads(resp.data.decode())
    assert data == 64


def test_app_config(app):
    assert not app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == "sqlite://"



def test_add_task(client):
    """Создание задачи"""

    client.post('/api/data', data={'user_id': 1,
                                  'description': 'description 2',
                                 })

    resp = client.get("/api/data")
    assert resp.status_code == 200
    #assert resp.json == {'user_id': 1,
     #                             'description': 'description 2',}
