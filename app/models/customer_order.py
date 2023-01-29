# coding=utf8
from datetime import datetime

from app.models.base import *


class CustomerOrder(Base):
    __tablename__ = 'clt_customer_orders'
    external_id = db.Column(db.String(50), nullable=False)
    external_order_no = db.Column(db.String(50), nullable=False)
    external_flag = db.Column(db.Integer(), nullable=False)
    open_id = db.Column(db.String(50), nullable=False)
    union_id = db.Column(db.String(50), nullable=False)
    device_uuid = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.Integer(), nullable=False)
    customer_mobile = db.Column(db.String(50), nullable=False)
    customer_name = db.Column(db.String(50), nullable=False)
    client_id = db.Column(db.Integer(), nullable=False)
    customer_id = db.Column(db.Integer(), nullable=False)
    client_customer_id = db.Column(db.Integer(), nullable=False)
    refer_type = db.Column(db.Integer(), nullable=False)
    agent_level_one_id = db.Column(db.Integer(), nullable=False)
    agent_level_two_id = db.Column(db.Integer(), nullable=False)
    agent_level_three_id = db.Column(db.Integer(), nullable=False)
    refer_id = db.Column(db.Integer(), nullable=False)
    refer_agent_id = db.Column(db.Integer(), nullable=False)
    out_trade_no = db.Column(db.String(50), nullable=False)
    order_id = db.Column(db.Integer(), nullable=False)
    order_type = db.Column(db.String(5), nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.now())
    shelf_product_id = db.Column(db.Integer(), nullable=False)
    product_id = db.Column(db.Integer(), nullable=False)
    product_type = db.Column(db.Integer(), nullable=False)
    product_param = db.Column(db.String(50), nullable=False)
    campaign_id = db.Column(db.Integer(), nullable=False)
    payment_type = db.Column(db.Integer(), nullable=False)
    payment_amount = db.Column(db.Integer(), nullable=False)
    coin_amount = db.Column(db.Integer(), nullable=False)
    payment_status = db.Column(db.Integer(), nullable=False)
    order_status = db.Column(db.Integer(), nullable=False)
    original_amount = db.Column(db.Integer(), nullable=False)
    coupon_id = db.Column(db.Integer(), nullable=False)
    discount_amount = db.Column(db.Integer(), nullable=False)
    refund_status = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.Integer(), nullable=False)
    sale_channel = db.Column(db.String(20), nullable=False)
    order_mode = db.Column(db.Integer(), nullable=False)
    payment_mode = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    created_user_id = db.Column(db.Integer(), nullable=False)
    payment_user_id = db.Column(db.Integer(), nullable=False)
    order_source = db.Column(db.String(20), nullable=False)
    promotion_id = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, out_trade_no, order_time, client_id, product_amount, order_id, client_user_id, agent_user_id):
        self.external_id = ''
        self.external_order_no = ''
        self.external_flag = 0
        self.open_id = ''
        self.union_id = ''
        self.device_uuid = ''
        self.device_type = 0
        self.customer_mobile = ''
        self.customer_name = ''
        self.client_id = client_id
        self.customer_id = 0
        self.client_customer_id = 0
        self.refer_type = 0
        self.agent_level_one_id = 0
        self.agent_level_two_id = 0
        self.agent_level_three_id = 0
        self.refer_id = 0
        self.refer_agent_id = 0
        self.out_trade_no = out_trade_no
        self.order_id = order_id
        self.order_type = '016'
        self.product_amount = product_amount
        self.order_time = order_time
        self.shelf_product_id = 0
        self.product_id = 0
        self.product_type = 0
        self.product_param = ''
        self.campaign_id = 0
        self.payment_type = 6
        self.payment_amount = 0
        self.coin_amount = 0
        self.payment_status = 0
        self.order_status = 1
        self.original_amount = 0
        self.coupon_id = 0
        self.discount_amount = 0
        self.refund_status = 1
        self.status = 10
        self.sale_channel = 'SK_AGENT'
        self.order_mode = 1
        self.payment_mode = 1
        self.user_id = client_user_id
        self.created_user_id = agent_user_id
        self.payment_user_id = agent_user_id
        self.order_source = 'PARTNER'
        self.promotion_id = 0
        self.created_at = order_time
