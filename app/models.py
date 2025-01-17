from datetime import date
import logging

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import select, func
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, relationship
from sqlalchemy.ext.hybrid import hybrid_property

class Base(DeclarativeBase, MappedAsDataclass):
  pass

db = SQLAlchemy(model_class=Base)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(64), index=True)

    task_relation = relationship("Task", back_populates="user_relation")

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), index=True)
    category = db.Column(db.String(64), index=True)
    responsible = db.Column(db.String(64))
    remind_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    finish_date = db.Column(db.Date)
    remark = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  
    user_relation =  relationship("User", back_populates="task_relation")


    def to_dict(self):
        a = {}
        for k, i in self.__dict__.items():
            #logger.info('def to_dict  k {} i {}'.format(k, i))
            if not k.startswith('_') and i is not None:
                if isinstance(i, date):
                    a[k] = i.isoformat()
                else:                
                    a[k] = str(i)
        #logger.info('def to dict {}'.format(self.claims_qty))
        a['claims_qty'] =self.claims_qty
        return a
