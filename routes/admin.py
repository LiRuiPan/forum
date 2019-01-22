from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes.helper import admin_required, current_user, new_csrf_token, csrf_required

from models.board import Board

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