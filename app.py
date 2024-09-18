from datetime import datetime
import json
from flask import Flask, Response, request
from bridge_event import DayFilterType, filter_bridge_events
from bridge_json_utils import parse_bridge_events
from calendar_utils import CAL_MIME_TYPE, create_cal_from_events

DAYS_LETTERS = ['L', 'Ma', 'Me', 'J', 'V', 'S', 'D']
JSON_FILENAME = 'records.json'
API_URL = 'https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records?limit=100'

app = Flask(__name__) 


@app.cli.command("download")
def download():
    import urllib.request

    request = urllib.request.urlopen(API_URL)
    json_text = request.read().decode(request.headers.get_content_charset())
    json_text = json.dumps(json.loads(json_text), indent=4)
    with open(JSON_FILENAME, 'w') as fs:
        fs.write(json_text)


@app.route('/chaban.ics')
def calendar():
    day_filter_str = request.args.get('jours')
    time_filter_str = request.args.get('heures')

    day_filter = parse_day_filter(day_filter_str) if day_filter_str else None
    time_filter = parse_time_filter(time_filter_str) if time_filter_str else None

    with open(JSON_FILENAME, 'r') as fs:
        json_data = json.load(fs)

    bridge_data = parse_bridge_events(json_data)
    bridge_data = filter_bridge_events(bridge_data, day_filter, time_filter)
    cal_text = create_cal_from_events(bridge_data)

    return Response(cal_text, mimetype=CAL_MIME_TYPE)


def parse_day_filter(days: str) -> DayFilterType:
    return tuple(day_letter in days for day_letter in DAYS_LETTERS)


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
