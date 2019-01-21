import functools
import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for
from models.user import User
from utils import log


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