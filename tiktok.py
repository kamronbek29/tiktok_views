import asyncio

import aiohttp
import time

REQUEST_URL = 'https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/'


async def get_video_id(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link, allow_redirects=True) as response:
            correct_url = str(response.url)

            if 'com/v/' in correct_url:
                video_id = correct_url.split('v/')[1].split('.')[0]
            else:
                video_id = correct_url.split('video/')[1].split('?')[0]

            return video_id


async def get_video_params(video_id):
    action_time = str(time.time())

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'TikTok 12.5.8 nv:198454 (Android; SDS 32.3; en_EN) Musical',
    }

    data = {
        'action_time': action_time,
        'item_id': video_id,
        'item_type': '1',
        'share_delta': '1',
        'stats_channel': 'copy',
        'version_code': '3.3.4',
        'app_name': 'musical_ly',
        'channel': 'App Store',
        'device_id': '7874600876274394189',
        'iid': '1232256540021056640',
        'aid': '1233',
        'os_version': '12.5.8',
        'device_platform': 'Android',
        'device_type': 'iPhone10,5'
    }

    return headers, data


async def get_video_url(link):
    video_id = await get_video_id(link)
    headers, data = await get_video_params(video_id)

    for i in range(1000):
        async with aiohttp.ClientSession() as session:
            async with session.post(REQUEST_URL, params=data, headers=headers) as response:
                response_json = await response.json()
                if response_json['status_code'] == 0:
                    if i % 10 == 0 and i != 0:
                        print(f'Made {i} successful shares')


if __name__ == '__main__':
    video_url = input('Paste video url here: ')
    asyncio.run(get_video_url(video_url))

