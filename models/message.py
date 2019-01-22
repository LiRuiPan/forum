from sqlalchemy import Column, Unicode, UnicodeText, Integer, Boolean

from models.base_model import SQLMixin, db
from models.user import User


class Messages(SQLMixin, db.Model):
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    read = Column(Boolean, nullable=False, default=False)

    def sender(self):
        sender_id = self.sender_id
        u = User.one(id=sender_id)
        return u

    def receiver(self):
        receiver_id = self.receiver_id
        u = User.one(id=receiver_id)
        return u