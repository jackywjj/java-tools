# coding=utf8
from app.models.base import *


class ClientPointRecord(Base):
    __tablename__ = 'clt_client_point_records'
    last_order_id = db.Column(db.Integer(), nullable=False)
    client_id = db.Column(db.Integer(), nullable=False)
    product_amount = db.Column(db.Integer(), nullable=False)
    created_by = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer(), nullable=False)

    def __init__(self, client_id, product_amount, created_by):
        self.client_id = client_id
        self.product_amount = product_amount
        self.created_by = created_by
        self.status = 1
