import argparse
import json
import os
from parsing import get_rooms, main_log
from datetime import datetime

JSON_PATH = 'results/rooms.json'


now = datetime.now()
date_now = datetime.strftime(datetime.now(), "%Y-%m-%d")


parser = argparse.ArgumentParser(description='Help')
parser.add_argument('--check_in',  type=str, default=date_now)
parser.add_argument('--los',  type=int, default=1)
parser.add_argument('--id',  type=int)
parser.add_argument('--adults',  type=int, default=2)
args = parser.parse_args()

HOTEL_ID = args.id
CHECK_IN = args.check_in
LOS = args.los
ADULTS = args.adults

room = get_rooms(CHECK_IN, LOS, HOTEL_ID, ADULTS)

if room:
    main_log.info('Room found')

    data = {
        'hotel_id': HOTEL_ID,
        'check_in': CHECK_IN,
        'los': LOS,
        'cheapest_room': room,
    }

    if not os.path.isfile(JSON_PATH):
        with open(JSON_PATH, 'w') as json_file:
            json.dump([data], json_file, indent=4)
    else:
        with open(JSON_PATH) as feeds_json:
            feeds = json.load(feeds_json)
            feeds.append(data)

            with open(JSON_PATH, 'w') as json_file:
                json.dump(feeds, json_file, indent=4)

else:
    main_log.info('Room not found', )
