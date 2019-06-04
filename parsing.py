from asyncio import Semaphore
import asyncio
import json
import os

from aiohttp import ClientSession, ClientConnectionError

from logger_creater import get_logger

JSON_PATH = 'results/rooms.json'
main_log = get_logger('request')


async def fetch(url: str, params: dict,  session: ClientSession) -> dict:

        try:
            async with session.get(url, params=params, timeout=10) as response:
                resp_json = await response.json()
        except ClientConnectionError as err:
            main_log.error('Connection error: {}'.format(err))
            return dict()
        try:
            checkout = resp_json['hotelSearchCriteria']['checkOutDate']
            hotel_name = resp_json['aboutHotel']['hotelName']
            currency = resp_json['currencyInfo']['code']
            hotel_url = resp_json['searchbox']['config']['defaultSearchURL']

            room_grid_data = resp_json['roomGridData']['masterRooms'][0]
            room_name = room_grid_data['name']
            room_data = room_grid_data['rooms'][0]
        except KeyError as err:
            main_log.info('Required information not found: {}'.format(err))
            return dict()

        cheapest_room = {
            'name': room_name,
            'occupancy': room_data['occupancy'],
            'price': room_data['price'],
            'currency': currency
        }

        data = {
            'hotel_name': hotel_name,
            'hotel_id': params['hotel_id'],
            'checkin': params['checkin'],
            'checkout': checkout,
            'los': params['los'],
            'cheapest_room': cheapest_room,
            'hotel_url': hotel_url
        }
        return data


async def bound_fetch(sem: Semaphore, url: str, params: dict, session: ClientSession):
    async with sem:
        data = await fetch(url, params, session)
        if data:
            save_data(data)
            main_log.info('Room found')
        else:
            main_log.info('Room not found')


async def create_tasks(input_data: list):
    url = 'https://www.agoda.com/api/en-us/pageparams/property'
    tasks = []
    sem = Semaphore(1000)

    async with ClientSession() as session:
        for item in input_data:
            params = {
                'hotel_id': item[0],
                'checkin': item[1],
                'los': item[2],
                'adults': item[3]
            }

            task = asyncio.ensure_future(bound_fetch(sem, url, params, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses


def save_data(room: dict):
    if not os.path.isfile(JSON_PATH):
        with open(JSON_PATH, 'w') as json_file:
            json.dump([room], json_file, indent=4)
    else:
        with open(JSON_PATH) as feeds_json:
            feeds = json.load(feeds_json)
            feeds.append(room)

            with open(JSON_PATH, 'w') as json_file:
                json.dump(feeds, json_file, indent=4)
