import argparse
from pprint import pformat, pprint
from parsing import get_rooms, main_log
from datetime import datetime

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
    with open('rooms', 'a') as file:
        file.write(pformat(data))
else:
    main_log.info('Room not found')
