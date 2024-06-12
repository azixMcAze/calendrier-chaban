from collections import namedtuple
import datetime
import json
import pytz
import urllib.request


API_URL = 'https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records?limit=100'
TZ_NAME = 'Europe/Paris'
TZ_DST = True

ClosureItem = namedtuple('ClosureItem', ['name', 'closingTime', 'reopeningTime'])

tz = pytz.timezone(TZ_NAME)


def parse_boat_closure(json_item: dict):
    date = datetime.datetime.fromisoformat(json_item['date_passage'])
    closing_time = datetime.time.fromisoformat(json_item['fermeture_a_la_circulation'])
    closing_dt = tz.localize(datetime.datetime.combine(date, closing_time), is_dst=TZ_DST)
    reopening_time = datetime.time.fromisoformat(json_item['re_ouverture_a_la_circulation'])
    reopening_dt = tz.localize(datetime.datetime.combine(date, reopening_time), is_dst=TZ_DST)

    return ClosureItem(name=json_item['bateau'], closingTime=closing_dt, reopeningTime=reopening_dt)


def parse_json_data(json_data: dict):
    return (parse_boat_closure(json_item) for json_item in json_data['results'])


def get_json_from_url():
    request = urllib.request.urlopen(API_URL)
    contents = request.read()
    return json.loads(contents)


def get_json_from_file(filename: str):
    with open(filename, 'r') as fs:
        return json.load(fs)
