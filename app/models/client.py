# coding=utf8
from app.models.base import *


class Client(Base):
    __tablename__ = 'clt_clients'
    agent_id = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    company_short = db.Column(db.String(50), nullable=False)
