import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer

db = SQLAlchemy()


def utctime():
    return int(time.time())


class SQLMixin(object):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)

    @classmethod
    def new(cls, form):
        m = cls()
        for name, value in form.items():
            setattr(m, name, value)

        m.save()
        return m

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.query.filter_by(id=id).first()
        kwargs['updated_time'] = utctime()
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.save()

    @classmethod
    def delete(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        for m in ms:
            db.session.delete(m)
        db.session.commit()
        return None

    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).first()
        return ms

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)

    def save(self):
        db.session.add(self)
        db.session.commit()