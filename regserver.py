# -------------------------------------------
# regserver.py
# Authors: Sam Liang and Sumanth Maddirala
# -------------------------------------------

from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from database import Database

# -------------------------------------------

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    dept = request.args.get('dept')
    number = request.args.get('number')
    area = request.args.get('area')
    title = request.args.get('title')

    if dept is None:
        dept = ''
    if number is None:
        number = ''
    if area is None:
        area = ''
    if title is None:
        title = ''

    form_args = [dept, number, area, title]
    error_msg = ""
    try:
        database = Database()
        database.connect()
        rows = database.search(form_args)
        database.disconnect()
    except Exception as e:
        error_msg = e

    html = render_template('index.html', error_msg=error_msg, dept=dept,
                           number=number, area=area, title=title, rows=rows)
    response = make_response(html)
    response.set_cookie('prev_dept', dept)
    response.set_cookie('prev_num', number)
    response.set_cookie('prev_area', area)
    response.set_cookie('prev_title', title)
    return response


@app.route('/classdetails', methods=['GET'])
def class_details():
    classid = request.args.get('classid').strip()
    is_int = True

    try:
        int(classid)
    except:
        is_int = False

    prev_dept = request.cookies.get('prev_dept')
    prev_num = request.cookies.get('prev_num')
    prev_area = request.cookies.get('prev_area')
    prev_title = request.cookies.get('prev_title')

    if prev_dept is None:
        prev_dept = ''
    if prev_num is None:
        prev_num = ''
    if prev_area is None:
        prev_area = ''
    if prev_title is None:
        prev_title = ''

    error_msg = ""
    try:
        database = Database()
        database.connect()
        results = database.class_details(classid)
        database.disconnect()
    except Exception as e:
        error_msg = e

    html = render_template('classdetails.html', error_msg=error_msg, is_int=is_int, results=results, classid=classid,
                           prev_dept=prev_dept, prev_num=prev_num, prev_area=prev_area, prev_title=prev_title)

    # html = render_template('classdetails.html', results=results, classid=classid, courseid=results['courseid'], days=results['days'], start=results['start'], end=results['end'], building=results['building'],
    #                        room=results['room'], dept_nums=results['dept_num'], area=results['area'], title=results['title'], desc=results['desc'], prereq=results['prereq'], profs=results['profs'], prev_dept=prev_dept, prev_num=prev_num, prev_area=prev_area, prev_title=prev_title)
    response = make_response(html)
    return response
