from flask import Flask, Response, request
import calendar_utils
import chaban_calendar

DAYS_LETTERS = ['L', 'Ma', 'Me', 'J', 'V', 'S', 'D']
JSON_FILENAME = 'records.json'

app = Flask(__name__) 

@app.route('/chaban.ics')
def calendar():
    days = request.args.get('jours')
    day_filter = parse_day_filter(days) if days else None

    with open(JSON_FILENAME, 'r') as fs:
        json_text = fs.read()

    cal_text = chaban_calendar.convert_json_to_cal(json_text, day_filter=day_filter)

    return Response(cal_text, mimetype=calendar_utils.CAL_MIME_TYPE)


def parse_day_filter(days: str):
    day_filter = set()
    for day_num, day_letter in enumerate(DAYS_LETTERS):
        if day_letter in days:
            day_filter.add(day_num)

    return day_filter

