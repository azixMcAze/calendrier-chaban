from chaban import get_json_from_url, parse_json_data, ClosureItem
from flask import Flask
import icalendar


app = Flask(__name__) 


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


@app.route('/')
def calendar():
    json_data = get_json_from_url()
    closure_items_list = parse_json_data(json_data)
    cal = create_cal_from_json(closure_items_list)
    return cal.to_ical()


if __name__ == '__main__':
    app.run(debug=True)
