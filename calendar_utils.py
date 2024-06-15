import datetime
import icalendar
import re
from bridge_json_utils import BridgeEvent
from typing import Iterable


CAL_MIME_TYPE = 'text/calendar'
UID_DOMAIN = 'chaban-calendar'
EVENT_SUMMARY_FORMAT = 'Pont Chaban-Delmas fermé à la circulation ({name})'

def compute_uid(closure_item):
    sanitized_name = re.sub(r'\W+|^(?=\d)','_', closure_item.name)
    time_utc = closure_item.closingTime.astimezone(datetime.timezone.utc)
    return f'{time_utc:%Y%m%dT%H%M%S}_{sanitized_name}@{UID_DOMAIN}'


def create_calendar_item(closure_item: BridgeEvent) -> icalendar.Event:
    cal_event = icalendar.Event()
    cal_event.add('summary', EVENT_SUMMARY_FORMAT.format(name=closure_item.name))
    cal_event.add('dtstart', closure_item.closingTime)
    cal_event.add('dtend', closure_item.reopeningTime)
    cal_event.add('uid', compute_uid(closure_item))

    return cal_event


def create_cal_from_json(closure_items_list: Iterable[BridgeEvent]) -> icalendar.Calendar:
    cal = icalendar.Calendar()
    
    for closure_item in closure_items_list:
        cal_event = create_calendar_item(closure_item)
        cal.add_component(cal_event)

    return cal
