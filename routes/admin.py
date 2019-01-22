from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes.helper import admin_required, current_user, new_csrf_token, csrf_required

from models.board import Board
from models.topic import Topic
from models.message import Messages
from models.reply import Reply

main = Blueprint('admin', __name__)


@main.route("/")
@admin_required
def index():
    u = current_user()
    token = new_csrf_token()
    return render_template('admin_index.html', user=u, token=token)


@main.route("/add_board", methods=["POST", "GET"])
@admin_required
@csrf_required
def add_board():
    form = request.form
    Board.new(form)
    return redirect(url_for('.index'))


@main.route("/delete_topic", methods=["POST", "GET"])
@admin_required
@csrf_required
def delete_topic():
    topic_title = request.form['title']
    t = Topic.one(title=topic_title)
    topic_id = t.id
    user_id = t.user_id
    content = '您的帖子《{}》已被管理员删除'.format(t.title)
    form = dict(
        receiver_id=user_id,
        sender_id=current_user().id,
        content=content
    )
    Messages.new(form)
    Topic.delete(id=topic_id)
    Reply.delete(topic_id=topic_id)
    return redirect(url_for('.index'))