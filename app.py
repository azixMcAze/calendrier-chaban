from datetime import datetime
from flask import Flask, Response, request
import calendar_utils
import chaban_calendar


DAYS_LETTERS = ['L', 'Ma', 'Me', 'J', 'V', 'S', 'D']
JSON_FILENAME = 'records.json'

app = Flask(__name__) 

@app.route('/chaban.ics')
def calendar():
    day_filter_str = request.args.get('jours')
    time_filter_str = request.args.get('heures')

    day_filter = parse_day_filter(day_filter_str) if day_filter_str else None
    time_filter = parse_time_filter(time_filter_str) if time_filter_str else None

    with open(JSON_FILENAME, 'r') as fs:
        json_text = fs.read()

    cal_text = chaban_calendar.convert_json_to_cal(json_text, day_filter=day_filter, time_filter=time_filter)

    return Response(cal_text, mimetype=calendar_utils.CAL_MIME_TYPE)


def parse_day_filter(days: str):
    day_filter = [False] * len(DAYS_LETTERS)

    for day_num, day_letter in enumerate(DAYS_LETTERS):
        if day_letter in days:
            day_filter[day_num] = True

    return day_filter


def parse_time(time_str: str):
    if len(time_str) == 3:
        time_str = '0' + time_str
    assert(len(time_str) == 4)

    return datetime.strptime(time_str, '%H%M').time()


def parse_time_range(time_range_str: str):
    times_str = time_range_str.split('-')
    assert(len(times_str) == 2)

    start_time = parse_time(times_str[0])
    end_time = parse_time(times_str[1])

    return (start_time, end_time)


def parse_time_filter(time_filter_str: str):
    return [
        parse_time_range(time_range_str)
        for time_range_str in time_filter_str.split(',')
    ]
