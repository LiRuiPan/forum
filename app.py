from flask import Flask
import secret
from routes.index import main as index_routes
from routes.index import not_found


# 注册路由
def register_routes(app):
    app.register_blueprint(index_routes)
    app.errorhandler(404)(not_found)


# 配置
def configured_app():
    app = Flask(__name__)
    app.secret_key = secret.secret_key

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
