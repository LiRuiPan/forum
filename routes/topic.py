from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from routes.helper import current_user, login_required, new_csrf_token, csrf_required
from models.board import Board
from models.topic import Topic

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    u = current_user()
    bs = Board.all()
    return render_template("topic/index.html", user=u, bs=bs, ms=ms, bid=board_id)


@main.route('/detail')
def detail():
    result = request.args.get('result', ' ')
    topic_id = request.args['id']
    m = Topic.get(topic_id)
    token = new_csrf_token()
    return render_template("topic/detail.html", topic=m, token=token, result=result)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/new")
@login_required
def new():
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token)


@main.route("/delete")
@login_required
@csrf_required
def delete():
    topic_id = request.args['id']
    Topic.delete(id=topic_id)
    r = '删除成功'
    return redirect(url_for('index.profile', result=r))