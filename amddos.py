import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx
import asyncio
import aiohttp

# تعداد درخواست‌ها و آدرس وب‌سایت را مشخص کنید
num_requests = 1000000
url = 'https://iranwire.com/'

# تابع برای ارسال درخواست با استفاده از requests
def send_request_requests(url):
    try:
        response = requests.get(url)
        return response.status_code
    except Exception as e:
        return str(e)

# تابع برای ارسال درخواست با استفاده از httpx
def send_request_httpx(client, url):
    try:
        response = client.get(url)
        return response.status_code
    except Exception as e:
        return str(e)

# تابع برای ارسال درخواست با استفاده از aiohttp
async def send_request_aiohttp(session, url):
    try:
        async with session.get(url) as response:
            return response.status
    except Exception as e:
        return str(e)

# تابع اصلی برای مدیریت درخواست‌ها
def main():
    # ارسال درخواست‌ها با استفاده از requests
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(send_request_requests, url) for _ in range(num_requests // 3)]
        for future in as_completed(futures):
            print(f'Requests: {future.result()}')

    # ارسال درخواست‌ها با استفاده از httpx
    with httpx.Client() as client:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(send_request_httpx, client, url) for _ in range(num_requests // 3)]
            for future in as_completed(futures):
                print(f'httpx: {future.result()}')

    # ارسال درخواست‌ها با استفاده از aiohttp
    asyncio.run(send_requests_aiohttp(url, num_requests // 3))

async def send_requests_aiohttp(url, num_requests):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request_aiohttp(session, url) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        for result in results:
            print(f'aiohttp: {result}')

if __name__ == '__main__':
    main()
