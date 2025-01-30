import json
import pytest
import logging
from sqlalchemy import func, select, update
from src.app.models import User, Task
from .conftest import _db
from flask import current_app, g

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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

    resp = client.post('/api/data', json={'id': '1',
                                  'description': 'description 2'
                                 })
    logger.info('task data {}'.format(resp))
    

    assert resp.status_code == 204
    g.user = 1

    resp = client.get("/api/data?search=description", )
    assert resp.status_code == 302
    assert resp.json == 'true'
