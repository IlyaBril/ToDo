import functools
import logging
from datetime import date
from sqlalchemy import func, select

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from sqlalchemy.orm import Session
from sqlalchemy import func, select, insert

from .models import db
from .auth import login_required
from .models import Task

todobp = Blueprint('todo', __name__, url_prefix='/')

def first_row_check(db):
    query = db.session.execute(select(Task)).first() is None
    logger.info('first row {}'.format(query))
    if query is True:
        task = Task()
        db.session.add(task)
        db.session.commit()



@login_required
@todobp.route('/')
def index():
    return render_template('tables/todo_table.html')


@login_required
@todobp.route('/api/data')
def data():
    query = Task.query

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Task.description.like(f'%{search}%'),
            Task.remark.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            description = s[1:]
            if description not in ['description', 'remark', 'category']:
                description = 'description'
            col = getattr(Task, description)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'total': total,
    }


@todobp.route('/api/data', methods=['POST'])
def update():
    logger.info('POST requested')
    data = request.get_json()
    logger.info('POST requested {}'.format(data))
    if 'id' not in data:
        abort(400)
    task = Task.query.get(data['id'])
    logger.info('Task quey {}'. format(task))
    for field in ['description', 'category', 'responsible', 'remind', 'start_date', 'due_date', 'finish_date', 'remark']:
        if field in data:
            logger.info('if is instfiled {} '.format(isinstance(getattr(Task, field)._Annotated__element.type, db.Date)))
            if isinstance(getattr(Task, field)._Annotated__element.type, db.Date):
                logger.info('set attribute task {} field {} date from iso {}'.format(task, field, date.fromisoformat(data[field])))
                setattr(task, field, date.fromisoformat(data[field]))
            else: 
                setattr(task, field, data[field])
                logger.info('set attribute field {} data {} '.format(field, data[field]))

    db.session.commit()
    
    return '', 204
