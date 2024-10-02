import sqlite3
import logging

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        logger.info('current {}'.format(current_app.config['DATABASE']))
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
  db = get_db()

  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo('Initialized the database.')


def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase
#
# class Base(DeclarativeBase):
#   pass
#
# db = SQLAlchemy(model_class=Base)