import sys
import chaban_calendar

def main(json_filename: str, ical_filename: str):
    with open(json_filename, 'r') as fs:
        json_text = fs.read()

    cal_text = chaban_calendar.convert_json_to_cal(json_text)

    with open(ical_filename, 'wb') as fs:
        fs.write(cal_text)


if __name__ == '__main__':
    if sys.argv[1] == '--web':
        from app import app
        app.run(debug=True)
    else:
        main(sys.argv[1], sys.argv[2])
