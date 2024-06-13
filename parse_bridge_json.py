from chaban import get_json_from_url, parse_json_data
from flask import Flask, Response
from calendar_data import create_cal_from_json, CAL_MIME_TYPE


app = Flask(__name__) 

@app.route('/')
def calendar():
    json_data = get_json_from_url()
    closure_items_list = parse_json_data(json_data)
    cal = create_cal_from_json(closure_items_list)
    cal_text = cal.to_ical()
    return Response(cal_text, CAL_MIME_TYPE)


if __name__ == '__main__':
    app.run(debug=True)
