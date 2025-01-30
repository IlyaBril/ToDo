import functools
import logging

from sqlalchemy import func, select, insert

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, Task, db

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')

bp = Blueprint('auth', __name__, url_prefix='/auth')
logger.info('blueprint {}'.format(bp))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                #db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, generate_password_hash(password)), )
                db.session.execute(insert(User), {"username": username, "password": generate_password_hash(password)})
                db.session.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    logger.info('logging in')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        error = None

        user = db.session.execute(select(User).where(User.username==username)).scalar_one_or_none() 

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id

           # query = db.session.execute(select(Task).where(Task.user_id==user.id)).first() is None
           # if query is True:
            #    task = Task()
             #   task.user_id=user.id
              #  db.session.add(task)
               # db.session.commit()

            return redirect(url_for('todo.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        #g.user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        g.user = db.session.execute(select(User).where(User.id == user_id)).scalar_one_or_none() 
        


@bp.route('/logout')
def logout():
    session.clear()
    logger.info('session cleaned {}'.format(session))
    return redirect(url_for('todo.index'))


def login_required(view):
    logger.info('Logging required requested')
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        #logger.info('g user is {}'.format(g.user))
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view