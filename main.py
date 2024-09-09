import sys


def download(json_filename: str):
    import urllib.request

    API_URL = 'https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records?limit=100'

    request = urllib.request.urlopen(API_URL)
    json_text = request.read().decode(request.headers.get_content_charset())

    with open(json_filename, 'w') as fs:
        fs.write(json_text)


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'web':
        from app import app
        app.run(debug=True)
    elif action == 'download':
        download(sys.argv[2])
    else:
        print('unknown command', action)
        exit(1)
