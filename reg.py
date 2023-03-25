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
    dept = flask.request.args.get('dept')
    num = flask.request.args.get('number')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')
    search = ds.DatabaseSearch()
    rawsearch = search.fullsearch(idept=dept,icoursenum=num,
    iarea=area, ititle=title)
    course_results = []
    for row in rawsearch:
        course_results.append(line.LineParser(row))
    html_code = flask.render_template('searchresults.html')
#@app.route('/classresult',methods=['GET'])