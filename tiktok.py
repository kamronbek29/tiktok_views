
import asyncio
import random

import aiohttp
import time

REQUEST_URL = 'https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/'


async def get_video_id(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link, allow_redirects=True) as response:
            correct_url = response.url
            video_id = str(correct_url).split('com/v/')[1].split('.html?')[0]

            return video_id


# Get random ids for device id and iid
async def random_with_n_digits():
    range_start = 10 ** 18
    range_end = (10 ** 19) - 1

    first_id = str(random.randint(range_start, range_end))
    second_id = str(random.randint(range_start, range_end))

    return first_id, second_id


async def get_video_params(video_id):
    first_id, second_id = await random_with_n_digits()
    action_time = str(time.time())

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'TikTok 16.3.5 rv:198454 (iPhone; iOS 13.1; sv_SE) Cronet',
    }

    data = {
        'action_time': action_time,
        'item_id': video_id,
        'item_type': '1',
        'share_delta': '1',
        'stats_channel': 'copy',
        'version_code': '16.6.5',
        'app_name': 'musical_ly',
        'channel': 'App Store',
        'device_id': first_id,
        'iid': second_id,
        'aid': '1233',
        'os_version': '13.1.1',
        'device_platform': 'iphone',
        'device_type': 'iPhone10,5'
    }

    return headers, data


async def get_video_url(link):
    video_id = await get_video_id(link)
    headers, data = await get_video_params(video_id)

    for i in range(1000):
        async with aiohttp.ClientSession() as session:
            async with session.post(REQUEST_URL, data=data, headers=headers) as response:
                response_json = await response.json()
                if response_json['status_code'] == 0:
                    if i % 10 == 0 and i != 0:
                        print(f'Made {i} successful shares')


if __name__ == '__main__':
    video_url = input('Paste video url here: ')
    asyncio.run(get_video_url(video_url))

