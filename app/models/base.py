# coding=utf8
from app import db

'''
Base model
'''


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def toJson(self):
        pass
