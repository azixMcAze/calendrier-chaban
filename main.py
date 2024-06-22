import sys

def convert(json_filename: str, ical_filename: str):
    import chaban_calendar

    with open(json_filename, 'r') as fs:
        json_text = fs.read()

    cal_text = chaban_calendar.convert_json_to_cal(json_text)

    with open(ical_filename, 'wb') as fs:
        fs.write(cal_text)


def download(json_filename: str):
    import bridge_json_utils
    import urllib.request

    request = urllib.request.urlopen(bridge_json_utils.API_URL)
    json_text = request.read().decode(request.headers.get_content_charset())

    with open(json_filename, 'w') as fs:
        fs.write(json_text)


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'web':
        from app import app
        app.run(debug=True)
    elif action == 'convert':
        convert(sys.argv[2], sys.argv[3])
    elif action == 'download':
        download(sys.argv[2])
    else:
        print('unknown command', action)
        exit(1)
