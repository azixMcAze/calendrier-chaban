from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Iterable, Optional

from datetimerange import DateTimeRange
import pytz


@dataclass
class BridgeEvent:
    name: str
    start_time: datetime
    duration: timedelta

DayFilterType = list[bool]
TimeRangeType = tuple[time, time]
TimeFilterType = list[TimeRangeType]

DAYS_COUNT = 7
TZ_NAME = 'Europe/Paris'
TZ_DST = True

tz = pytz.timezone(TZ_NAME)


def combine_date_and_times(common_date: date, start_time: time, end_time: time):
    if start_time <= end_time:
        day_offset = 0
    else:
        day_offset = 1

    start_dt = tz.localize(datetime.combine(common_date, start_time))
    end_dt = tz.localize(datetime.combine(common_date + timedelta(days=day_offset), end_time))
    duration = end_dt - start_dt

    return (start_dt, duration)


def day_filter_predicate(bridge_event: BridgeEvent, day_filter: Optional[DayFilterType]):
    if day_filter is None:
        return True
    else:
        return day_filter[bridge_event.start_time.weekday()]


def convert_hour_filter_to_range(time_couple: TimeRangeType, event_date: date):
    (start_dt, duration) = combine_date_and_times(event_date, time_couple[0], time_couple[1])
    return DateTimeRange(start_dt, start_dt + duration)


def hours_filter_predicate(bridge_event: BridgeEvent, time_filter: Optional[TimeFilterType]):
    if time_filter is None:
        return True
    
    event_date = bridge_event.start_time.date()

    time_filter_ranges = [convert_hour_filter_to_range(time_couple, event_date) for time_couple in time_filter]
    bridge_time_range = DateTimeRange(bridge_event.start_time, bridge_event.start_time + bridge_event.duration)

    return any(time_filter_range.is_intersection(bridge_time_range) for time_filter_range in time_filter_ranges)


def filter_by_day(bridge_data: Iterable[BridgeEvent], day_filter: Optional[DayFilterType], time_filter: Optional[TimeFilterType]):
    if day_filter is not None or time_filter is not None:
        assert(day_filter is None or len(day_filter) == DAYS_COUNT)
        return (bridge_event
                    for bridge_event in bridge_data
                    if day_filter_predicate(bridge_event, day_filter) and hours_filter_predicate(bridge_event, time_filter))
    else:
        return bridge_data
