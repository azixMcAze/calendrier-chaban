from calendar_data import CAL_MIME_TYPE
from chaban import get_json_from_url
from flask import Flask, Response
import chaban_calendar


app = Flask(__name__) 

@app.route('/')
def calendar():
    json_text = get_json_from_url()
    cal_text = chaban_calendar.convert_json_to_cal(json_text)
    return Response(cal_text, CAL_MIME_TYPE)
