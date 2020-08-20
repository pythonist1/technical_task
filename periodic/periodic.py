import aiohttp
import datetime, asyncio, time


async def run_periodically():
        now = datetime.datetime.now()
        run_time = datetime.datetime(now.year,now.month,now.day,0,0) + datetime.timedelta(days=1)
        session = aiohttp.ClientSession()
        time.sleep(3)
        async with session.get('http://localhost:8000/collector_run'):
            await session.close()
        while True:
            now = datetime.datetime.now()
            if datetime.datetime(now.year,now.month,now.day,now.hour,now.minute) == run_time:
                print(now)
                run_time += datetime.timedelta(days=1)
                session = aiohttp.ClientSession()
                async with session.get('http://localhost:8000/collector_run'):
                    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run_periodically())
