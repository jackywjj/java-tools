# coding=utf8
from app import db


def get_databases():
    sql = "SHOW DATABASES"
    result = db.engine.execute(sql)
    dbs = []
    for row in result:
        dbs.append(row['Database'])
    return dbs


def get_tables(dbname):
    sql = "SELECT TABLE_NAME AS tableName FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='" + dbname + "'"
    result = db.engine.execute(sql)
    tables = []
    for row in result:
        tables.append(row['tableName'])
    return tables


def get_table_field(tablename):
    sql = "SHOW FULL COLUMNS FROM " + tablename
    results = db.engine.execute(sql)
    fields = []
    for result in results:
        fields.append({'field': result['Field'], 'type': result['Type'],
                       'isNull': result['Null'], 'key': result['Key'],
                       'defaultValue': result['Default'], 'extra': result['Extra'], 'comment': result['Comment']})
    return fields


def get_select_field(tableName, fields):
    sql = "SELECT "
    sqlField = ""
    for field in fields:
        # attr = convertField(field['field'])
        if (sqlField == ''):
            sqlField += field['field']
        else:
            sqlField += ',' + field['field']
    sql += sqlField + ' FROM ' + tableName
    return sql


def get_insert_sql(tableName, fields):
    sql = "INSERT INTO " + tableName + " "
    sqlField = ''
    sqlValue = ''
    for field in fields:
        if (field['extra'] != 'auto_increment'):
            if (sqlField == ''):
                sqlField += field['field']
            else:
                sqlField += ',' + field['field']
    sql += '(' + sqlField + ') VALUES '

    for field in fields:
        if (field['extra'] != 'auto_increment'):
            attr = convertField(field['field'])
            if (sqlValue == ''):
                sqlValue = '#{' + attr + '}'
            else:
                sqlValue += ',#{' + attr + '}'
    sql += '(' + sqlValue + ') '
    return sql


def get_update_sql(tableName, fields):
    sql = "UPDATE " + tableName + " SET "
    sqlField = ""
    where = ""
    for field in fields:
        attr = convertField(field['field'])
        if (field['extra'] != 'auto_increment'):
            if (sqlField == ''):
                sqlField += field['field'] + '=#{' + attr + '}'
            else:
                sqlField += ',' + field['field'] + '=#{' + attr + '}'
        if (field['extra'] == 'auto_increment'):
            where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
    sql += sqlField + where
    return sql


def get_update_sql_v2(tableName, fields):
    sql = "UPDATE " + tableName + "<br/>"
    sql += "\t\t&lt;set&gt;<br/>"
    for field in fields:
        attr = convertField(field['field'])
        if not (field['extra'] == 'auto_increment'):
            sql += "\t\t\t&lt;if test=\"" + attr + "!=null\"&gt; " + field[
                'field'] + "=#{" + attr + "} &lt;/if&gt;<br/>"
    sql += "\t\t&lt;/set&gt;<br/>"
    sql += "\t\tWHERE id=#{id}"
    return sql


def get_delete_sql(tableName, fields):
    sql = "DELETE FROM " + tableName
    where = ""
    for field in fields:
        attr = convertField(field['field'])
        if (field['extra'] == 'auto_increment'):
            where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
    sql += where
    return sql


def get_select_sql(tableName, fields):
    sql = "SELECT "
    sqlField = ""
    where = ""
    for field in fields:
        attr = convertField(field['field'])
        if (sqlField == ''):
            sqlField += field['field'] + ' AS ' + attr
        else:
            sqlField += ',' + field['field'] + ' AS ' + attr
        if (field['extra'] == 'auto_increment'):
            where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
    sql += sqlField + ' FROM ' + tableName + where
    return sql


def get_select_field_for_mapper(tableName, fields):
    sql = "SELECT "
    sqlField = ""
    for field in fields:
        attr = convertField(field['field'])
        if (sqlField == ''):
            sqlField += field['field'] + ' AS ' + attr
        else:
            sqlField += ',' + field['field'] + ' AS ' + attr
    sql += sqlField + ' FROM ' + tableName
    return sql


