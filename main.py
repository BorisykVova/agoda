import argparse
import asyncio
import csv
import time

from agoda_date import get_date
from parsing import create_tasks
from information_processing import load_data


parser = argparse.ArgumentParser(description='Help')
parser.add_argument('--checkin',  type=str, default=get_date())
parser.add_argument('--los',  type=int, default=1)
parser.add_argument('--id',  type=int)
parser.add_argument('--adults',  type=int, default=2)
parser.add_argument('-csv',  action='store_true')
parser.add_argument('--path', type=str, default='input/input.csv')
parser.add_argument('--sem', type=int, default=100)
parser.add_argument('--day_range', type=int, default=0)
args = parser.parse_args()


if args.csv:
    data = load_data(args.path)
else:
    data = [{'hotel_id': args.id,
             'checkin': args.checkin,
             'los': args.los,
             'adults': args.adults
             }]

start_time = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(create_tasks(data, args.sem, args.day_range))
loop.run_until_complete(future)
print(time.time() - start_time)
