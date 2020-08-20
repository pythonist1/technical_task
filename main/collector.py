import aiohttp
import json, asyncio, datetime
from pprint import pprint

routes = [
    ('ALA','TSE'),
    ('TSE','ALA'),
    ('ALA','MOW'),
    ('MOW','ALA'),
    ('ALA','CIT'),
    ('CIT','ALA'),
    ('TSE','MOW'),
    ('MOW','TSE'),
    ('TSE','LED'),
    ('LED','TSE'),
]

async def collect():
    print(1)
    headers = {'content-type': 'application/json'}
    for route in routes:
        month_ahead_flights = []
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        for i in range(31):
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get('https://api.skypicker.com/flights' +
                                        f'?flyFrom={route[0]}&to={route[1]}' +
                                        f'&dateFrom={str(date.day)+"/"+str(date.month)+"/"+str(date.year)}' +
                                        f'&dateTo={str(date.day)+"/"+str(date.month)+"/"+str(date.year)}' +
                                        '&partner=picky&v=3') as resp:
                    jsonform = json.loads(await resp.text())
            try:
                min_price = min(list(zip([flight for flight in jsonform['data']],
                                        [price['price'] for price in jsonform['data']])), 
                                        key=lambda x: x[1])[0]
                pprint(min_price)
                month_ahead_flights.append({'date':date.isoformat(),
                                            'variant':min_price})
            except (ValueError, KeyError):
                continue
            date += datetime.timedelta(days=1)
        yield {'route':route[0]+'-'+route[1],'dates':month_ahead_flights}