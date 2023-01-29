# coding=utf8
from wtforms import Form, IntegerField, SelectField, validators


class RecordForm(Form):
    client_id = IntegerField(u'客户ID', [validators.DataRequired(message=u"客户ID不能为空。")])
    product_amount = IntegerField(u'充值点数', [validators.DataRequired(message=u"充值数量不能为空。")])
