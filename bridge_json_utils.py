from datetime import date, time

from bridge_event import BridgeEvent, combine_date_and_times


def parse_bridge_json_item(json_item: dict) -> BridgeEvent:
    event_date = date.fromisoformat(json_item['date_passage'])
    start_time = time.fromisoformat(json_item['fermeture_a_la_circulation'])
    end_time = time.fromisoformat(json_item['re_ouverture_a_la_circulation'])

    (start_dt, duration) = combine_date_and_times(event_date, start_time, end_time)

    return BridgeEvent(name=json_item['bateau'], start_time=start_dt, duration=duration)


def parse_bridge_json_data(json_data: dict) -> list[BridgeEvent]:
    bridge_data = [parse_bridge_json_item(json_item) for json_item in json_data['results']]
    
    return sorted(bridge_data, key=lambda item: item.start_time)
