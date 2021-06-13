import yaml
import os
import random
import nga_text
import time


class menu:
    menu = {}
    rule = {}
    full_formula = {}
    tot = 0

    def __init__(self):
        self.load()
        # self.changeAlc()

    def load(self):
        if os.path.exists('resource/menu.yaml'):
            with open('resource/menu.yaml', 'r', encoding='utf-8') as f:
                data = yaml.load(f.read(), Loader=yaml.FullLoader)
                self.menu = data['menu']
                self.rule = data['rule']
                self.full_formula = data['full_formula']
                self.tot = data['tot']

    def save(self):
        data = {}
        data['tot'] = self.tot
        data['menu'] = self.menu
        data['rule'] = self.rule
        data['full_formula'] = self.full_formula
        yaml_menu = yaml.dump(data, allow_unicode=True)
        with open('resource/menu.yaml', 'w', encoding='utf-8') as f:
            f.write(yaml_menu)

    def changeAlc(self):
        val = 'y'
        while True:
            val = input('插入新的酒吗？Y/y确认')
            if val == 'y' or val == 'Y':
                self._addAlc()
            else:
                break

    def test(self):
        #print(self.menu['熊熊烈火']['info'])
        for key, value in self.menu.items():
            print(value)

    def _addAlc(self):
        item = {}
        item['title'] = input('Input title:')
        item['desc'] = input('Input desc:')
        print('Input info:')
        endstr = 'end'
        info = ''
        for line in iter(input, endstr):
            info += line + '\n'
        item['info'] = info
        item['formula'] = {}
        item['formula']['water'] = input('Formula WATER:')
        item['formula']['suger'] = input('Formula SUGAR:')
        item['formula']['alcohol'] = input('Formula ALCOHOL:')
        self.menu[item['title']] = item

    def addAlc(self, title, desc, info, formula, author=60178730):
        item = {}
        item['title'] = title
        item['desc'] = desc
        item['info'] = info
        item['author'] = author
        item['formula'] = {}
        for i in formula:
            crt_material = self.checkMaterial(i, ifCreate=True)
            if crt_material in item['formula']:
                item['formula'][crt_material] += 1
            else:
                item['formula'][crt_material] = 1
        self.menu[item['title']] = item
        self.save()

    def _showDrink(self, drink):
        if(random.random()>0.5):
            s = "[img]https://s.im5i.com/2021/04/01/WG4py.gif[/img]"
            return s
        s = nga_text.b(nga_text.size(drink, '110%')) + '\n'
        s += nga_text.i(self.menu[drink]['desc']) + '\n\n'
        s += self.menu[drink]['info']
        if drink.find('色图')!=-1 or drink.find('涩图')!=-1:
            try:
                with open('resource/setu.yaml', 'r', encoding='utf-8') as f:
                    setu = yaml.load(f.read(), Loader=yaml.FullLoader)
                    if len(setu)!=0:
                        tgt=setu[random.randint(0, len(setu)-1)]
                        print(tgt)
                        s += f"\n[img]{tgt['pic']}[/img]\npixiv:{tgt['id']}"
            except:
                print('获取色图失败！')
        return s

    def showDrink(self, drink):
        return nga_text.collapse(self._showDrink(drink), drink)

    def checkMaterial(self, material, ifCreate=False):
        if(material not in self.rule):
            if ifCreate:
                self.full_formula[str(self.tot)] = 0
                self.rule[material] = str(self.tot)
                self.tot += 1
                return str(self.tot-1)
            else:
                return 'null'
        return self.rule[material]

    def getFullFromula(self):
        # {'water': 0, 'suger': 0, 'alcohol': 0, 'null': 0}
        return self.full_formula.copy()

    def setTimestamp(self, drink):
        self.menu[drink]['timestamp'] = time.time()

    def check(self, formula):
        for key, value in self.menu.items():
            target = value['formula']
            flag = True
            for i, j in target.items():
                #print(i, j, formula[i])
                if str(formula[i]) != str(j):
                    flag = False
                    break
            if flag:
                print(key)
                return key
        return self.checkName('错误发生')

    def checkName(self, name):
        if(name in self.menu):
            print(name)
            return name
        return self.checkName('错误发生')

    def ranDrink(self):
        n = len(self.menu)
        return list(self.menu.keys())[random.randint(0, n-1)]

    def showRecommend(self):
        s = '[b][size=150%]酒品推荐[/size][/b]\n\n'
        bs = ''
        lst = []
        lst.append(self.ranDrink())
        for i in range(9):
            while True:
                t = self.ranDrink()
                if t not in lst:
                    lst.append(t)
                    break
        for i in lst:
            bs += nga_text.b(nga_text.size(i, '110%'))+', '
        bs += '\n'
        for i in lst:
            bs += '\n'+self._showDrink(i)+'\n'
        s += nga_text.collapse(bs, '随机推荐十款酒品')
        ts = ''
        for i in self.menu:
            ts += nga_text.b(i) + ', '
        s += nga_text.collapse(ts, '完整酒单')
        return s


if __name__ == '__main__':
    new = menu()
    cnt = 0
    for key, value in new.menu.items():
        if value['author'] == 34500815:
            cnt+=1
    print(cnt)
    # print(new.showDrink('色图'))
    # print(new.showRecommend())
    #new.setTimestamp('埃及颂')
    # new.addAlc('调试', '测试', '测试22222', ['披萨', '汉堡', '汉堡', '汉堡'])
    # new.check({'water': 0, 'suger': 0, 'alcohol': 0, '0': 1, '1': 3})
    # new.save()
    # print(new.showDrink('水'))
