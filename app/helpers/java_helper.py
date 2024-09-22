# coding=utf8
import pymysql
from app import db
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT

conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DATABASE, port=int(MYSQL_PORT),
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


def get_databases():
    sql = "SHOW DATABASES"
    cursor.execute(sql)
    dbs = []
    result = cursor.fetchall()
    for row in result:
        dbs.append(row['Database'])
    return dbs


def get_tables(dbname):
    sql = "SELECT TABLE_NAME AS tableName FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='" + dbname + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    tables = []
    for row in result:
        tables.append(row['tableName'])
    return tables


def get_table_field(table_name):
    sql = "SHOW FULL COLUMNS FROM " + table_name
    cursor.execute(sql)
    results = cursor.fetchall()
    fields = []
    for result in results:
        fields.append({'field': result['Field'], 'type': result['Type'],
                       'isNull': result['Null'], 'key': result['Key'],
                       'defaultValue': result['Default'], 'extra': result['Extra'], 'comment': result['Comment']})
    return fields


def get_select_field(table_name, fields):
    sql = "SELECT "
    sqlField = ""
    for field in fields:
        # attr = convertField(field['field'])
        if sqlField == '':
            sqlField += field['field']
        else:
            sqlField += ',' + field['field']
    sql += sqlField + ' FROM ' + table_name
    return sql


def get_insert_sql(table_name, fields):
    sql = "INSERT INTO " + table_name + " "
    sqlField = ''
    sqlValue = ''
    for field in fields:
        if field['extra'] != 'auto_increment':
            if sqlField == '':
                sqlField += field['field']
            else:
                sqlField += ',' + field['field']
    sql += '(' + sqlField + ') VALUES '

    for field in fields:
        if field['extra'] != 'auto_increment':
            attr = convert_field(field['field'])
            if sqlValue == '':
                sqlValue = '#{' + attr + '}'
            else:
                sqlValue += ',#{' + attr + '}'
    sql += '(' + sqlValue + ') '
    return sql


def get_update_sql(table_name, fields):
    sql = "UPDATE " + table_name + " SET "
    sqlField = ""
    where = ""
    for field in fields:
        attr = convert_field(field['field'])
        if field['extra'] != 'auto_increment':
            if sqlField == '':
                sqlField += field['field'] + '=#{' + attr + '}'
            else:
                sqlField += ',' + field['field'] + '=#{' + attr + '}'
        if field['extra'] == 'auto_increment':
            where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
    sql += sqlField + where
    return sql


def get_update_sql_v2(table_name, fields):
    sql = "UPDATE " + table_name + "<br/>"
    sql += "\t\t&lt;set&gt;<br/>"
    for field in fields:
        attr = convert_field(field['field'])
        if not (field['extra'] == 'auto_increment'):
            sql += "\t\t\t&lt;if test=\"" + attr + "!=null\"&gt; " + field[
                'field'] + "=#{" + attr + "} &lt;/if&gt;<br/>"
    sql += "\t\t&lt;/set&gt;<br/>"
    sql += "\t\tWHERE id=#{id}"
    return sql


def get_delete_sql(table_name, fields):
    sql = "DELETE FROM " + table_name
    where = ""
    for field in fields:
        attr = convert_field(field['field'])
        if field['extra'] == 'auto_increment':
            where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
    sql += where
    return sql


def get_select_sql(table_name, fields):
    sql = "SELECT "
    sqlField = ""
    where = ""
    for field in fields:
        attr = convert_field(field['field'])
        if sqlField == '':
            sqlField += field['field'] + ' AS ' + attr
        else:
            sqlField += ',' + field['field'] + ' AS ' + attr
        if field['extra'] == 'auto_increment':
            where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
    sql += sqlField + ' FROM ' + table_name + where
    return sql


def get_select_field_for_mapper(table_name, fields):
    sql = "SELECT "
    sqlField = ""
    for field in fields:
        attr = convert_field(field['field'])
        if sqlField == '':
            sqlField += field['field'] + ' AS ' + attr
        else:
            sqlField += ',' + field['field'] + ' AS ' + attr
    sql += sqlField + ' FROM ' + table_name
    return sql


