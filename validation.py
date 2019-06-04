import datetime

import trafaret as t


def valid_date(date: str) -> str:
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def check_valid(data: list) -> dict:

    params = {
        'hotel_id': data[0],
        'checkin': data[1],
        'los': data[2],
        'adults': data[3]
    }

    convert = t.Dict({
         'hotel_id': t.Int,
         'checkin': valid_date,
         'los': t.Int,
         'adults': t.Int,
    })

    correct_data = convert.check(params)
    return correct_data
