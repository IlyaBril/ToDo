from .db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(64), index=True)

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

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'category': self.category,
            'responsible': self.responsible,
            'remind_date': self.remind_date,
            'start_date': self.start_date,
			'due_date': self.due_date,
			'finish_date': self.finish_date,
			'remark': self.remark
        }