def get_select_normal_field_for_mapper(tableName, fields):
    sql = "SELECT "
    sqlField = ""
    for field in fields:
        if (sqlField == ''):
            sqlField += field['field']
        else:
            sqlField += ',' + field['field']
    sql += sqlField + ' FROM ' + tableName
    return sql


def get_simple_select_sql(tableName, fields):
    sql = "SELECT "
    sqlField = ""
    where = ""
    for field in fields:
        attr = convertField(field['field'])
        if (sqlField == ''):
            sqlField += field['field']
        else:
            sqlField += ',' + field['field']
        if (field['extra'] == 'auto_increment'):
            where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
    sql += sqlField + ' FROM ' + tableName + where
    return sql


def get_java_entity(tableName, objectName, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>" \
           "@EqualsAndHashCode(callSuper = false)<br/>@TableName(\"" + tableName + "\")<br/>"
    code += "public class " + titleFirst(objectName) + " {<br/>"
    for field in fields:
        attr = convertField(field['field'])
        code += "\t" + '/** ' + field['comment'] + ' */' + "<br/>"
        fieldType = renderFieldType(field['type'])
        annotation = rederAnnotation(field['field'])
        if annotation != None:
            code += "\t" + annotation + "<br/>"
        code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code


def get_java_dto(objectName, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>"
    code += "public class " + titleFirst(objectName) + "Dto {<br/>"
    for field in fields:
        attr = convertField(field['field'])
        if (attr != 'createdBy') and (attr != 'createdAt') and (attr != 'updatedBy') and (attr != 'updatedAt') and (
                attr != 'active'):
            fieldType = renderFieldType(field['type'])
            code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code


def get_java_bo(objectName, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>"
    code += '@ApiModel("")' + "<br/>"
    code += "public class " + titleFirst(objectName) + "Bo {<br/>"
    for field in fields:
        attr = convertField(field['field'])
        if (attr != 'createdBy') and (attr != 'createdAt') and (attr != 'updatedBy') and (attr != 'updatedAt') and (
                attr != 'active'):
            code += "\t" + '@ApiModelProperty(value = "' + field['comment'] + '")' + "<br/>"
            fieldType = renderFieldType(field['type'])
            code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code
    
def get_java_form_bean(objectName, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>"
    code += "public class " + titleFirst(objectName) + "Form {<br/>"
    for field in fields:
        attr = convertField(field['field'])
        if (attr != 'createdBy') and (attr != 'createdAt') and (attr != 'updatedBy') and (attr != 'updatedAt') and (
                attr != 'active'):
            code += "\t" + '@ApiModelProperty(value = "' + field['comment'] + '")' + "<br/>"
            fieldType = renderFieldType(field['type'])
            code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code

def get_java_vo(objectName, fields):
    code = "@Getter<br/>@Setter<br/>@Builder<br/>@ToString<br/>@NoArgsConstructor<br/>@AllArgsConstructor<br/>"
    code += "public class " + titleFirst(objectName) + "Vo {<br/>"
    for field in fields:
        attr = convertField(field['field'])
        if (attr != 'createdBy') and (attr != 'createdAt') and (attr != 'updatedBy') and (attr != 'updatedAt') and (
                attr != 'active'):
            code += "\t" + '@ApiModelProperty(value = "' + field['comment'] + '")' + "<br/>"
            fieldType = renderFieldType(field['type'])
            code += "\t" + 'private ' + fieldType + ' ' + attr + ";<br/>"
    code += '}'
    return code


def get_java_assembler(objectName):
    code = "@Mapper<br/>"
    code += "public interface " + titleFirst(objectName) + "Assembler {<br/>"
    code += "\t" + titleFirst(objectName) + "Assembler INSTANCE = Mappers.getMapper(" + titleFirst(
        objectName) + "Assembler.class);<br/>"
    code += "\t" + titleFirst(objectName) + "Bo to" + titleFirst(objectName) + "Bo(" + titleFirst(
        objectName) + " " + objectName + ");<br/>"
    code += "\t" + titleFirst(objectName) + " to" + titleFirst(objectName) + "(" + titleFirst(
        objectName) + "Dto " + objectName + ");<br/>"
    code += "\t" + "List&lt;" + titleFirst(objectName) + "Bo&gt; to" + titleFirst(
        objectName) + "BoList(List&lt;" + titleFirst(
        objectName) + "&gt; " + objectName + "List);<br/>"
    code += '}'
    return code


def get_java_convertor(objectName):
    code = "@Mapper<br/>"
    code += "public interface " + titleFirst(objectName) + "Convertor {<br/>"
    code += "\t" + titleFirst(objectName) + "Convertor INSTANCE = Mappers.getMapper(" + titleFirst(
        objectName) + "Convertor.class);<br/>"
    code += "\t" + titleFirst(objectName) + "Vo to" + titleFirst(objectName) + "Vo(" + titleFirst(
        objectName) + " " + objectName + ");<br/>"
    code += "\t" + titleFirst(objectName) + "Vo to" + titleFirst(objectName) + "Vo(" + titleFirst(
        objectName) + "Bo " + objectName + "Bo);<br/>"
    code += "\t" + titleFirst(objectName) + "Dto to" + titleFirst(objectName) + "Dto(" + titleFirst(
        objectName) + "Form " + objectName + "Form);<br/>"
    code += "\t" + "List&lt;" + titleFirst(objectName) + "Vo&gt; to" + titleFirst(
        objectName) + "VoList(List&lt;" + titleFirst(
        objectName) + "&gt; " + objectName + "List);<br/>"
    code += "\t" + "List&lt;" + titleFirst(objectName) + "Vo&gt; to" + titleFirst(
        objectName) + "VoList(List&lt;" + titleFirst(
        objectName) + "Bo&gt; " + objectName + "BoList);<br/>"
    code += '}'
    return code

def get_java_adapter(objectName):
    code = "@Mapper<br/>"
    code += "public interface " + titleFirst(objectName) + "Adapter {<br/>"
    code += "\t" + titleFirst(objectName) + "Adapter INSTANCE = Mappers.getMapper(" + titleFirst(
        objectName) + "Adapter.class);<br/>"
    code += "\t" + titleFirst(objectName) + "Vo to" + titleFirst(objectName) + "Vo(" + titleFirst(
        objectName) + "Bo " + objectName + "Bo);<br/>"
    code += "\t" + titleFirst(objectName) + "Dto to" + titleFirst(objectName) + "Dto(" + titleFirst(
        objectName) + "Form " + objectName + "Form);<br/>"
    code += "\t" + "List&lt;" + titleFirst(objectName) + "Vo&gt; to" + titleFirst(
        objectName) + "VoList(List&lt;" + titleFirst(
        objectName) + "Bo&gt; " + objectName + "BoList);<br/>"
    code += '}'
    return code

def getJavaMapper(objectName, table_name, fields):
    className = titleFirst(objectName)

    field_sql = get_select_field_for_mapper(table_name, fields)
    normal_file_sql = get_select_normal_field_for_mapper(table_name, fields)

    insert_sql = get_insert_sql(table_name, fields)
    update_sql = get_update_sql(table_name, fields)

    code = "public interface " + className + "Mapper {<br/>"

    # code += "\t" + 'String SELECT_FIELDS = "' + field_sql + '";<br/>'
    code += "\t" + 'String SELECT_FIELDS = "' + normal_file_sql + ' ";<br/>'

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 新建 ' + objectName + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + objectName + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '@Insert("' + insert_sql + '")' + "<br/>"
    code += "\t" + 'int create' + className + '(' + className + ' ' + objectName + ');' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 更新 ' + objectName + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + objectName + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '@Update("' + update_sql + '")' + "<br/>"
    code += "\t" + 'int update' + className + '(' + className + ' ' + objectName + ');' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 删除 ' + objectName + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param id' + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'int delete' + className + '(@Param("id") int id);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 根据ID获取 ' + objectName + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param id' + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '@Select(SELECT_FIELDS + " WHERE id=#{id}")' + "<br/>"
    code += "\t" + '' + className + ' get' + className + 'ById(@Param("id") int id);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 获取 ' + objectName + u" 列表<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '@Select(SELECT_FIELDS + " WHERE active=1 ORDER BY id DESC")' + "<br/>"
    code += "\t" + 'List&lt;' + className + '&gt; get' + className + 'List();' + "<br/>"

    code += '}'
    return code


def getJavaService(objectName):
    className = titleFirst(objectName)
    code = "public interface " + className + "Service {<br/>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 新建 ' + objectName + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + objectName + "Dto<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'int create' + className + '(' + className + 'Dto ' + objectName + 'Dto);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 更新 ' + objectName + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + objectName + "Dto<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'int update' + className + '(' + className + 'Dto ' + objectName + 'Dto);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 删除 ' + objectName + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + objectName + 'Id' + "<br/>"
    code += "\t" + ' * @return int' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'int delete' + className + '(int ' + objectName + 'Id);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 根据ID获取 ' + objectName + "<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @param ' + objectName + 'Id' + "<br/>"
    code += "\t" + ' * @return ' + className + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + '' + className + 'Bo get' + className + 'ById(int ' + objectName + 'Id);' + "<br/>"

    code += "<br>"

    code += "\t" + '/**' + "<br/>"
    code += "\t" + u' * 获取 ' + objectName + u" 列表<br/>"
    code += "\t" + ' *' + "<br/>"
    code += "\t" + ' * @return List&lt;' + className + 'Bo&gt;' + "<br/>"
    code += "\t" + ' */' + "<br/>"
    code += "\t" + 'List&lt;' + className + 'Bo&gt; get' + className + 'List();' + "<br/>"

    code += '}'
    return code


def convertField(field):
    fieldList = field.split("_")
    attr = ''
    for f in fieldList:
        if (attr == ''):
            attr = f
        else:
            attr += f.title()
    return attr


def titleFirst(str):
    if len(str) <= 0:
        return
    return str[0:1].title() + str[1:]


def renderFieldType(fieldType):
    if fieldType.startswith('bigint'):
        return 'Long'
    elif fieldType.startswith('datetime'):
        return 'LocalDateTime'
    elif fieldType.startswith('date'):
        return 'LocalDate'
    elif fieldType.startswith('tinyint'):
        return 'Integer'
    elif fieldType.startswith('int'):
        return 'Integer'
    elif fieldType.startswith('decimal'):
        return 'BigDecimal'
    elif fieldType.startswith('timestamp'):
        return 'LocalDateTime'
    else:
        return 'String'


def rederAnnotation(fieldName):
    if fieldName.startswith('active'):
        return '@TableLogic' + "<br/>\t@TableField(fill = FieldFill.INSERT)"
    elif fieldName.startswith('updated_at'):
        return '@TableField(fill = FieldFill.INSERT_UPDATE)'
    elif fieldName.startswith('created_at'):
        return '@TableField(fill = FieldFill.INSERT)'
    elif fieldName == 'id':
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


def get_table_comment(tableName):
    sql = "SHOW TABLE STATUS WHERE Name='" + tableName + "';"
    result = db.engine.execute(sql)
    one_row = result.fetchone()
    if one_row is not None:
        return one_row['Comment']
    else:
        return ''


def generate_db_doc(tableName, fields):
    table_comment = get_table_comment(tableName)
    html = '## &lt;span id="archor_' + tableName + '"&gt;' + tableName + '&lt;/span&gt;' + "\n\n"
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
