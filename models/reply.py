from sqlalchemy import Column, Integer, UnicodeText

from models.base_model import db, SQLMixin
import models.user
import models.topic


class Reply(SQLMixin, db.Model):

    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = models.user.User.one(id=self.user_id)
        return u

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        r = Reply.new(form)
        return r

    def topic(self):
        t = models.topic.Topic.one(id=self.topic_id)
        return t