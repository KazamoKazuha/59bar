import yaml
import os
import time
import math
from cloth import cloth
import nga_text


class user_manager:
    userList = {}

    def load(self):
        if os.path.exists('resource/user.yaml'):
            with open('resource/user.yaml', 'r', encoding='utf-8') as f:
                data = yaml.load(f.read(), Loader=yaml.FullLoader)
                self.userList=data['user']
                # self.userList = yaml.load(f.read(), Loader=yaml.FullLoader)

    def save(self):
        data={}
        data['user']=self.userList
        yaml_userList = yaml.dump(data, allow_unicode=True)
        with open('resource/user.yaml', 'w', encoding='utf-8') as f:
            f.write(yaml_userList)

    def __init__(self):
        self.load()

    def userInit(self, id, name):
        id = str(id)
        if id in self.userList:
            print('当前用户已存在', id)
            return
        user_item = {'id': id, 'name': name, 'score': 0, 'group': 1, 'ban': 0, 'bantimes': 0, 'banreply': False,
                     'level': 0, 'history': {'cloth_sum': 0,'cloth': [], 'drink': {}, 'drunk': {}}}
        self.userList[id] = user_item
        self.save()
    
    def id2name(self,id):
        return self.userList[str(id)]['name']

    def banUser(self, id):
        id = str(id)
        crt = int(time.time())
        self.userList[id]['bantimes'] = self.userList[id]['bantimes'] + 1
        print('Crt:' + time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.gmtime(crt)))
        self.userList[id]['ban'] = int((math.ceil(crt/600)) * 600)
        self.userList[id]['level'] = 0
        print('Ban ' + id + ' until:' +
              time.strftime('%Y-%m-%d %H:%M:%S',
                            time.gmtime(self.userList[id]['ban'])))
        self.save()

    def addCloth(self, id, cloth):
        id = str(id)
        # self.userList[id]['history']['cloth'].append(cloth)
        if 'cloth_sum' not in self.userList[id]['history']:
            self.userList[id]['history']['cloth_sum']=0
        self.userList[id]['history']['cloth_sum']+=1
        # print(self.userList[id])
        self.save()
        return 0

    def addDrink(self, id, drink):
        id = str(id)
        times = 0
        if drink in self.userList[id]['history']['drink']:
            times = self.userList[id]['history']['drink'][drink]
        times += 1
        self.userList[id]['history']['drink'][drink] = times
        self.userList[id]['score'] = self.userList[id]['score'] + \
            self.userList[id]['level']
        self.save()
        return self.userList[id]['level']

    def addDrunk(self, id, drunk):
        id = str(id)
        drunk = str(drunk)
        times = 0
        if drunk in self.userList[id]['history']['drunk']:
            times = self.userList[id]['history']['drunk'][drunk]
        times += 1
        self.userList[id]['history']['drunk'][drunk] = times
        self.userList[id]['score'] = self.userList[id]['score'] + \
            pow(10, int(drunk))
        self.save()
        return pow(10, int(drunk))

    def showUser(self, id, showType=0):
        id = str(id)
        # [collapse=aaaa]bbbbb[/collapse]
        item = self.userList[id]
        s = '尊敬的 ' + nga_text.b(item['name']) + ' 博士：\n\n'
        s += nga_text.b('您的分数为：') + str(item['score']) + '\n'
        s += nga_text.b('您被吸尘器了：') + str(item['bantimes']) + '次\n\n'
        s += nga_text.b('您脱掉了：') + str(item['history']['cloth_sum']) + '件\n'
        for i in item['history']['cloth']:
            s += nga_text.i(i + '，')
        s += '\n'
        if showType > 0:
            s += nga_text.b('您喝掉了：') + '\n'
            for i, j in item['history']['drink'].items():
                s += nga_text.i(i) + '：' + str(j) + '次\n'
        s += nga_text.b('您喝醉了：') + '\n'
        for i, j in item['history']['drunk'].items():
            s += nga_text.i('等级' + i) + '：' + str(j) + '次\n'
        return nga_text.collapse(s, item['name'])

    def showList(self):
        score = 0
        name = []
        s = ''
        cnt=0
        show_list = sorted(self.userList.items(),
                           key=lambda x: x[1]['score'], reverse=True)
        for i, item in show_list:
            cnt+=1
            if(cnt>20):
                break
            if(item['score'] > score):
                score = item['score']
                name = []
            if(item['score'] == score):
                name.append(item['name'])
            if(item['score'] != 0):
                s += self.showUser(i)
        fs = '[b][size=150%]酒鬼名单[/size][/b]\n\n[b]当前最高分：[/b]' + \
            str(score)+'\n\n[b]当前最佳酒鬼：[/b]\n'
        for i in name:
            fs += i + '\n'
        return fs + '\n' + s + '只显示分数最高的20位博士'

    def tmpCommand(self):
        for i,j in self.userList.items():
            self.userList[i]['history']['cloth_sum'] = len(
                self.userList[i]['history']['cloth'])
            self.userList[i]['history']['cloth']=[]
        self.save()



if __name__ == '__main__':
    new = user_manager()
    print(len(new.userList))
    #lst = new.userList['62783284']['history']['drink']
    #sum=0
    #for i,j in lst.items():
    #    sum+=j
    #print(sum)
    # new.tmpCommand()
    # print(new.showUser('20703054'))
    # new.userInit(60178730, '105gun')
    # new.addDrink(60178730, '水')
    # new.addDrunk(60178730, 1)
    # new.banUser(60178730)
    # print(new.showUser(60178730))
