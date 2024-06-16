from bridge_json_utils import parse_bridge_json_data, combine_date_and_times, BridgeEvent
from calendar_utils import create_cal_from_json
from datetime import time, date
from datetimerange import DateTimeRange
from typing import Optional, Iterable
import json

DayFilterType = list[bool]
TimeRangeType = tuple[time, time]
TimeFilterType = list[TimeRangeType]

DAYS_COUNT = 7


def day_filter_predicate(bridge_event: BridgeEvent, day_filter: Optional[DayFilterType]):
    if day_filter is None:
        return True
    else:
        return day_filter[bridge_event.closingTime.weekday()]


def convert_hour_filter_to_range(time_couple: TimeRangeType, event_date: date):
    (start_dt, end_dt) = combine_date_and_times(event_date, time_couple[0], time_couple[1])
    return DateTimeRange(start_dt, end_dt)


def hours_filter_predicate(bridge_event: BridgeEvent, time_filter: Optional[TimeFilterType]):
    if time_filter is None:
        return True
    
    event_date = bridge_event.closingTime.date()

    time_filter_ranges = [convert_hour_filter_to_range(time_couple, event_date) for time_couple in time_filter]
    bridge_time_range = DateTimeRange(bridge_event.closingTime, bridge_event.reopeningTime)

    return any(time_filter_range.is_intersection(bridge_time_range) for time_filter_range in time_filter_ranges)


def filter_by_day(bridge_data: Iterable[BridgeEvent], day_filter: Optional[DayFilterType], time_filter: Optional[TimeFilterType]):
    if day_filter is not None or time_filter is not None:
        assert(day_filter is None or len(day_filter) == DAYS_COUNT)
        return (bridge_event
                    for bridge_event in bridge_data
                    if day_filter_predicate(bridge_event, day_filter) and hours_filter_predicate(bridge_event, time_filter))
    else:
        return bridge_data


def convert_json_to_cal(json_text: str, day_filter: Optional[DayFilterType] = None, time_filter: Optional[TimeFilterType] = None) -> bytes:
    json_data = json.loads(json_text)
    bridge_data = parse_bridge_json_data(json_data)
    bridge_data = filter_by_day(bridge_data, day_filter, time_filter)
    cal = create_cal_from_json(bridge_data)

    return cal.to_ical()
