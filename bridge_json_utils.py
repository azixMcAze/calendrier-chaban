from dataclasses import dataclass
from datetime import datetime, timedelta, time, date
import pytz


API_URL = 'https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records?limit=100'
TZ_NAME = 'Europe/Paris'
TZ_DST = True

tz = pytz.timezone(TZ_NAME)

@dataclass
class BridgeEvent:
    name: str
    closingTime: datetime
    reopeningTime: datetime


def combine_date_and_times(common_date: date, start_time: time, end_time: time):
    if start_time < end_time:
        day_offset = 0
    else:
        day_offset = 1

    start_dt = tz.localize(datetime.combine(common_date, start_time))
    end_dt = tz.localize(datetime.combine(common_date + timedelta(days=day_offset), end_time))

    return (start_dt, end_dt)


def parse_bridge_json_item(json_item: dict) -> BridgeEvent:
    event_date = date.fromisoformat(json_item['date_passage'])
    closing_time = time.fromisoformat(json_item['fermeture_a_la_circulation'])
    reopening_time = time.fromisoformat(json_item['re_ouverture_a_la_circulation'])

    (closing_dt, reopening_dt) = combine_date_and_times(event_date, closing_time, reopening_time)

    return BridgeEvent(name=json_item['bateau'], closingTime=closing_dt, reopeningTime=reopening_dt)


def parse_bridge_json_data(json_data: dict) -> list[BridgeEvent]:
    return [parse_bridge_json_item(json_item) for json_item in json_data['results']]
