import random
import requests
import threading
from time import time, sleep


REQUEST_URL = 'https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/?ac=WIFI&op_region=SE&app_skin=white&'


def get_video_id(video_url):
    response = requests.get(video_url)
    correct_url = str(response.url)

    if 'com/v/' in correct_url:
        video_id = correct_url.split('v/')[1].split('.')[0]
    else:
        video_id = correct_url.split('video/')[1].split('?')[0]

    return video_id


class TikTOkViews:
    def __init__(self):
        self.start_time = time()
        self.added = 0
        self.lock = threading.Lock()
        self.amount = int(input('How many shares do you want? '))
        self.video_id = get_video_id(input('Paste tiktok video url: '))

    def update_title(self):
        while self.added == 0:
            sleep(0.2)

        while self.added < self.amount:
            print('Added: {0}/{1}'.format(self.added, self.amount))
            sleep(0.2)

        print('Added: {0}/{1}'.format(self.added, self.amount))

    def main(self):
        action_time = round(time())
        device_id = str(random.randint(1000000000000000000, 9999999999999999999))

        data = {
            'action_time': action_time,
            'item_id': self.video_id,
            'item_type': 1,
            'share_delta': 1,
            'stats_channel': 'copy'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'TikTok 16.6.5 rv:166515 (iPhone; iOS 13.6; en_US) Cronet',
            'x-common-params-v2': f'version_code=16.6.5&app_name=musical_ly&channel=App%20Store&'
                                  f'device_id={device_id}&aid=1233&os_version=13.5.1&'
                                  f'device_platform=iphone&device_type=iPhone10,5',
        }

        try:
            response = requests.post(REQUEST_URL, params=data, headers=headers)

        except:
            self.main()

        else:
            if all(i not in response.text for i in ['Service Unavailable', 'Gateway Timeout']):
                if response.status_code == 200:
                    self.added += 1
                else:
                    self.lock.acquire()
                    print(f'Error: {response.text} | Status Code: {response.status_code}')
                    self.lock.release()
                    self.main()
            else:
                self.main()

    def start(self):
        threading.Thread(target=self.update_title).start()

        for _ in range(self.amount):
            while True:
                if threading.active_count() <= 300:
                    threading.Thread(target=self.main).start()
                    break

        sleep(3)


if __name__ == '__main__':
    tiktok_views = TikTOkViews()
    tiktok_views.start()
