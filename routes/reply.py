from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes.helper import login_required, csrf_required, current_user
from models.reply import Reply

main = Blueprint('reply', __name__)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Reply.add(form, user_id=u.id)
    return redirect(url_for('topic.detail', id=m.topic_id))


@main.route("/delete")
@login_required
@csrf_required
def delete():
    reply_id = request.args['reply_id']
    r = Reply.one(id=reply_id)
    topic_id = r.topic_id
    u = current_user()
    if u.id == r.user_id or u.role == 'admin':
        Reply.delete(id=reply_id)
        r = '删除评论成功'
        return redirect(url_for('topic.detail', id=topic_id, result=r))
    else:
        r = '没有权限'
        return redirect(url_for('topic.detail', id=topic_id, result=r))