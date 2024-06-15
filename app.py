from bridge_json_utils import API_URL
from calendar_utils import CAL_MIME_TYPE
from flask import Flask, Response
import chaban_calendar
import urllib.request


app = Flask(__name__) 

@app.route('/')
def calendar():
    request = urllib.request.urlopen(API_URL)
    json_text = request.read()
    cal_text = chaban_calendar.convert_json_to_cal(json_text)
    return Response(cal_text, CAL_MIME_TYPE)
