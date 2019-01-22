import functools
import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for
from models.user import User
from utils import log
import redis

cache = redis.StrictRedis()


def current_user():
    u_id = session.get('user_id', '')
    u: User = User.one(id=u_id)
    return u


def login_required(route_function):
    @functools.wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u is None:
            log('游客用户')
            r = '请登录'
            return redirect(url_for('index.index', result=r))
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        user_id = request.args.get('user_id', '')
        if user_id == '':
            u = current_user()
            user_id = str(u.id)
        else:
            user_id = str(user_id)

        if cache.exists(token) and cache.get(token).decode() == user_id:
            cache.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token(*user_id):
    if len(user_id) == 0:
        u = current_user()
        if u is None:
            user_id = str(-1)
        else:
            user_id = str(u.id)
    else:
        user_id = str(user_id[0])
    token = str(uuid.uuid4())
    cache.set(token, user_id)
    return token


def admin_required(route_function):
    @functools.wraps(route_function)
    def f():
        log('admin_required')
        u = current_user()
        if u is None:
            log('游客用户')
            r = '请登录'
            return redirect(url_for('index.index', result=r))
        elif u.role == 'admin':
            log('admin用户', route_function)
            return route_function()
        else:
            log('越权访问', route_function)
            r = '无权访问'
            return redirect(url_for('index.profile', result=r))

    return f