# coding=utf8

from flask import Blueprint, render_template, request

from app.helpers.java_helper import get_databases, get_tables, get_table_field, get_insert_sql, get_update_sql, \
    get_delete_sql, get_select_sql, get_java_entity, get_simple_select_sql, get_java_mapper, get_java_service, \
    get_java_dto, get_java_bo, get_java_assembler, get_java_vo, get_java_convertor, get_java_form_bean, get_java_adapter

java_controller = Blueprint('client_point_controller', __name__, url_prefix='/java')

'''
Client Point
'''


@java_controller.route('/dbtools', methods=['GET', 'POST'])
def db_tools():
    db_name = request.args.get('db_name')
    table_name = request.args.get('table_name')
    object_name = request.args.get('object_name')
    dbs = get_databases()
    if not db_name:
        db_name = dbs[0]
    tables = get_tables(db_name)
    if not table_name:
        table_name = tables[0]

    fields = get_table_field(db_name + '.' + table_name)

    insert_sql = ''
    update_sql = ''
    delete_sql = ''
    select_sql = ''
    simple_select_sql = ''
    java_code = ''
    java_mapper = ''
    java_service = ''
    java_dto = ''
    java_bo = ''
    java_vo = ''
    java_form_bean = ''
    java_assembler = ''
    java_convertor = ''
    java_adapter = ''

    if object_name:
        insert_sql = get_insert_sql(table_name, fields)
        update_sql = get_update_sql(table_name, fields)
        delete_sql = get_delete_sql(table_name, fields)
        select_sql = get_select_sql(table_name, fields)
        simple_select_sql = get_simple_select_sql(table_name, fields)
        java_code = get_java_entity(table_name, object_name, fields)
        java_dto = get_java_dto(object_name, fields)
        java_bo = get_java_bo(object_name, fields)
        java_vo = get_java_vo(object_name, fields)
        java_form_bean = get_java_form_bean(object_name, fields)
        java_mapper = get_java_mapper(object_name, table_name, fields)
        java_service = get_java_service(object_name)
        java_assembler = get_java_assembler(object_name)
        java_convertor = get_java_convertor(object_name)
        java_adapter = get_java_adapter(object_name)

    else:
        object_name = ''

    data = {"menuid": 2}
    return render_template("java_tools.html", data=data, dbs=dbs, tables=tables, db_name=db_name, table_name=table_name,
                           fields=fields, insert_sql=insert_sql, update_sql=update_sql, select_sql=select_sql,
                           simple_select_sql=simple_select_sql, delete_sql=delete_sql, java_code=java_code,
                           java_mapper=java_mapper, java_service=java_service,
                           java_dto=java_dto, object_name=object_name, java_bo=java_bo, java_form_bean=java_form_bean,
                           java_assembler=java_assembler, java_vo=java_vo, java_convertor=java_convertor,
                           java_adapter=java_adapter)
