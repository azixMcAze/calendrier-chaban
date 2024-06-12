from chaban import get_json_from_url, parse_json_data, ClosureItem
from flask import Flask
from calendar_data import create_cal_from_json


app = Flask(__name__) 


@app.route('/')
def calendar():
    json_data = get_json_from_url()
    closure_items_list = parse_json_data(json_data)
    cal = create_cal_from_json(closure_items_list)
    return cal.to_ical()


if __name__ == '__main__':
    app.run(debug=True)