def get_select_normal_field_for_mapper(table_name, fields):
    sql = "SELECT "
    sqlField = ""
    for field in fields:
        if sqlField == '':
            sqlField += field['field']
        else:
            sqlField += ',' + field['field']
    sql += sqlField + ' FROM ' + table_name
    return sql


def get_simple_select_sql(table_name, fields):
    sql = "SELECT "
    sqlField = ""
    where = ""
    for field in fields:
        attr = convert_field(field['field'])
        if sqlField == '':
            sqlField += field['field']
        else:
            sqlField += ',' + field['field']
        if field['extra'] == 'auto_increment':
            where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
    sql += sqlField + ' FROM ' + table_name + where
    return sql


def get_java_entity(table_name, object_name, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>" \
           "@EqualsAndHashCode(callSuper = false)<br/>@TableName(\"" + table_name + "\")<br/>"
    code += "public class " + title_first(object_name) + " {<br/>"
    for field in fields:
        attr = convert_field(field['field'])
        code += "\t" + '/** ' + field['comment'] + ' */' + "<br/>"
        fieldType = render_field_type(field['type'])
        annotation = render_annotation(field['field'])
        if annotation is not None:
            code += "\t" + annotation + "<br/>"
        code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code


def get_java_dto(object_name, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>"
    code += "public class " + title_first(object_name) + "Dto {<br/>"
    for field in fields:
        attr = convert_field(field['field'])
        if (attr != 'createdBy') and (attr != 'createdAt') and (attr != 'updatedBy') and (attr != 'updatedAt') and (
                attr != 'active'):
            fieldType = render_field_type(field['type'])
            code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code


def get_java_bo(object_name, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>"
    code += '@ApiModel("")' + "<br/>"
    code += "public class " + title_first(object_name) + "Bo {<br/>"
    for field in fields:
        attr = convert_field(field['field'])
        if (attr != 'createdBy') and (attr != 'createdAt') and (attr != 'updatedBy') and (attr != 'updatedAt') and (
                attr != 'active'):
            code += "\t" + '@ApiModelProperty(value = "' + field['comment'] + '")' + "<br/>"
            fieldType = render_field_type(field['type'])
            code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code


def get_java_form_bean(object_name, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>"
    code += "public class " + title_first(object_name) + "Form {<br/>"
    for field in fields:
        attr = convert_field(field['field'])
        if (attr != 'createdBy') and (attr != 'createdAt') and (attr != 'updatedBy') and (attr != 'updatedAt') and (
                attr != 'active'):
            code += "\t" + '@ApiModelProperty(value = "' + field['comment'] + '")' + "<br/>"
            fieldType = render_field_type(field['type'])
            code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code


def get_java_vo(objectName, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>"
    code += "public class " + title_first(objectName) + "Vo {<br/>"
    for field in fields:
        attr = convert_field(field['field'])
        if (attr != 'createdBy') and (attr != 'createdAt') and (attr != 'updatedBy') and (attr != 'updatedAt') and (
                attr != 'active'):
            code += "\t" + '@ApiModelProperty(value = "' + field['comment'] + '")' + "<br/>"
            fieldType = render_field_type(field['type'])
            code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code


def get_java_assembler(object_name):
    code = "@Mapper<br/>"
    code += "public interface " + title_first(object_name) + "Assembler {<br/>"
    code += "\t" + title_first(object_name) + "Assembler INSTANCE = Mappers.getMapper(" + title_first(
        object_name) + "Assembler.class);<br/>"
    code += "\t" + title_first(object_name) + "Bo to" + title_first(object_name) + "Bo(" + title_first(
        object_name) + " " + object_name + ");<br/>"
    code += "\t" + title_first(object_name) + " to" + title_first(object_name) + "(" + title_first(
        object_name) + "Dto " + object_name + ");<br/>"
    code += "\t" + "List&lt;" + title_first(object_name) + "Bo&gt; to" + title_first(
        object_name) + "BoList(List&lt;" + title_first(
        object_name) + "&gt; " + object_name + "List);<br/>"
    code += '}'
    return code


def get_java_convertor(object_name):
    code = "@Mapper<br/>"
    code += "public interface " + title_first(object_name) + "Convertor {<br/>"
    code += "\t" + title_first(object_name) + "Convertor INSTANCE = Mappers.getMapper(" + title_first(
        object_name) + "Convertor.class);<br/>"
    code += "\t" + title_first(object_name) + "Vo to" + title_first(object_name) + "Vo(" + title_first(
        object_name) + " " + object_name + ");<br/>"
    code += "\t" + title_first(object_name) + "Vo to" + title_first(object_name) + "Vo(" + title_first(
        object_name) + "Bo " + object_name + "Bo);<br/>"
    code += "\t" + title_first(object_name) + "Dto to" + title_first(object_name) + "Dto(" + title_first(
        object_name) + "Form " + object_name + "Form);<br/>"
    code += "\t" + "List&lt;" + title_first(object_name) + "Vo&gt; to" + title_first(
        object_name) + "VoList(List&lt;" + title_first(
        object_name) + "&gt; " + object_name + "List);<br/>"
    code += "\t" + "List&lt;" + title_first(object_name) + "Vo&gt; to" + title_first(
        object_name) + "VoList(List&lt;" + title_first(
        object_name) + "Bo&gt; " + object_name + "BoList);<br/>"
    code += '}'
    return code


def get_java_adapter(object_name):
    code = "@Mapper<br/>"
    code += "public interface " + title_first(object_name) + "Adapter {<br/>"
    code += "\t" + title_first(object_name) + "Adapter INSTANCE = Mappers.getMapper(" + title_first(
        object_name) + "Adapter.class);<br/>"
    code += "\t" + title_first(object_name) + "Vo to" + title_first(object_name) + "Vo(" + title_first(
        object_name) + "Bo " + object_name + "Bo);<br/>"
    code += "\t" + title_first(object_name) + "Dto to" + title_first(object_name) + "Dto(" + title_first(
        object_name) + "Form " + object_name + "Form);<br/>"
    code += "\t" + "List&lt;" + title_first(object_name) + "Vo&gt; to" + title_first(
        object_name) + "VoList(List&lt;" + title_first(
        object_name) + "Bo&gt; " + object_name + "BoList);<br/>"
    code += '}'
    return code


def get_java_mapper(object_name, table_name, fields):
    className = title_first(object_name)

    field_sql = get_select_field_for_mapper(table_name, fields)
    normal_file_sql = get_select_normal_field_for_mapper(table_name, fields)

    insert_sql = get_insert_sql(table_name, fields)
    update_sql = get_update_sql(table_name, fields)

    code = "public interface " + className + "Mapper {<br/>"

    # code += "\t" + 'String SELECT_FIELDS = "' + field_sql + '";<br/>'
    code += "\t" + 'String SELECT_FIELDS = "' + normal_file_sql + ' ";<br/>'

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 新建 ' + object_name + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + object_name + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '@Insert("' + insert_sql + '")' + "<br/>"
    code += "\t" + 'int create' + className + '(' + className + ' ' + object_name + ');' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 更新 ' + object_name + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + object_name + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '@Update("' + update_sql + '")' + "<br/>"
    code += "\t" + 'int update' + className + '(' + className + ' ' + object_name + ');' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 删除 ' + object_name + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param id' + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'int delete' + className + '(@Param("id") int id);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 根据ID获取 ' + object_name + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param id' + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '@Select(SELECT_FIELDS + " WHERE id=#{id}")' + "<br/>"
    code += "\t" + '' + className + ' get' + className + 'ById(@Param("id") int id);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 获取 ' + object_name + u" 列表<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '@Select(SELECT_FIELDS + " WHERE active=1 ORDER BY id DESC")' + "<br/>"
    code += "\t" + 'List&lt;' + className + '&gt; get' + className + 'List();' + "<br/>"

    code += '}'
    return code


def get_java_service(object_name):
    className = title_first(object_name)
    code = "public interface " + className + "Service {<br/>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 新建 ' + object_name + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + object_name + "Dto<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'int create' + className + '(' + className + 'Dto ' + object_name + 'Dto);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 更新 ' + object_name + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + object_name + "Dto<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'int update' + className + '(' + className + 'Dto ' + object_name + 'Dto);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 删除 ' + object_name + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + object_name + 'Id' + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'int delete' + className + '(int ' + object_name + 'Id);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 根据ID获取 ' + object_name + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + object_name + 'Id' + "<br/>"
    code += "\t" + ' * @return ' + className + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '' + className + 'Bo get' + className + 'ById(int ' + object_name + 'Id);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 获取 ' + object_name + u" 列表<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @return List&lt;' + className + 'Bo&gt;' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'List&lt;' + className + 'Bo&gt; get' + className + 'List();' + "<br/>"

    code += '}'
    return code


def convert_field(field):
    fieldList = field.split("_")
    attr = ''
    for f in fieldList:
        if attr == '':
            attr = f
        else:
            attr += f.title()
    return attr


def title_first(str):
    if len(str) <= 0:
        return
    return str[0:1].title() + str[1:]


def render_field_type(field_type):
    if field_type.startswith('bigint'):
        return 'Long'
    elif field_type.startswith('datetime'):
        return 'LocalDateTime'
    elif field_type.startswith('date'):
        return 'LocalDate'
    elif field_type.startswith('tinyint'):
        return 'Integer'
    elif field_type.startswith('int'):
        return 'Integer'
    elif field_type.startswith('decimal'):
        return 'BigDecimal'
    elif field_type.startswith('timestamp'):
        return 'LocalDateTime'
    else:
        return 'String'


def render_annotation(field_name):
    if field_name.startswith('active'):
        return '@TableLogic' + "<br/>\t@TableField(fill = FieldFill.INSERT)"
    elif field_name.startswith('updated_at'):
        return '@TableField(fill = FieldFill.INSERT_UPDATE)'
    elif field_name.startswith('created_at'):
        return '@TableField(fill = FieldFill.INSERT)'
    elif field_name == 'id':
        return '@TableId(value = "id",type = IdType.AUTO)'


def debug_print(msg):
    print(
        "\n##########################################################################################################")
    print(msg)
    print(
        "\n##########################################################################################################")


# For db doc generate function
def get_doc_tables(tablePrefix):
    sql = "SELECT TABLE_NAME AS tableName FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='cy_qydb' AND TABLE_NAME like '" + tablePrefix + "%%'"
    result = db.engine.execute(sql)
    tables = []
    for row in result:
        tables.append(row['tableName'])
    return tables


def get_table_comment(table_name):
    sql = "SHOW TABLE STATUS WHERE Name='" + table_name + "';"
    result = db.engine.execute(sql)
    one_row = result.fetchone()
    if one_row is not None:
        return one_row['Comment']
    else:
        return ''


def generate_db_doc(table_name, fields):
    table_comment = get_table_comment(table_name)
    html = '## &lt;span id="archor_' + table_name + '"&gt;' + table_name + '&lt;/span&gt;' + "\n\n"
    html += table_comment + "\n\n"
    html += u'字段 | 类型 | Extra | 默认 | 备注' + "\n"
    html += '---------- | ---------- | ---------- | ---------- | ----------' + "\n"
    for field in fields:
        field_type = field['type'].split(" ")
        temp_type = field_type[0]
        temp_extra = ''
        if len(field_type) > 1:
            temp_extra = field_type[1]
        html += field['field'] + ' | ' + temp_type + ' | ' + temp_extra + ' | ' + field['extra'] + ' | ' + field[
            'comment'] + "\n"
    html += "\n\n"
    return html
