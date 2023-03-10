from flask import Flask, render_template
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

def get_sermons_data():
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
                tmpdate = "%04d-%02d-%02d" % (tmp[-1].year,tmp[-1].month,tmp[-1].day)
                if tmp[-1].hour < 15:
                    tmpdate += " AM"
                else:
                    tmpdate += " PM"
                tmp[-1] = tmpdate
                href = ""
                try:
                    book,chapter = re.match(r'(.*?)\s+(\d+):', tmp[2]).groups()
                    chapter = int(chapter)
                    book = book.lower().strip()
                    book = re.sub(r'\s+','-',book)
                    href = "https://www.kingjamesbibleonline.org/%s-Chapter-%d/" % (book, chapter) 
                except Exception as e:
                    #traceback.print_exc()
                    pass
                ddata = {
			'id' : tmp[0],
			'title' : tmp[1],
			'book' : tmp[2],
			'summary' : tmp[3],
			'link' : "/" + os.path.basename(tmp[4]),
			'sermondate' : tmp[5],
			'href' : href,
                }
                newrows.append(ddata)
            except Exception as e: 
                #traceback.print_exc()
                pass
        return newrows
    except Exception as e:
        traceback.print_exc()
    finally:
        cursor.close()
        con.close()
    return []

@app.route('/')
def hello_world():
     return 'This is a Python Flask Application with redis and accessed through Nginx'

@app.route('/cgi-bin/sermons.py')
def get_sermons():
    sermons = get_sermons_data() 
    return render_template('sermons.html',sermons=sermons)
