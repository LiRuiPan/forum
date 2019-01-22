from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from routes.helper import current_user
from models.board import Board
main = Blueprint('topic', __name__)


@main.route("/")
def index():
    u = current_user()
    bs = Board.all()
    return render_template("topic/index.html", user=u, bs=bs)