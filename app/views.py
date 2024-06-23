# views.py
    # """
    # 该代码定义了 Web 应用程序的各种路由和功能，包括登录、注册、选择、插入、删除和查看 SQL 数据库中的数据。
    # :return: 该代码在 Flask 应用程序中定义多个路由。每个路由对应一个特定的 URL 端点，并与返回呈现的 HTML
    # 模板的函数关联。返回值是调用“render_template”函数的结果，该函数根据指定的模板文件和任何提供的数据生成 HTML 响应。
    # """
    # Orientation to Web Page


from flask import render_template, redirect, request
from app.__init__ import app
from app.sql import SQL_Server

global table
global username
global password
global verification_code
verification_code='abcd-efgh'

@app.route('/')
def welcome():
    """root panel"""
    return render_template('welcome.html')

@app.route('/login')
def loginPanel():
    """登陆"""
    return render_template('login.html')

@app.route('/logindetect', methods=['POST'])
def loginDetect():
    """detect login information"""
    global username, password
    username = request.form['username']
    password = request.form['password']
    sql = SQL_Server()
    # try to login
    results = sql.loginDetect(username, password)
    if len(results) == 0:
        return redirect('/login')
    return redirect('/developer')

@app.route('/register')
def registerPanel():
    """用户注册"""
    return render_template('register.html')

@app.route('/register/result', methods=['GET', 'POST'])
def registerResult():
    """show register result"""
    global verification_code
    username = request.form['username']
    password = request.form['password']
    temp_code=request.form['verification_code']
    if temp_code!=verification_code:
        return render_template('register.html')
    sql = SQL_Server()
    # try to insert (username, password) into USERTABLE
    result = sql.register(username, password)
    return render_template('register_result.html', username=username, password=password, result=result)

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    """patient register user information"""
    print("ok")
    return render_template('patient.html')

@app.route('/check_doctor', methods=['POST'])
def check_doctor():
    """check doctor"""
    table='doctor'
    attribute = ' '
    sql = SQL_Server()
    if not sql.tableDetect(table):
        # exceptions.BadRequestKeyError here
        print("error: table doctor not exist")
        return render_template('patient.html')
    results = sql.selectFromTable(table, ' ', ' ')
    attributeList = sql.getAttributeListForSelectShow(table, attribute)
    if len(results) != 0:
        col = len(results[0])
    else:
        col = 0
    return render_template('developer_select_result.html', table='_', attributeList=attributeList, results=results, attribute=attribute, row=len(results), col=col)

@app.route('/patient_insert', methods=['POST'])
def patient_insert():
    """patient insert"""
    table='doctor_visits'

    patient_id = request.form['patient_id']
    patient_name = request.form['patient_name']
    patient_gender = request.form['patient_gender']
    patient_condition = request.form['patient_condition']
    doctor_id = request.form['doctor_id']
    doctor_name = request.form['doctor_name']

    sql = SQL_Server()

    insertSQL1 = "('{}', '{}', '{}')".format(patient_id, patient_name, patient_gender)
    registration_id = sql.generate_id('registration', 'registration_id')
    doctor_visits_id = sql.generate_id('doctor_visits', 'doctor_visits_id')
    insertSQL2 = "('{}', '{}','{}', '{}')".format(doctor_visits_id, doctor_id, patient_id, patient_condition)
    insertSQL3 = "('{}','{}')".format(registration_id, doctor_visits_id)


    # do insertion
    SF1 = sql.insertIntoTable('registered_user', insertSQL1)
    SF2 = sql.insertIntoTable('doctor_visits', insertSQL2)
    SF3 = sql.insertIntoTable('registration', insertSQL3)
    print("sql1:",  insertSQL1)
    print("sql2:",  insertSQL2)
    print("sql3:",  insertSQL3)


    if SF2 == 'Succeeded' and SF3 == 'Succeeded':
        SF = 'Succeeded'
    else:
        SF = 'Failed'

    attribute = ' '
    selected_option = ' '
    results = sql.selectFromTable(table, selected_option, attribute) or []
    attributeList = sql.getAttributeListForSelectShow('doctor_visits', '*')
    if len(results) != 0:
        col = len(results[0])
    else:
        col = 0
    return render_template('developer_select_result.html', table=table, attributeList=attributeList, results=results, attribute=attribute, row=len(results), col=col, SF=SF)

@app.route('/developer', methods=['GET', 'POST'])
def developerPanel():
    """detect developer's password"""
    # if (username password) not correct
    global username, password
    sql = SQL_Server()
    sql.getTableList()
    sql.getAttributeList()
    tableList = sql.tableList
    attributeList = sql.attributeList
    # else login succeed
    return render_template('developer.html', user=username, tableList=tableList, attributeList=attributeList, tableLen=len(tableList))

