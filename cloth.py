import yaml
import os
import random


def clothInput():
    ans = {'first': [], 'second': []}
    while True:
        s = input('type in first')
        if s == 'end':
            break
        ans['first'].append(s)
    while True:
        s = input('type in second')
        if s == 'end':
            break
        ans['second'].append(s)
    print(ans)
    yaml_cloth = yaml.dump(ans, allow_unicode=True)
    with open('resource/cloth.yaml', 'w') as f:
        f.write(yaml_cloth)


def outputTest():
    if os.path.exists('resource/cloth.yaml'):
        with open('resource/cloth.yaml', 'r') as f:
            ans = yaml.load(f.read(), Loader=yaml.FullLoader)
            print(ans)
            n = len(ans['first'])
            m = len(ans['second'])
            for i in range(20):
                a = ans['first'][random.randint(0, n-1)]
                b = ans['second'][random.randint(0, m-1)]
                print(b+a)


class cloth:
    clo = {}

    def __init__(self):
        if os.path.exists('resource/cloth.yaml'):
            with open('resource/cloth.yaml', 'r', encoding='gbk') as f:
                self.clo = yaml.load(f.read(), Loader=yaml.FullLoader)

    def get(self):
        n = len(self.clo['first'])
        m = len(self.clo['second'])
        a = self.clo['first'][random.randint(0, n-1)]
        b = self.clo['second'][random.randint(0, m-1)]
        # print(b+a)
        return b+a


if __name__ == '__main__':
    outputTest()
