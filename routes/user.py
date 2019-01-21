from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session
)

import uuid
import os
from werkzeug.datastructures import FileStorage
from routes.helper import current_user, login_required, new_csrf_token, csrf_required
from models.user import User

main = Blueprint('user', __name__)


@main.route('/setting')
@login_required
def setting():
    u = current_user()
    r = request.args.get('result', ' ')
    token = new_csrf_token()
    return render_template('setting.html', user=u, token=token, result=r)


# 用户修改个人信息
@main.route('/edit', methods=["POST"])
@login_required
@csrf_required
def edit():
    user_id = request.args['id']
    form = request.form.to_dict()
    if 'role' in form:
        r = '非法操作'
        redirect(url_for('.setting', result=r))
    else:
        if form['receive_message'] == 'True':
            form['receive_message'] = True
        else:
            form['receive_message'] = False
        User.update(user_id, **form)
        r = '设置成功'
        return redirect(url_for('.setting', result=r))


# 用户修改密码
@main.route('/change', methods=["POST"])
@login_required
@csrf_required
def change():
    user_id = request.args['id']
    username = request.args['username']
    form = request.form.to_dict()
    f = dict(
        username=username,
        password=form['old_pass']
    )
    u = User.validate_login(f)
    if u is None:
        r = '旧密码不正确'
    else:
        password = User.salted_password(form['new_pass'])
        User.update(user_id, password=password)
        r = '修改成功'
    return redirect(url_for('.setting', result=r))


@main.route('/logout')
@login_required
def logout():
    session.pop('user_id')
    return redirect(url_for('index.index'))


@main.route('/image/add', methods=['POST'])
@login_required
@csrf_required
def avatar_add():
    file: FileStorage = request.files['avatar']

    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)
    user_id = request.args['id']
    User.update(user_id, image='/images/{}'.format(filename))
    r = '上传成功'
    return redirect(url_for('.setting', result=r))