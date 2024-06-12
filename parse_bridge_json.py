from collections import namedtuple
import datetime
import icalendar
import json
import pytz
import sys

TZ_NAME = 'Europe/Paris'
TZ_DST = True

tz = pytz.timezone(TZ_NAME)

ClosureItem = namedtuple('ClosureItem', ['name', 'closingTime', 'reopeningTime'])


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


def main(json_filename: str, ical_filename: str):
    with open(json_filename, 'r') as fs:
        json_data = json.load(fs)

    cal = create_cal_from_json(json_data)

    with open(ical_filename, 'wb') as fs:
        fs.write(cal.to_ical())


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
