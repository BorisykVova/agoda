from datetime import datetime
import argparse
import json
import time
import csv
import os

from parsing import get_rooms, main_log

start_time = time.time()
JSON_PATH = 'results/rooms.json'

now = datetime.now()
date_now = datetime.strftime(datetime.now(), "%Y-%m-%d")


parser = argparse.ArgumentParser(description='Help')
parser.add_argument('--check_in',  type=str, default=date_now)
parser.add_argument('--los',  type=int, default=1)
parser.add_argument('--id',  type=int)
parser.add_argument('--adults',  type=int, default=2)
parser.add_argument('-csv',  action='store_true')
parser.add_argument('--path', type=str, default='input/input.csv')
args = parser.parse_args()

rooms = []

if args.csv:
    with open(args.path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            rooms.append(get_rooms(*line))
else:
    rooms.append(get_rooms(args.id, args.check_in, args.los,  args.adults))


if rooms:
    main_log.info('Rooms found({})'.format(time.time() - start_time))
    if not os.path.isfile(JSON_PATH):
        with open(JSON_PATH, 'w') as json_file:
            json.dump(rooms, json_file, indent=4)
    else:
        with open(JSON_PATH) as feeds_json:
            feeds = json.load(feeds_json)
            feeds.append(rooms)

            with open(JSON_PATH, 'w') as json_file:
                json.dump([*feeds, *rooms], json_file, indent=4)

else:
    main_log.info('Rooms not found')
