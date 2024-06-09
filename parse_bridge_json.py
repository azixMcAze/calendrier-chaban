import json
import sys
import datetime
import pytz

TZ_NAME = 'Europe/Paris'
TZ_DST = True

def main(json_filename: str):
    with open(json_filename, 'r') as fs:
        json_data = json.load(fs)

    tz = pytz.timezone(TZ_NAME)

    for json_item in json_data['results']:
        date = datetime.datetime.fromisoformat(json_item['date_passage'])
        closing_time = datetime.time.fromisoformat(json_item['fermeture_a_la_circulation'])
        closing_dt = tz.localize(datetime.datetime.combine(date, closing_time), is_dst=TZ_DST)
        reopening_time = datetime.time.fromisoformat(json_item['re_ouverture_a_la_circulation'])
        reopening_dt = tz.localize(datetime.datetime.combine(date, reopening_time), is_dst=TZ_DST)

        print(closing_dt, reopening_dt)


if __name__ == '__main__':
    main(sys.argv[1])
