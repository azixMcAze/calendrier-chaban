from chaban import ClosureItem
import icalendar


def create_calendar_item(closure_item: ClosureItem):
    cal_event = icalendar.Event()
    cal_event.add('summary', closure_item.name)
    cal_event.add('dtstart', closure_item.closingTime)
    cal_event.add('dtend', closure_item.reopeningTime)

    return cal_event


def create_cal_from_json(closure_items_list):
    cal = icalendar.Calendar()
    
    for closure_item in closure_items_list:
        cal_event = create_calendar_item(closure_item)
        cal.add_component(cal_event)

    return cal