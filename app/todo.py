import functools
import logging
from datetime import date

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from sqlalchemy.orm import Session
from sqlalchemy import func, select

from .db import db
from .auth import login_required
from .models import Task

todobp = Blueprint('todo', __name__, url_prefix='/')


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
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    task = Task.query.get(data['id'])
    for field in ['description', 'category', 'responsible', 'remind', 'start_date', 'due_date', 'finish_date', 'remark']:
        if field in data:
            setattr(task, field, data[field])
    db.session.commit()
    return '', 204
