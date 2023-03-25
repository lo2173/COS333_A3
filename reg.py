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
#-----------------------------------------------------------------------
app = flask.Flask(__name__)
#-----------------------------------------------------------------------


@app.route('/', methods =['GET'])
@app.route('/searchresults',methods=['GET'])
def search_results():
    #prev_dept= flask.request.cookies.get('deptcookie')
    #prev_num = flask.request.cookies.get('numcookie')
    #prev_area = flask.request.cookies.get('areacookie')
    #prev_title = flask.request.cookies.get('titlecookie')
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
    #if dept is not None:
     #   response.set_cookie('deptcookie',dept)
    #if num is not None:
      #  response.set_cookie('numcookie',num)
    #if area is not None:
     #   response.set_cookie('areacookie',area)
    #if title is not None:
    #    response.set_cookie('titlecookie',title)
    return response
#@app.route('/classresult',methods=['GET'])
