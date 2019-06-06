import argparse
import asyncio
import csv
import time

from parsing import create_tasks
from agoda_time import get_date


parser = argparse.ArgumentParser(description='Help')
parser.add_argument('--checkin',  type=str, default=get_date())
parser.add_argument('--los',  type=int, default=1)
parser.add_argument('--id',  type=int)
parser.add_argument('--adults',  type=int, default=2)
parser.add_argument('-csv',  action='store_true')
parser.add_argument('--path', type=str, default='input/input.csv')
args = parser.parse_args()


if args.csv:
    with open(args.path, 'r') as csv_file:
        data = list(csv.reader(csv_file))
else:
    data = [[args.id, args.checkin, args.los, args.adults]]

start_time = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(create_tasks(data))
loop.run_until_complete(future)
print(time.time() - start_time)
