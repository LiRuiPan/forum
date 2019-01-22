from sqlalchemy import Integer, Column, UnicodeText, Unicode

from models.base_model import SQLMixin, db
import models.user
from models.board import Board


class Topic(SQLMixin, db.Model):
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def user(self):
        u = models.user.User.one(id=self.user_id)
        return u

    def board(self):
        b = Board.one(id=self.board_id).title
        return b