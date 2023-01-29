# coding=utf8

from flask import Blueprint, render_template, abort, request, session, redirect, url_for
from jinja2 import TemplateNotFound

dashboard_controller = Blueprint('dashboard_controller', __name__, url_prefix='/')

'''
Dashboard
'''


@dashboard_controller.route('/', methods=['GET'])
def dashboard():
    data = {"menuid": 1}
    try:
        return render_template("dashboard.html", data=data)
    except TemplateNotFound:
        abort(404)