@app.route('/developer/select', methods=['GET', 'POST'])
def selectPanel():
    """detect the table which is to be selected"""
    global table
    table = request.form['table']
    sql = SQL_Server()
    # detect if the table is in db
    if not sql.tableDetect(table):
        # exceptions.BadRequestKeyError here
        return redirect('/developer')
    attributeList = sql.getAttributeListOfTable(table)
    return render_template('developer_select.html', table=table, attributeList=attributeList, attributeLen=len(attributeList))

@app.route('/developer/select/result', methods=['GET', 'POST'])
def selectResult():
    """show select option result"""
    global table
    attribute = request.form['attribute']
    selected_option = request.form['selected_option']

    sql = SQL_Server()
    print("table: ", table)
    print("attribute: ", attribute)
    print("selected_option: ", selected_option)
    results = sql.selectFromTable(table, selected_option, attribute) or []
    print("result: ", results)
    attributeList = sql.getAttributeListForSelectShow(table, attribute)
    if len(results) != 0:
        col = len(results[0])
    else:
        col = 0
    return render_template('developer_select_result.html', table=table, attributeList=attributeList, results=results, attribute=attribute, row=len(results), col=col)

@app.route('/developer/insert', methods=['GET', 'POST'])
def insertPanel():
    """detect the table which is to be inserted"""
    global table
    table = request.form['table']
    sql = SQL_Server()
    # detect if the table is in db
    if not sql.tableDetect(table):
        # exceptions.BadRequestKeyError here
        return redirect('/developer')
    attribute = ' '
    selected_option = ' '
    results = sql.selectFromTable(table, selected_option, attribute)
    attributeList = sql.getAttributeListOfTable(table)
    if len(results) != 0:
        col = len(results[0])
    else:
        col = 0
    return render_template('developer_insert.html', table=table, attributeList=attributeList, results=results, attribute=attribute, row=len(results), col=col, attributeLen=len(attributeList))

@app.route('/developer/insert/result', methods=['GET', 'POST'])
def insertResult():
    """show result after insertion"""
    global table
    sql = SQL_Server()
    insertSQL = request.form['insertSQL']
    print("insert: ", insertSQL)
    # do insertion
    SF = sql.insertIntoTable(table, insertSQL)
    attribute = ' '
    selected_option = ' '
    results = sql.selectFromTable(table, selected_option, attribute)
    attributeList = sql.getAttributeListForSelectShow(table, attribute)
    if len(results) != 0:
        col = len(results[0])
    else:
        col = 0
    return render_template('developer_insert_result.html', table=table, attributeList=attributeList, results=results, attribute=attribute, row=len(results), col=col, SF=SF)

@app.route('/developer/delete', methods=['GET', 'POST'])
def deletePanel():
    """detect the table which is to be inserted"""
    global table
    table = request.form['table']
    sql = SQL_Server()
    # detect if the table is in db
    if not sql.tableDetect(table):
        # exceptions.BadRequestKeyError here
        return redirect('/developer')
    attribute = ' '
    selected_option = ' '
    results = sql.selectFromTable(table, selected_option, attribute)
    attributeList = sql.getAttributeListOfTable(table)
    if len(results) != 0:
        col = len(results[0])
    else:
        col = 0
    return render_template('developer_delete.html', table=table, attributeList=attributeList, results=results, attribute=attribute, row=len(results), col=col, attributeLen=len(attributeList))

@app.route('/developer/delete/result', methods=['GET', 'POST'])
def deleteResult():
    """show result after deletion"""
    global table
    sql = SQL_Server()
    deleteSQL = request.form['deleteSQL']
    # do deletion
    SF = sql.deleteFromUserTable(table, deleteSQL)
    attribute = ' '
    selected_option = ' '
    results = sql.selectFromTable(table, selected_option, attribute)
    attributeList = sql.getAttributeListForSelectShow(table, attribute)
    if len(results) != 0:
        col = len(results[0])
    else:
        col = 0
    return render_template('developer_delete_result.html', table=table, attributeList=attributeList, results=results, attribute=attribute, row=len(results), col=col, SF=SF)

@app.route('/developer/drop', methods=['GET', 'POST'])
def dropPanel():
    """detect the table which is to be inserted"""
    table = request.form['table']
    sql = SQL_Server()
    # detect if the table is in db
    if not sql.tableDetect(table):
        # exceptions.BadRequestKeyError here
        return redirect('/developer')
    SF = sql.dropTable(table)
    return render_template('developer_drop.html', table=table, SF=SF)
