import sys
from chaban import get_json_from_file, parse_json_data
from calendar_data import create_cal_from_json, write_cal_to_file


def main(json_filename: str, ical_filename: str):
    json_data = get_json_from_file(json_filename)
    closure_items_list = parse_json_data(json_data)
    cal = create_cal_from_json(closure_items_list)
    write_cal_to_file(cal, ical_filename)


if __name__ == '__main__':
    if sys.argv[1] == '--web':
        from app import app
        app.run(debug=True)
    else:
        main(sys.argv[1], sys.argv[2])
