import datetime
import icalendar
import json
import pytz
import sys

TZ_NAME = 'Europe/Paris'
TZ_DST = True

def main(json_filename: str, ical_filename: str):
    with open(json_filename, 'r') as fs:
        json_data = json.load(fs)

    cal = icalendar.Calendar()
    tz = pytz.timezone(TZ_NAME)

    for json_item in json_data['results']:
        date = datetime.datetime.fromisoformat(json_item['date_passage'])
        closing_time = datetime.time.fromisoformat(json_item['fermeture_a_la_circulation'])
        closing_dt = tz.localize(datetime.datetime.combine(date, closing_time), is_dst=TZ_DST)
        reopening_time = datetime.time.fromisoformat(json_item['re_ouverture_a_la_circulation'])
        reopening_dt = tz.localize(datetime.datetime.combine(date, reopening_time), is_dst=TZ_DST)

        cal_event = icalendar.Event()
        cal_event.add('summary', json_item['bateau'])
        cal_event.add('dtstart', closing_dt)
        cal_event.add('dtend', reopening_dt)
        cal.add_component(cal_event)

    with open(ical_filename, 'wb') as fs:
        fs.write(cal.to_ical())


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
