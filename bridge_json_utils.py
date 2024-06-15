from dataclasses import dataclass
import datetime
import pytz


API_URL = 'https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records?limit=100'
TZ_NAME = 'Europe/Paris'
TZ_DST = True

tz = pytz.timezone(TZ_NAME)

@dataclass
class BridgeEvent:
    name: str
    closingTime: datetime.datetime
    reopeningTime: datetime.datetime


def parse_bridge_json_item(json_item: dict) -> BridgeEvent:
    date = datetime.datetime.fromisoformat(json_item['date_passage'])
    closing_time = datetime.time.fromisoformat(json_item['fermeture_a_la_circulation'])
    closing_dt = tz.localize(datetime.datetime.combine(date, closing_time), is_dst=TZ_DST)
    reopening_time = datetime.time.fromisoformat(json_item['re_ouverture_a_la_circulation'])
    reopening_dt = tz.localize(datetime.datetime.combine(date, reopening_time), is_dst=TZ_DST)

    return BridgeEvent(name=json_item['bateau'], closingTime=closing_dt, reopeningTime=reopening_dt)


def parse_bridge_json_data(json_data: dict) -> list[BridgeEvent]:
    return (parse_bridge_json_item(json_item) for json_item in json_data['results'])
