import requests
import typing
from logger_creater import get_logger


main_log = get_logger('request')


def get_rooms(check_in: str, los: str, hotel_id: str, adults: str) -> typing.Dict:

    try:
        resp = requests.get('https://www.agoda.com/api/en-us/pageparams/property',
                            params={
                                'checkin': check_in,
                                'los': los,
                                'hotel_id': hotel_id,
                                'adults': adults
                            }, timeout=10)
    except (requests.ConnectionError, requests.RequestException) as err:
            main_log.error("Got Request Exception: %s", err)
            return dict()

    if resp.status_code in [400, 404]:
        main_log.error('Hotel(hotel_id=%s) not found: %s', hotel_id, resp)
        return dict()

    try:
        room_grid_data = resp.json()['roomGridData']['masterRooms'][0]
        room_name = room_grid_data['name']
        room_data = room_grid_data['rooms'][0]
    except KeyError as err:
        main_log.error('No room information(hotel_id=%s, date=%s, los: %s : %s', hotel_id, check_in, los, err)
        return dict()

    cheapest_room = {
        'name': room_name,
        'occupancy': room_data['occupancy'],
        'price': room_data['price']
    }

    return cheapest_room
