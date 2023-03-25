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
#-----------------------------------------------------------------------
app = flask.Flask(__name__)
#-----------------------------------------------------------------------


@app.route('/', methods =['GET'])
@app.route('/searchresults',methods=['GET'])
def search_results():
    dept = flask.request.args.get('dept')
    num = flask.request.args.get('number')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')
    search = ds.DatabaseSearch()
    rawsearch = search.fullsearch(idept=dept,icoursenum=num,
    iarea=area, ititle=title)
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
    classid = flask.request.url.split('?')[1]
    wrapper = tw.TextWrapper(width = 72, break_long_words=True)
    search = cs.ClassSearch(classid)
    general= search.get_general()
    deptandnum = search.get_deptandnum()
    profs = search.get_prof()
    course_id = general[0]
    days = general[1]
    starttime = general[2]
    endtime = general[3]
    building = general[4]
    room = general[5]
    area = general[6]
    title = general[7]
    title = wrapper.wrap(title)
    description = general[8]
    description = wrapper.wrap(description)
    prereqs = general[9]
    prereqs = wrapper.wrap(prereqs)
    html_code = flask.render_template('regdetails.html',
        classid=classid,days=days,start_time=starttime,
        end_time=endtime,building=building,room=room,
        course_id=course_id,dept_and_nums=deptandnum,
        area=area,title=title,description=description,
        professors=profs,prereqs=prereqs)
    response = flask.make_response(html_code)
    return response