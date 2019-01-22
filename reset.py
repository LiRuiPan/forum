from sqlalchemy import create_engine
import secret
from app import configured_app
from models.base_model import db
from models.user import User
from models.board import Board
import os
import shutil


def clear_file():
    path = 'static/photos/captcha'
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS forum')
        c.execute('CREATE DATABASE forum CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE forum')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username=secret.admin_name,
        password=secret.admin_password,
        role='admin',
        image='/static/photos/head/default.jpg',
        email=secret.admin_email,
    )
    User.register(form)

    form = dict(
        username='gua',
        password='123',
        image='/static/photos/head/default.jpg',
        email=secret.test_mail,
    )
    User.register(form)
    boards = ['技术讨论', '个人随笔', '学习分享']
    for b in boards:
        Board.new(dict(title=b))


if __name__ == '__main__':
    app = configured_app()
    clear_file()
    with app.app_context():
        reset_database()
        generate_fake_date()
