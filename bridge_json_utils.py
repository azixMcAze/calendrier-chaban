from dataclasses import dataclass
from datetime import datetime, timedelta, time, date
import pytz


TZ_NAME = 'Europe/Paris'
TZ_DST = True

tz = pytz.timezone(TZ_NAME)

@dataclass
class BridgeEvent:
    name: str
    start_time: datetime
    duration: timedelta


def combine_date_and_times(common_date: date, start_time: time, end_time: time):
    if start_time <= end_time:
        day_offset = 0
    else:
        day_offset = 1

    start_dt = tz.localize(datetime.combine(common_date, start_time))
    end_dt = tz.localize(datetime.combine(common_date + timedelta(days=day_offset), end_time))
    duration = end_dt - start_dt

    return (start_dt, duration)


def parse_bridge_json_item(json_item: dict) -> BridgeEvent:
    event_date = date.fromisoformat(json_item['date_passage'])
    start_time = time.fromisoformat(json_item['fermeture_a_la_circulation'])
    end_time = time.fromisoformat(json_item['re_ouverture_a_la_circulation'])

    (start_dt, duration) = combine_date_and_times(event_date, start_time, end_time)

    return BridgeEvent(name=json_item['bateau'], start_time=start_dt, duration=duration)


def parse_bridge_json_data(json_data: dict) -> list[BridgeEvent]:
    return [parse_bridge_json_item(json_item) for json_item in json_data['results']]
