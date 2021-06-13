from better_module import crawler
import time
import yaml
import os
import math
import random
from maid import maid
import nga_text


def getTime():
    return time.strftime('%Y-%m-%d %H:%M:%S',
                         time.gmtime(int(time.time())))


class client:
    lastTimestamp = 0
    log = {'lastFloor': 0, 'lastEdit': 0, 'theme': 25744165, 'log': []}

    def load(self):
        if os.path.exists('log.yaml'):
            with open('log.yaml', 'r', encoding='gb18030') as f:
                self.log = yaml.load(f.read(), Loader=yaml.FullLoader)

    def save(self):
        yaml_log = yaml.dump(self.log, allow_unicode=True)
        with open('log.yaml', 'w', encoding='gb18030') as f:
            f.write(yaml_log)

    def exe(self, command):
        # mode: edit, reply, replyFloor
        if(command['mode'] == 'edit'):
            return self.crawler.editFloor(
                self.log['theme'], command['floor'], command['content'])
        if(command['mode'] == 'reply'):
            return self.crawler.reply(
                self.log['theme'], command['content'])
        if(command['mode'] == 'replyFloor'):
            return self.crawler.replyFloor(
                self.log['theme'], command['floor'], command['content'])

    def insertCommand(self, content, floor=0, mode='reply'):
        # mode: edit, reply, replyFloor
        command = {'mode': mode,
                   'floor': floor, 'content': content}
        self.log['log'].append(command)

    def check(self, info):
        # 选择角色
        char_list = ['maid', 'surtr', 'ptilopsis', 'ceobe']
        crt_maid = char_list[random.randint(0, len(char_list)-1)]
        # 初始化新玩家
        if(str(info['id']) not in self.maid.user.userList):
            self.maid.user.userInit(info['id'], info['name'])
        content = info['content'].split()
        for i in range(8):
            content.append('占位')
        if('女仆！' not in content and '女仆!' not in content):
            return
        # 处理
        if(self.maid.user.userList[str(info['id'])]['ban'] > time.time()):
            # print('当前用户处于封禁状态，', info['name'], '楼层为', info['floor'])
            tmp=''
            if('查看' in content):  # and str(info['id']) == '60178730'):
                tmp = '\n\n' + self.maid.user.showUser(str(info['id']), 1)
            if(self.maid.user.userList[str(info['id'])]['banreply'] == False):
                self.insertCommand(nga_text.b('你还在吸尘器里，不能召唤女仆!')+tmp,
                                   info['floor'], 'replyFloor')
                # self.maid.user.userList[str(info['id'])]['banreply'] = True
            return
        answer = ''
        # 一楼只执行一条指令
        if('点单' in content):
            target = content[content.index('点单')+1]
            target = self.maid.menu.checkName(target)
            if(target != '错误发生' or crt_maid == 'ptilopsis'):
                answer += self.maid.action(target, info['id'], maid=crt_maid)
                # self.insertCommand(self.maid.action(target,info['id']), info['floor'], 'replyFloor')
            else:
                answer += '女仆请你吃了一个大嘴巴子\n女仆：“没有这种酒！”\n\n（如果需要“发明”新的酒类，请参考三楼的说明）'
                print('err')
        elif('点酒' in content):
            target = content[content.index('点酒')+1]
            target = self.maid.menu.checkName(target)
            if(target != '错误发生' or crt_maid == 'ptilopsis'):
                answer += self.maid.action(target, info['id'], maid=crt_maid)
                # self.insertCommand(self.maid.action(target,info['id']), info['floor'], 'replyFloor')
            else:
                answer += '女仆请你吃了一个大嘴巴子\n女仆：“没有这种酒！”\n\n（如果需要“发明”新的酒类，请参考三楼的说明）'
                print('err')
        elif('调酒' in content):
            start_index = content.index('调酒')+1
            formula = self.maid.menu.getFullFromula()
            for i in range(start_index, start_index+4):
                print(content[i])
                formula[self.maid.menu.checkMaterial(content[i])] += 1
            print(formula)
            target = self.maid.menu.check(formula)
            if(target != '错误发生' or crt_maid == 'ptilopsis'):
                answer += self.maid.action(target, info['id'], maid=crt_maid)
                # self.insertCommand(self.maid.action(target,info['id']), info['floor'], 'replyFloor')
            else:
                answer += '女仆请你吃了一个大嘴巴子\n女仆：“不要乱玩调酒机！”\n\n（如果需要“发明”新的酒类，请参考三楼的说明）'
                print('err')
        elif('发明' in content):
            start_index = content.index('发明')+1
            title = content[start_index]
            desc = content[start_index+1]
            formula = content[start_index+2:start_index+6]
            drink_info = ''
            for i in range(start_index+6,len(content)-8):
                drink_info += content[i] + '\n'
            
            _formula = self.maid.menu.getFullFromula()
            for i in formula:
                _formula[self.maid.menu.checkMaterial(i)] += 1
            _name = self.maid.menu.checkName(title)
            if drink_info == '占位':
                answer += nga_text.b('操作失败！') + '输入格式错误\n'
            elif (_name == '错误发生' or str(self.maid.menu.menu[_name]['author']) == str(info['id'])) \
                    and (self.maid.menu.check(_formula) == '错误发生' or title == self.maid.menu.check(_formula)):
                self.maid.menu.addAlc(
                    title, desc, drink_info, formula, author=info['id'])
                answer += nga_text.b('操作成功！') + '新的配方已记录\n\n' + self.maid.menu.showDrink(title)
            else:
                answer += nga_text.b('操作失败！') + '已有同名酒或同款配方存在\n'

        if('查看' in content ):
            answer += '\n' + self.maid.user.showUser(str(info['id']), 1)
        if(answer != ''):
            self.insertCommand(answer, info['floor'], 'replyFloor')

    def infomation(self):
        if os.path.exists('resource/infomation'):
            try:
                with open('resource/infomation', 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                return ''

    def mainLoop(self):
        self.cnt=0
        while True:
            # 查楼
            while True:
                rtn = self.crawler.get(
                    self.log['theme'], self.log['lastFloor']+1)
                if(rtn['status'] == 0):
                    _rtn = self.crawler.get(
                        self.log['theme'], self.log['lastFloor']+2)
                    if(_rtn['status'] != 0):
                        self.cnt+=1
                    if(self.cnt>30):
                        self.log['lastFloor'] = self.log['lastFloor']+1
                        continue
                    break
                self.log['lastFloor'] = self.log['lastFloor']+1
                self.cnt = 0
                self.check(rtn)
            # 定期编辑二楼内容
            if(self.log['lastEdit']+3600 < time.time()):
                s = self.infomation()+self.maid.menu.showRecommend()+self.maid.user.showList()
                self.insertCommand(s, 1, 'edit')
                self.log['lastEdit'] = (math.floor(time.time()/3600))*3600
            # 执行一个
            if(self.lastTimestamp < time.time()):
                if(len(self.log['log']) != 0):
                    crt = self.log['log'][0]
                    if(self.exe(crt)):
                        print('成功执行：', crt, getTime())
                        self.log['log'].pop(0)
                        self.lastTimestamp = time.time()
            self.save()
            if os.path.exists('stop'):
                print('\n\n\n\n\nQUITING!!!!\n')
                self.maid.save()
                self.maid.user.save()
                self.maid.menu.save()
                os.remove('stop')
                return
            time.sleep(2)

    def __init__(self):
        self.load()
        self.crawler = crawler('cookies')
        self.maid = maid()
        self.mainLoop()


if __name__ == '__main__':
    main = client()
