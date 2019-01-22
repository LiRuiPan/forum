from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes.helper import current_user, login_required, csrf_required, new_csrf_token
from models.message import Messages
from models.user import User

main = Blueprint('mail', __name__)


@main.route('/')
@login_required
def index():
    u = current_user()
    unread = Messages.all(receiver_id=u.id, read=False)
    reads = Messages.all(receiver_id=u.id, read=True)
    sends = Messages.all(sender_id=u.id)
    token = new_csrf_token()
    t = render_template(
        'mail/index.html',
        user=u,
        unread=unread,
        read=reads,
        sends=sends,
        token=token
    )
    return t


@main.route("/write")
@login_required
def write():
    receiver_id = int(request.args['id'])
    r: User = User.one(id=receiver_id)
    if r.receive_message is False:
        result = '对方不接受私信'
        return redirect(url_for('index.user_detail', id=r.id, result=result))
    else:
        u = current_user()
        token = new_csrf_token()
        return render_template('mail/write.html', r=r, user=u, token=token)


@main.route("/reply")
@login_required
def reply():
    r_id = int(request.args['receiver_id'])
    m_id = int(request.args['message_id'])
    Messages.update(m_id, read=True)
    return redirect(url_for('.write', id=r_id))


@main.route("/send", methods=["POST", "GET"])
@login_required
@csrf_required
def send():
    form = request.form.to_dict()
    form['receiver_id'] = int(request.args['id'])
    u = current_user()
    form['sender_id'] = u.id
    Messages.new(form)
    return redirect(url_for('.index'))


@main.route("/read")
@login_required
@csrf_required
def read():
    m_id = int(request.args['id'])
    Messages.update(m_id, read=True)
    return redirect(url_for('.index'))


@main.route("/delete")
@login_required
@csrf_required
def delete():
    m_id = int(request.args['id'])
    Messages.delete(id=m_id)
    return redirect(url_for('.index'))