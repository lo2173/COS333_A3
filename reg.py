#-----------------------------------------------------------------------
# Author: Lois I Omotara
# reg.py
# []need to ask how to get cookies: set cookie
#-----------------------------------------------------------------------
import html
import flask
import databasesearch as ds
import classsearch as cs
import line
import textwrap as tw
import sys
#-----------------------------------------------------------------------
app = flask.Flask(__name__)
#-----------------------------------------------------------------------


@app.route('/', methods =['GET'])
def search_results():
    source = flask.request.url
    if source.find('?')<0:
        dept = flask.request.args.get('dept')
        num = flask.request.args.get('number')
        area = flask.request.args.get('area')
        title = flask.request.args.get('title')
    else:
        request = source.split('?')[1].split('&')
        dept = str(request[0].split('=')[1])
        num = str(request[1].split('=')[1])
        area = str(request[2].split('=')[1])
        title=str(request[3].split('=')[1])
    try:
        search = ds.DatabaseSearch()
        rawsearch = search.fullsearch(idept=dept,icoursenum=num,
        iarea=area, ititle=title)
    except Exception as ex:
        print(ex,file=sys.stderr)
        html_code=flask.render_template('errorpage.html',
            type_error = 'A server error occured. Please contact the system adminstrator')
        return flask.make_response(html_code)
    course_results_ = []
    for row in rawsearch:
        course_results_.append(line.LineParser(row))
    if dept is None:
        dept = ''
    if num is None:
        num = ''
    if area is None:
        area = ''
    if title is None:
        title = ''
    html_code = flask.render_template('searchresults.html',
        course_results = course_results_,
        dept = dept,
        num = num,
        area = area,
        title = title)
    response = flask.make_response(html_code)
    response.set_cookie('deptcookie',dept)
    response.set_cookie('numcookie',num)
    response.set_cookie('areacookie',area)
    response.set_cookie('titlecookie',title)
    return response

@app.route('/regdetails',methods=['GET'])
def regdetails():
    prev_dept = flask.request.cookies.get('deptcookie')
    prev_num = flask.request.cookies.get('numcookie')
    prev_area = flask.request.cookies.get('areacookie')
    prev_title = flask.request.cookies.get('titlecookie')
    try:
        classid = flask.request.url.split('=')[1]
    except IndexError:
        html_code = flask.render_template('errorpage.html',
            type_error = 'Missing Classid')
        return flask.make_response(html_code)
    try:
        classid = int(classid)
    except ValueError:
        html_code = flask.render_template('errorpage.html',
            type_error = 'Non-Integer Classid')
        return flask.make_response(html_code)
    #wrapper = tw.TextWrapper(width = 72, break_long_words=True)

    try:
        search = cs.ClassSearch(classid)
        general= search.get_general()
        if bool(general) is False:
            html_code = flask.render_template('errorpage.html',
                type_error = 'Non-Exisiting Classid')
            return flask.make_response(html_code)
        general = general[0]
        deptandnums = search.get_deptandnum()
    except Exception as ex:
        print(ex,file=sys.stderr)
        html_code=flask.render_template('errorpage.html',
            type_error = 'A server error occured. Please contact the system adminstrator')
        return flask.make_response(html_code)
    deptandnum =[]
    for line in deptandnums:
        deptandnum.append(line[0]+' '+line[1])
    professors = search.get_prof()
    profs = []
    for line in professors:
        profs.append(line[0])
    course_id = general[0]
    days = general[1]
    starttime = general[2]
    endtime = general[3]
    building = general[4]
    room = general[5]
    area = general[6]
    title = general[7]
    #title = wrapper.wrap(title)
    description = general[8]
    #description = wrapper.wrap(description)
    prereqs = general[9]
    #prereqs = wrapper.wrap(prereqs)
    html_code = flask.render_template('regdetails.html',
        class_id=classid,days=days,start_time=starttime,
        end_time=endtime,building=building,room=room,
        course_id=course_id,dept_and_nums=deptandnum,
        area=area,title=title,description=description,
        professors=profs,prereqs=prereqs,prev_dept=prev_dept,
        prev_num=prev_num,prev_area=prev_area,prev_title=prev_title)
    response = flask.make_response(html_code)
    return response