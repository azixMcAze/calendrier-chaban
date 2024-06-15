from flask import Flask, Response
import bridge_json_utils
import calendar_utils
import chaban_calendar
import urllib.request


app = Flask(__name__) 

@app.route('/')
def calendar():
    request = urllib.request.urlopen(bridge_json_utils.API_URL)
    json_text = request.read()
    cal_text = chaban_calendar.convert_json_to_cal(json_text)
    return Response(cal_text, calendar_utils.CAL_MIME_TYPE)
