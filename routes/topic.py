from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    return render_template("topic/index.html")