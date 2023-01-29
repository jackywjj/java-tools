# coding=utf8
from datetime import datetime

from app.models.base import *


class CustomerOrderItem(Base):
    __tablename__ = 'clt_customer_order_items'
    order_id = db.Column(db.Integer(), nullable=False)
    order_type = db.Column(db.String(5), nullable=False)
    product_id = db.Column(db.Integer(), nullable=False)
    product_type = db.Column(db.Integer(), nullable=False)
    product_param = db.Column(db.String(255), nullable=False)
    out_trade_no = db.Column(db.String(50), nullable=False)
    goods_id = db.Column(db.Integer(), nullable=False)
    goods_title = db.Column(db.String(50), nullable=False)
    order_item_type = db.Column(db.Integer(), nullable=False)
    payment_amount = db.Column(db.Integer(), nullable=False)
    coin_amount = db.Column(db.Integer(), nullable=False)
    product_amount = db.Column(db.Integer(), nullable=False)
    item_id = db.Column(db.Integer(), nullable=False)
    shelf_goods_id = db.Column(db.Integer(), nullable=False)
    shelf_goods_title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, out_trade_no, product_amount, order_id, order_time):
        self.order_id = order_id
        self.order_type = '016'
        self.product_id = 0
        self.product_type = 0
        self.product_param = ''
        self.out_trade_no = out_trade_no
        self.goods_id = 34
        self.goods_title = '一书一课企业学习流量（正式）'
        self.order_item_type = 0
        self.payment_amount = 0
        self.coin_amount = 0
        self.product_amount = product_amount
        self.item_id = 0
        self.shelf_goods_id = 7
        self.shelf_goods_title = '一书一课企业学习流量'
        self.created_at = order_time


