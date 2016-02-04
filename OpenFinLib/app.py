#!/usr/bin/env python
import os
from flask import Flask, render_template, redirect, url_for, abort, request
import time
import datetime
from workalendar.usa import *
from workalendar.europe import *
import json
from security import SecurityRef
from schedule import CSchedule

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] ='OpenFin'


usaholidays = UnitedStates()
franceholidays = France()
greeceholidays = Greece()
ukholidays = UnitedKingdom()

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
        raise TypeError("Type not Serializable")
    if isinstance(obj, datetime.date):
        serial = obj.isoformat()
        return serial
        raise TypeError("Type not Serializable")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/views/<path:filename>')
def getView(filename):
	return app.send_static_file('views/' + filename)

@app.route('/js/<path:filename>')
def getJsFile(filename):
	return app.send_static_file('js/' + filename)

@app.route('/css/<path:filename>')
def getCssFile(filename):
	return app.send_static_file('css/' + filename)

@app.route('/img/<path:filename>')
def getImgFile(filename):
	return app.send_static_file('img/' + filename)

@app.route('/country/<string:iso>/<int:year>', methods=['GET'])
def country(iso, year):
    result = []
    if iso == 'USA':
        for i in usaholidays.holidays(year):
            result.append({ 'date': i[0], 'name': i[1]})
        holiday = json.dumps(result,default=json_serial)
        return holiday
    elif iso == 'FRA':
        for i in franceholidays.holidays(year):
            result.append({ 'date': i[0], 'name': i[1]})
        holiday = json.dumps(result,default=json_serial)
        return holiday
    elif iso == 'GRE':
        for i in greeceholidays.holidays(year):
            result.append({ 'date': i[0], 'name': i[1]})
        holiday = json.dumps(result,default=json_serial)
        return holiday
    elif iso == 'GBR': 
        for i in ukholidays.holidays(year):
            result.append({ 'date': i[0], 'name': i[1]})
        holiday = json.dumps(result,default=json_serial)
        return holiday

@app.route('/schedule/<string:type>/<int:id>', methods=['GET'])
def schedule(type, id):
    securityinfo = SecurityRef().get(type,id)
    print(securityinfo)
    dates = CSchedule().get_schedule(securityinfo)
    return json.dumps(list(dates), default=json_serial) 
    

@app.route('/securityschedule/<string:type>/<int:id>', methods=['GET'])
def securityschedule(type, id):
    return json.dumps(SecurityRef().get(type,id), default=json_serial)

@app.route('/cschedule', methods=['PUT', 'POST'])
def security():
    input_params = json.loads(request.data)
    result =CSchedule().get(input_params)
    return json.dumps(result, default=json_serial)



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 8000))
	app.run(host='0.0.0.0', port=8000, debug=True)
