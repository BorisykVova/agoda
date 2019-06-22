from concurrent.futures._base import TimeoutError
from asyncio import Semaphore
import asyncio
import typing as typ

from aiohttp import ClientSession, ClientConnectionError, ServerTimeoutError, ContentTypeError
from trafaret import DataError

from logger_creater import get_logger
from validation import check_valid
from information_processing import save_data

main_log = get_logger('request')


async def fetch(url: str, params: dict,  session: ClientSession) -> dict:

        try:
            async with session.get(url, params=params, timeout=10) as response:
                resp_json = await response.json()
        except ClientConnectionError as err:
            main_log.error(f'Connection error: {err}')
            return dict()
        except ServerTimeoutError as err:
            main_log.error(f'Server timeout error: {err}')
            return dict()
        except TimeoutError as err:
            main_log.error(f'Concurrent timeout error: {err}')
            return dict()
        except ContentTypeError as err:
            main_log.error(f'Response content type error : {err}')

        try:
            checkout = resp_json['hotelSearchCriteria']['checkOutDate']
            hotel_name = resp_json['aboutHotel']['hotelName']
            currency = resp_json['currencyInfo']['code']
            hotel_url = resp_json['searchbox']['config']['defaultSearchURL']
            room_grid_data = resp_json['roomGridData']['masterRooms'][0]
            room_name = room_grid_data['name']
            room_data = room_grid_data['rooms'][0]
            room_images = room_grid_data['images']
        except (KeyError, IndexError) as err:
            main_log.info(f'Required information not found: {err}')
            return dict()

        cheapest_room = {
            'name': room_name,
            'occupancy': room_data['occupancy'],
            'price': room_data['price'],
            'currency': currency,
            'images': room_images
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


async def bound_fetch(semaphore: Semaphore, url: str, params: dict, session: ClientSession) -> None:
    async with semaphore:
        data = await fetch(url, params, session)
        if data:
            save_data(data)
            main_log.info('Room found')
        else:
            main_log.info('Room not found')


async def create_tasks(input_data: typ.List[dict], semaphore_count: int, day_range: int) -> None:
    url = 'https://www.agoda.com/api/en-us/pageparams/property'
    tasks = []
    semaphore = Semaphore(semaphore_count)
    async with ClientSession() as session:
        for item in input_data:
            try:
                params = check_valid(item, day_range)
            except (ValueError, IndexError, DataError) as err:
                main_log.info(f'Invalid data: {err}')
                continue
            task = asyncio.ensure_future(bound_fetch(semaphore, url, params, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses
