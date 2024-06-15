from flask import Flask, Response
import calendar_utils
import chaban_calendar


JSON_FILENAME = 'records.json'

app = Flask(__name__) 

@app.route('/chaban.ics')
def calendar():
    with open(JSON_FILENAME, 'r') as fs:
        json_text = fs.read()
    cal_text = chaban_calendar.convert_json_to_cal(json_text)
    return Response(cal_text, mimetype=calendar_utils.CAL_MIME_TYPE)
