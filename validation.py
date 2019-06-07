import trafaret as t

from agoda_date import get_date, valid_date


def check_valid(data: dict, rand_days:int) -> dict:
    convert = t.Dict({
         t.Key('hotel_id') >> 'hotel_id': t.Int,
         t.Key('checkin', default=get_date(day_range=rand_days)) >> 'checkin': valid_date,
         t.Key('los', default=1) >> 'los': t.Int,
         t.Key('adults', default=2) >> 'adults': t.Int,
    })
    correct_data = convert.check(data)
    return correct_data
