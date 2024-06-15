import json
from bridge_json_utils import parse_bridge_json_data
from calendar_utils import create_cal_from_json


def convert_json_to_cal(json_text: str):
    json_data = json.loads(json_text)
    closure_items_list = parse_bridge_json_data(json_data)
    cal = create_cal_from_json(closure_items_list)

    return cal.to_ical()