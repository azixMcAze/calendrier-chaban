from datetime import date, time
import json

from bridge_event import BridgeEvent, combine_date_and_times

JSON_FILENAME = 'records.json'
API_URL = 'https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records?limit=100'


def parse_bridge_json_item(json_item: dict) -> BridgeEvent:
    event_date = date.fromisoformat(json_item['date_passage'])
    start_time = time.fromisoformat(json_item['fermeture_a_la_circulation'])
    end_time = time.fromisoformat(json_item['re_ouverture_a_la_circulation'])

    (start_dt, duration) = combine_date_and_times(event_date, start_time, end_time)

    return BridgeEvent(name=json_item['bateau'], start_time=start_dt, duration=duration)


def parse_bridge_events(json_data: dict) -> list[BridgeEvent]:
    bridge_data = [parse_bridge_json_item(json_item) for json_item in json_data['results']]
    
    return sorted(bridge_data, key=lambda item: item.start_time)


def load_bridge_events():
    with open(JSON_FILENAME, 'r') as fs:
        json_data = json.load(fs)

    return parse_bridge_events(json_data)


def save_bridge_json(json_data):
    json_text = json.dumps(json_data, indent=4)
    with open(JSON_FILENAME, 'w') as fs:
        fs.write(json_text)


def download_bridge_json():
    import urllib.request

    request = urllib.request.urlopen(API_URL)
    json_text = request.read().decode(request.headers.get_content_charset())

    return json.loads(json_text)


def download_bridge_events():
    json_data = download_bridge_json()

    return parse_bridge_events(json_data)


