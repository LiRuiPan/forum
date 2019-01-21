from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory
)
from models.captcha import Captcha
from models.user import User
from routes.helper import current_user, login_required

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登陆
"""


@main.route("/")
def index():
    u = current_user()
    if u is None:
        result = request.args.get('result', ' ')
        c = Captcha.get()
        return render_template("user/login.html", path=c.path, cap_id=c.id, result=result)
    else:
        return redirect(url_for('topic.index'))


@main.route("/register_view")
def register_view():
    result = request.args.get('result', ' ')
    c = Captcha.get()
    return render_template("user/register.html", path=c.path, cap_id=c.id, result=result)


@main.route("/register/<int:id>", methods=['POST'])
def register(id):
    form = request.form.to_dict()
    content = form['content']
    flag = Captcha.scan(id, content)
    if flag:
        form.pop('content')
        u = User.register(form)
        if u is None:
            r = '该用户名已存在，请重新选择'
            return redirect(url_for('.register_view', result=r))
        else:
            r = '注册成功，请登陆'
            return redirect(url_for('.index', result=r))
    else:
        r = '验证码不正确，请重新输入'
        return redirect(url_for('.register_view', result=r))


@main.route("/login/<int:id>", methods=['POST'])
def login(id):
    form = request.form.to_dict()
    u = User.validate_login(form)
    print('login user <{}>'.format(u))
    if u is None:
        r = '用户名或密码有误，请重新输入'
        return redirect(url_for('.index', result=r))
    else:
        content = form['content']
        flag = Captcha.scan(id, content)
        if flag:
            # session 中写入 user_id
            session['user_id'] = u.id
            # 设置 cookie 有效期为 永久
            session.permanent = True
            return redirect(url_for('topic.index'))
        else:
            r = '验证码不正确，请重新输入'
            return redirect(url_for('.index', result=r))


@main.route('/logout')
@login_required
def logout():
    session.pop('user_id')
    return redirect(url_for('index.index'))


# 当前用户主页
@main.route('/profile')
@login_required
def profile():
    result = request.args.get('result', ' ')
    u = current_user()
    return render_template('user/profile.html', user=u, current=u.id, result=result)


@main.route('/user')
def user_detail():
    user_id = request.args['id']
    u = User.find(user_id)
    if u is None:
        abort(404)
    else:
        result = request.args.get('result', ' ')
        c = current_user()
        if c is None:
            current_user_id = -1
        else:
            current_user_id = c.id
        return render_template('user/profile.html', user=u, current=current_user_id, result=result)
    

@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)


def not_found(e):
    return render_template('404.html')