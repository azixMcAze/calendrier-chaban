import icalendar

CAL_MIME_TYPE = 'text/calendar'
UID_DOMAIN = 'chaban-calendar'


def compute_uid(closure_item):
    return f'{closure_item.closingTime.isoformat()}_{closure_item.name}@{UID_DOMAIN}'


def create_calendar_item(closure_item):
    cal_event = icalendar.Event()
    cal_event.add('summary', closure_item.name + ' 3')
    cal_event.add('dtstart', closure_item.closingTime)
    cal_event.add('dtend', closure_item.reopeningTime)
    cal_event.add('uid', compute_uid(closure_item))

    return cal_event


def create_cal_from_json(closure_items_list):
    cal = icalendar.Calendar()
    
    for closure_item in closure_items_list:
        cal_event = create_calendar_item(closure_item)
        cal.add_component(cal_event)

    return cal


def write_cal_to_file(cal, filename: str):
    with open(filename, 'wb') as fs:
        fs.write(cal.to_ical())
