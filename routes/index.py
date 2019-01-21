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

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
"""


@main.route("/")
def index():
    return render_template('index.html')


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)


def not_found(e):
    return render_template('404.html')