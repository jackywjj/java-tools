# coding=utf8
from app.models.base import *


class City(Base):
    __tablename__ = 'dic_cities'
    province_code = db.Column(db.String(50), nullable=False)
    city_code = db.Column(db.String(50), nullable=False)
    city_name = db.Column(db.String(50), nullable=False)

    def toJson(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
