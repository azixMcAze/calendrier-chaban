from collections import namedtuple
from flask import Flask
import datetime
import icalendar
import json
import pytz
import urllib.request


API_URL = 'https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records?limit=20'

TZ_NAME = 'Europe/Paris'
TZ_DST = True

ClosureItem = namedtuple('ClosureItem', ['name', 'closingTime', 'reopeningTime'])

tz = pytz.timezone(TZ_NAME)
app = Flask(__name__) 


def parse_boat_closure(json_item: dict):
    date = datetime.datetime.fromisoformat(json_item['date_passage'])
    closing_time = datetime.time.fromisoformat(json_item['fermeture_a_la_circulation'])
    closing_dt = tz.localize(datetime.datetime.combine(date, closing_time), is_dst=TZ_DST)
    reopening_time = datetime.time.fromisoformat(json_item['re_ouverture_a_la_circulation'])
    reopening_dt = tz.localize(datetime.datetime.combine(date, reopening_time), is_dst=TZ_DST)

    return ClosureItem(name=json_item['bateau'], closingTime=closing_dt, reopeningTime=reopening_dt)


def create_calendar_item(closure_item: ClosureItem):
    cal_event = icalendar.Event()
    cal_event.add('summary', closure_item.name)
    cal_event.add('dtstart', closure_item.closingTime)
    cal_event.add('dtend', closure_item.reopeningTime)

    return cal_event


def create_cal_from_json(json_data : dict):
    cal = icalendar.Calendar()
    
    for json_item in json_data['results']:
        closure_item = parse_boat_closure(json_item)
        cal_event = create_calendar_item(closure_item)
        cal.add_component(cal_event)

    return cal


def get_json_from_file(filename: str):
    with open(filename, 'r') as fs:
        return json.load(fs)


def get_json_from_url(url: str):
    request = urllib.request.urlopen(url)
    contents = request.read()
    return json.loads(contents)


@app.route('/')
def calendar():
    json_data = get_json_from_url(API_URL)
    cal = create_cal_from_json(json_data)
    return cal.to_ical()


if __name__ == '__main__':
    app.run(debug=True)
