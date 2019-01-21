from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from routes.helper import current_user

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template("topic/index.html", user=u)