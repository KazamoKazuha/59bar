
import requests
import time
import math
import json
import yaml

_REFRESH_TOKEN = "DyHteIcdx4BWw4szpfgbO5JEZd5c6fHJIrMliGn1_5s"


class setu_manager:
    timestamp = 0

    def __init__(self):
        while True:
            if time.time() > self.timestamp+600:
                self.get()

    def get(self):
        self.timestamp = math.floor(time.time()/600)*600+300
        headers = {'num': 10, 'apikey': '694488666047165767e5b5'}
        json_result = requests.get(
            'https://api.lolicon.app/setu/', params=headers)
        # json_result = json.loads(json_result)
        rtn=json_result.json()
        self.lst=[]
        # print("Printing image titles and tags with English tag translations present when available")
        if rtn['code']==0:
            for illust in rtn['data']:
                self.lst.append(
                    {'pic': illust['url'], 'id': illust['pid']})
            self.save()

    def save(self):
        yaml_setuList = yaml.dump(self.lst, allow_unicode=True)
        with open('resource/setu.yaml', 'w', encoding='utf-8') as f:
            f.write(yaml_setuList)
        print('Saved!')


if __name__ == '__main__':
    new = setu_manager()
