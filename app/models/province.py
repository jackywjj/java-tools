# coding=utf8
from app.models.base import *


class Province(Base):
    __tablename__ = 'dic_provinces'
    province_code = db.Column(db.String(50), nullable=False)
    province_name = db.Column(db.String(50), nullable=False)
