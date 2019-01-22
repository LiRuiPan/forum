from flask import Flask
import time
import secret
from utils import log
from models.base_model import db

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.user import main as user_routes
from routes.message import main as message_routes
from routes.admin import main as admin_routes
from routes.index import not_found


def sort(cs):
    return sorted(cs, key=lambda c: c.created_time, reverse=True)


def count(input):
    log('count using jinja filter')
    return len(input)


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


# 注册路由
def register_routes(app):
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(message_routes, url_prefix='/message')
    app.register_blueprint(admin_routes, url_prefix='/admin')
    app.errorhandler(404)(not_found)
    app.template_filter()(sort)
    app.template_filter()(count)
    app.template_filter()(format_time)


# 配置
def configured_app():
    app = Flask(__name__)
    app.secret_key = secret.secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/forum?charset=utf8mb4'.format(
        secret.database_password
    )
    db.init_app(app)

    register_routes(app)

    return app


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=3000,
    )
    app.run(**config)
