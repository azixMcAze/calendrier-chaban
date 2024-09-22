from datetime import datetime
from flask import Flask, Response, request
from bridge_event import DayFilterType, filter_bridge_events
from bridge_json_utils import load_bridge_events, download_bridge_json, save_bridge_json
from calendar_utils import CAL_MIME_TYPE, create_cal_from_events

DAYS_LETTERS = ['L', 'Ma', 'Me', 'J', 'V', 'S', 'D']
app = Flask(__name__) 


@app.cli.command("download")
def download():
    json_data = download_bridge_json()
    save_bridge_json(json_data)


@app.route('/chaban.ics')
def calendar():
    day_filter_str = request.args.get('jours')
    time_filter_str = request.args.get('heures')

    day_filter = parse_day_filter(day_filter_str) if day_filter_str else None
    time_filter = parse_time_filter(time_filter_str) if time_filter_str else None

    bridge_data = load_bridge_events()
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
