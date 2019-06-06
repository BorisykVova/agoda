import trafaret as t

from agoda_time import get_date, valid_date


def check_valid(data: list) -> dict:

    # params = {
    #     'hotel_id': data[0],
    #     'checkin': data[1],
    #     'los': data[2],
    #     'adults': data[3]
    # }

    params = {}

    try:
        params['hotel_id'] = data[0]
    except IndexError as err:
        raise IndexError('In input miss hotel_id: {}'.format(err))

    try:
        params['checkin'] = data[1]
    except IndexError:
        params['checkin'] = get_date(day_range=60)

    try:
        params['los'] = data[2]
    except IndexError:
        params['los'] = 1

    try:
        params['adults'] = data[3]
    except IndexError:
        params['adults'] = 1

    convert = t.Dict({
         'hotel_id': t.Int,
         'checkin': valid_date,
         'los': t.Int,
         'adults': t.Int,
    })

    correct_data = convert.check(params)
    return correct_data
