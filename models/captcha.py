from sqlalchemy import Column, UnicodeText
import os
from models.base_model import SQLMixin, db
from models.helper import captcha_path, captcha_image, captcha_text


class Captcha(SQLMixin, db.Model):
    path = Column(UnicodeText, nullable=False)
    content = Column(UnicodeText, nullable=False)

    @classmethod
    def get(cls):
        path = captcha_path()
        if os.path.exists(path):
            c = Captcha.one(path=path)
            return c
        else:
            content = captcha_text()
            captcha_image(content, path)
            f = dict(
                path=path,
                content=content
            )
            c = Captcha.new(f)
            return c

    @classmethod
    def scan(cls, cap_id, content):
        c = Captcha.one(id=cap_id)
        if c is None:
            return False
        else:
            if c.content.upper() == content.upper():
                return True
            else:
                return False
