import json
import sys
import datetime


def main(json_filename: str):
    with open(json_filename, 'r') as fs:
        json_data = json.load(fs)

    for json_item in json_data['results']:
        date = datetime.datetime.fromisoformat(json_item['date_passage'])
        time = datetime.time.fromisoformat(json_item['fermeture_a_la_circulation'])
        t2 = datetime.datetime.combine(date, time)
        print(date, time, t2)


if __name__ == '__main__':
    main(sys.argv[1])
