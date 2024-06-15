import json
from bridge_json_utils import parse_bridge_json_data,BridgeEvent
from calendar_utils import create_cal_from_json
from typing import Optional, Iterable


def day_filter_predicate(bridge_event: BridgeEvent, day_filter: set[int]):
    return bridge_event.closingTime.weekday() in day_filter


def filter_by_day(bridge_data: Iterable[BridgeEvent], day_filter: Optional[set[int]]):
    if day_filter is not None:
        return (bridge_event for bridge_event in bridge_data if day_filter_predicate(bridge_event, day_filter))
    else:
        return bridge_data


def convert_json_to_cal(json_text: str, day_filter: Optional[set[int]] = None) -> bytes:
    json_data = json.loads(json_text)
    bridge_data = parse_bridge_json_data(json_data)
    bridge_data = filter_by_day(bridge_data, day_filter)
    cal = create_cal_from_json(bridge_data)

    return cal.to_ical()
