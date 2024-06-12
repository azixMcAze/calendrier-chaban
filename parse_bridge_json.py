from chaban import get_json_from_url, parse_boat_closure, API_URL, ClosureItem
from flask import Flask
import icalendar


app = Flask(__name__) 


def create_calendar_item(closure_item: ClosureItem):
    cal_event = icalendar.Event()
    cal_event.add('summary', closure_item.name)
    cal_event.add('dtstart', closure_item.closingTime)
    cal_event.add('dtend', closure_item.reopeningTime)

    return cal_event


def create_cal_from_json(json_data : dict):
    cal = icalendar.Calendar()
    
    for json_item in json_data['results']:
        closure_item = parse_boat_closure(json_item)
        cal_event = create_calendar_item(closure_item)
        cal.add_component(cal_event)

    return cal


@app.route('/')
def calendar():
    json_data = get_json_from_url(API_URL)
    cal = create_cal_from_json(json_data)
    return cal.to_ical()


if __name__ == '__main__':
    app.run(debug=True)
