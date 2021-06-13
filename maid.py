import yaml
import os
import random
import nga_text
from cloth import cloth
from menu import menu
from user import user_manager


class maid:
    koujou = {}
    rate_drunk = [0.9, 0.8, 0.7, 0.6, 0.5, 0.5]
    rate_cleaner = [0.05, 0.15, 0.3, 0.6, 0.7, 0.8, 0.8]

    def load(self):
        if os.path.exists('koujou/maid.yaml'):
            with open('koujou/maid.yaml', 'r', encoding='gbk') as f:
                self.koujou = yaml.load(f.read(), Loader=yaml.FullLoader)

    def save(self):
        yaml_koujou = yaml.dump(self.koujou, allow_unicode=True)
        with open('koujou/maid.yaml', 'w', encoding='gbk') as f:
            f.write(yaml_koujou)

    def input(self,name):
        self.koujou[name] = {'part1': [], 'part2': [], 'part_drunk': []}
        while True:
            s = input('type in part1')
            if s == 'end':
                break
            self.koujou[name]['part1'].append(s)
        while True:
            s = input('type in part2')
            if s == 'end':
                break
            self.koujou[name]['part2'].append(s)
        while True:
            s = input('type in part_drunk')
            if s == 'end':
                break
            self.koujou[name]['part_drunk'].append(s)
        print(self.koujou)
        self.save()

    def action(self, drink, user, maid='maid'):
        user = str(user)
        sm = 0
        real_level = self.user.userList[user]['level']
        level = min(real_level, 5)
        rate_drunk = random.random()
        rate_drink = random.random()
        rate_cleaner = random.random()
        ifDrunk = False
        ifCleaner = False
        sm += self.user.addDrink(user, drink)
        self.menu.setTimestamp(drink)
        if(rate_drunk < self.rate_drunk[level]):
            ifDrunk = True
            self.user.userList[user]['level'] = real_level + 1
            sm += self.user.addDrunk(user, real_level + 1)
        if((ifDrunk and rate_cleaner < self.rate_cleaner[level]) or (level > 4 and rate_drink > 0.1)):
            ifCleaner = True
        clothList = []
        for i in range(real_level):
            if(ifDrunk or random.random() > 0.5):
                cloth = self.cloth.get()
                sm += self.user.addCloth(user, cloth)
                clothList.append(cloth)
        rtn = self.actionText(drink, user, ifDrunk, ifCleaner, clothList, sm, maid)
        if(ifCleaner):
            self.user.banUser(user)
        self.user.userList[user]['banreply'] = False  # 重置ban回复
        return rtn

    def actionText(self, drink, user, ifDrunk, ifCleaner, clothList, sm, maid):
        real_level = self.user.userList[user]['level']
        level = min(real_level, 5)
        s = '你的酒似乎好了……你握紧了手里的龙门币……\n'
        s += self.koujou[maid]['part1'][random.randint(0,
                                                       len(self.koujou[maid]['part1'])-1)] + '\n'
        s += self.koujou[maid]['part2'][random.randint(0,
                                                       len(self.koujou[maid]['part2'])-1)] + '\n\n'
        s += nga_text.b('你喝下一杯')
        s += self.menu.showDrink(drink)
        s += nga_text.i('苦酒入喉……') + '\n'
        for i in range(real_level):
            for j in range(random.randint(1, pow(2, real_level))):
                s += nga_text.i('吨')
            s += '\n'
        # if(rate)
        s += '\n'
        if(ifDrunk):
            s += nga_text.b('你喝醉了！') + '\n'
        s += '当前醉酒等级为：' + str(real_level) + '级\n\n'
        if(len(clothList) != 0):
            s += nga_text.b('你脱掉了身上的衣服！！') + '\n'+'你脱掉了：'
            for i in clothList:
                s += i + ','
            s += '\n'
        if(ifCleaner or random.random() > 0.75):
            s += '\n' + nga_text.b('大事不好！！！')
            ts = ''
            for i in range(10):
                ts += '……' * random.randint(1, 5) + '\n\n'
            if(ifCleaner):
                ts += nga_text.b(self.koujou[maid]['part_drunk'][random.randint(0,
                                                                                len(self.koujou[maid]['part_drunk'])-1)]) + '\n\n'
                ts += '[size=120%][color=red][u][i][b]你被吸尘器了！！！[/b][/i][/u][/color][/size]'
            else:
                ts += nga_text.b('虚惊一场！看来恋恋暂时没有把你吸尘器掉的打算……')
            s += nga_text.collapse(ts, '你听见吸尘器的嗡嗡声………………')
        s += nga_text.b('当前分数为：') + '(+' + str(sm) + ')' + \
            str(self.user.userList[user]['score'])
        return s

    def __init__(self):
        self.load()
        self.save()
        self.menu = menu()
        self.user = user_manager()
        self.cloth = cloth()


if __name__ == '__main__':
    new = maid()
    new.input('ceobe')
    new.save()
