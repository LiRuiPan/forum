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
import flask_mail
from models.captcha import Captcha
from models.user import User
from models.topic import Topic
from routes.helper import current_user, login_required, new_csrf_token, csrf_required
from config import admin_mail

main = Blueprint('index', __name__)
mail = flask_mail.Mail()


"""
用户在这里可以
    访问首页
    注册
    登陆
    查看个人主页
    找回密码
    查找内容
    查看关于界面
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


# 注册页面
@main.route("/register_view")
def register_view():
    result = request.args.get('result', ' ')
    c = Captcha.get()
    return render_template("user/register.html", path=c.path, cap_id=c.id, result=result)


# 注册
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


# 登陆
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


# 找回密码界面
@main.route('/find_view')
def find_view():
    r = request.args.get('result', ' ')
    c = Captcha.get()
    return render_template('user/find.html', path=c.path, cap_id=c.id, result=r)


# 向用户邮箱发送找回密码邮件
def send_to_user(user):
    token = new_csrf_token(user.id)
    title = '找回密码邮件'
    content = '请尽快点击此链接更改密码 https://www.liruipan.com/find_password_view?token={}&user_id={}'.format(token, user.id)
    m = flask_mail.Message(
        subject=title,
        body=content,
        sender=admin_mail,
        recipients=[user.email]
    )
    mail.send(m)
    return None


# 找回密码
@main.route('/find/<int:id>', methods=['POST'])
def find(id):
    form = request.form.to_dict()
    u = User.one(username=form['username'])
    if u is None:
        r = '该用户不存在，请重新输入'
    else:
        content = form['content']
        flag = Captcha.scan(id, content)
        if flag:
            if u.email == form['email']:
                send_to_user(u)
                r = '已向您的邮箱发送更改密码邮件，请及时查看'
            else:
                r = '邮箱不正确，请重新输入'
        else:
            r = '验证码不正确，请重新输入'
    return redirect(url_for('.find_view', result=r))


# 用户忘记密码后更改密码的界面
@main.route('/find_password_view')
@csrf_required
def find_password_view():
    r = request.args.get('result', ' ')
    user_id = request.args['user_id']
    c = Captcha.get()
    return render_template('user/change_pass.html', path=c.path, cap_id=c.id, user_id=user_id, result=r)


# 用户忘记密码后更改密码
@main.route('/find_password', methods=['POST', 'GET'])
def change_password():
    cap_id = request.args['cap_id']
    user_id = int(request.args['user_id'])
    form = request.form.to_dict()
    u = User.one(username=form['username'])
    if u is None or u.id != user_id:
        r = '请输入正确的用户名'
    else:
        content = form['content']
        flag = Captcha.scan(cap_id, content)
        if flag:
            password = User.salted_password(form['password'])
            User.update(user_id, password=password)
            r = '修改成功，请登陆'
            return redirect(url_for('.index', result=r))
        else:
            r = '验证码不正确,请重新输入'
    token = new_csrf_token(user_id)
    return redirect(url_for('.find_password_view', token=token, user_id=user_id, result=r))


# 当前用户主页
@main.route('/profile')
@login_required
def profile():
    result = request.args.get('result', ' ')
    u = current_user()
    token = new_csrf_token()
    return render_template('user/profile.html', user=u, current=u.id, token=token, result=result)


# 用户主页
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
        token = new_csrf_token()
        return render_template('user/profile.html', user=u, current=current_user_id, token=token, result=result)


# 关于
@main.route('/about')
def about():
    u = current_user()
    return render_template('about.html', user=u)


# 查找
@main.route('/search', methods=['POST'])
def search():
    content = request.form['content']
    u = User.one(username=content)
    if u is not None:
        return redirect(url_for('.user_detail', id=u.id))
    else:
        t = Topic.one(title=content)
        if t is not None:
            return redirect(url_for('topic.detail', id=t.id))
        else:
            return not_found(t)


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)


def not_found(e):
    return render_template('404.html')