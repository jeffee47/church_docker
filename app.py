from flask import Flask
import pymysql
import json
import traceback
import os
import re

app = Flask(__name__)

def source_env(f=".env",keyfilter=[]):
    lines = []
    envdata = {} 
    with open(f,"r") as fh:
        tmplines = [x.strip() for x in fh.readlines()]
        for line in tmplines:
            line = re.sub(r'#.*', '', line)
            if line.strip() == '': continue
            k,v = line.split("=",1)
            if keyfilter:
                if k not in keyfilter:
                    continue
            envdata[k] = v
    return envdata

@app.route('/')
def hello_world():
     return 'This is a Python Flask Application with redis and accessed through Nginx'

@app.route('/sermons')
def sermons():
    dbopts = source_env(".env",["user","password","host","db"])
    con = pymysql.connect(**dbopts)
    cursor = con.cursor()
    try:
        SQL = """SELECT id,title,book,summary,link,sermondate FROM sermons ORDER BY sermondate DESC"""
        cursor.execute(SQL)
        rows = cursor.fetchall()
        newrows = []
        for tmpdata in rows:
            try:
                tmp = list(tmpdata)
                tmpdate = tmp[-1].isoformat()
                tmp[-1] = tmpdate
                ddata = {
			'id' : tmp[0],
			'title' : tmp[1],
			'book' : tmp[2],
			'summary' : tmp[3],
			'link' : tmp[4],
			'sermondate' : tmp[5],
                }
                newrows.append(ddata)
            except Exception as e: 
                #traceback.print_exc()
                pass
        return json.dumps(newrows)
    except Exception as e:
        traceback.print_exc()
    finally:
        cursor.close()
        con.close()
    return json.dumps([])

        

#@app.route('/visitor')
#def visitor():
#     redis.incr('visitor')
#     visitor_num = redis.get('visitor').decode("utf-8")
#     return "Visit Number = : %s" % (visitor_num)
#@app.route('/visitor/reset')
#def reset_visitor():
#    redis.set('visitor', 0)
#    visitor_num = redis.get('visitor').decode("utf-8") 
#    return "Visitor Count has been reset to %s" % (visitor_num)