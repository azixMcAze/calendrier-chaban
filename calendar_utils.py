import datetime
import re
from typing import Iterable

import icalendar

from bridge_json_utils import BridgeEvent


CAL_MIME_TYPE = 'text/calendar'
UID_DOMAIN = 'chaban-calendar'
EVENT_SUMMARY_FORMAT = 'Fermeture du pont Chaban-Delmas ({name})'


def compute_uid(bridge_event: BridgeEvent):
    sanitized_name = re.sub(r'\W+|^(?=\d)','_', bridge_event.name)
    time_utc = bridge_event.start_time.astimezone(datetime.timezone.utc)
    return f'{time_utc:%Y%m%dT%H%M%S}_{sanitized_name}@{UID_DOMAIN}'


def create_calendar_item(bridge_event: BridgeEvent) -> icalendar.Event:
    ical_event = icalendar.Event()
    ical_event.add('summary', EVENT_SUMMARY_FORMAT.format(name=bridge_event.name))
    ical_event.add('dtstart', bridge_event.start_time)
    ical_event.add('dtend', bridge_event.duration)
    ical_event.add('uid', compute_uid(bridge_event))

    return ical_event


def create_cal_from_json(bridge_event_list: Iterable[BridgeEvent]) -> icalendar.Calendar:
    cal = icalendar.Calendar()
    
    for bridge_event in bridge_event_list:
        cal_event = create_calendar_item(bridge_event)
        cal.add_component(cal_event)

    return cal
