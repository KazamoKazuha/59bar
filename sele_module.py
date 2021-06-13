from selenium import webdriver
import os
import json
import math
import re


class crawler:
    ans = {'status': -1}
    list = []

    def loadCookies(self, tgt='cookies.json'):
        self.driver.delete_all_cookies()
        with open(tgt, 'r') as f:
            list_cookies = json.loads(f.read())
        for i in list_cookies:
            self.driver.add_cookie(i)
        self.driver.get('https://bbs.nga.cn/')

    def saveCookies(self, tgt='cookies.json'):
        cookies = self.driver.get_cookies()
        json_cookies = json.dumps(cookies)
        with open(tgt, 'w') as f:
            f.write(json_cookies)

    def login(self):
        if os.path.exists('cookies.json'):
            # val = input('检查到本地cookies，是否载入？Y/y确认')
            val = 'y'
            if val == 'y' or val == 'Y':
                # try read
                self.loadCookies()
                return
        input('请手动登录，登录完毕后回车以继续')
        self.saveCookies()

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://bbs.nga.cn/')
        self.login()

    def get(self, theme, floor):
        ans = {'status': 1, 'theme': theme, 'floor': floor}
        name = ''
        content = ''
        page = math.ceil((floor+1)/20)
        # print(page)
        try:
            self.driver.get(
                'https://bbs.nga.cn/read.php?tid=%s&page=%s' % (theme, page))
            self.driver.get(
                'https://bbs.nga.cn/read.php?tid=%s&page=%s' % (theme, page))
        except:
            print('network fail!!!')
            ans['status'] = 0
            return
        try:
            # nameFirst = self.driver.find_element_by_xpath(
            #     '//*[@id="postauthor%s"]/b' % (str(floor))).text
            nameSecond = self.driver.find_element_by_xpath(
                '//*[@id="postauthor%s"]' % (str(floor))).text
            name = nameSecond
            print('Get name: ', nameSecond)
        except:
            # print('Get name fail!')
            ans['status'] = 0
            self.ans = ans
            return ans
        print('Current floor:', floor)
        try:
            userId = self.driver.find_element_by_xpath(
                '//*[@id = "posterinfo%s"]/div[1]/a[2]' % (str(floor))).text
            print('Get id: ' + userId)
        except:
            print('Get id fail!')
            ans['status'] = 0
            self.ans = ans
            return ans
        try:
            # //*[@id="pid497085199Anchor"]
            pid = self.driver.find_element_by_xpath(
                '//*[@id="postcontainer%s"]/a[1]' % (str(floor))).get_attribute('id')
            # print(pid)
            pid = re.findall(r'\d+', pid)[0]
            print('Get pid: ' + pid)
        except:
            print('Get pid fail!')
            ans['status'] = 0
            self.ans = ans
            return ans
        try:
            content = self.driver.find_element_by_xpath(
                '//*[@id = "postcontent%s"]' % (str(floor))).text
            content_prefix = ''
            try:
                content_prefix = self.driver.find_element_by_xpath(
                    '//*[@id = "postcontent%s"]/div' % (str(floor))).text
            except:
                pass
            content = content[len(content_prefix):]
            print(content)
        except:
            print('Get content fail!')
            ans['status'] = 0
            self.ans = ans
            return ans
        ans['name'] = name
        ans['id'] = userId
        ans['pid'] = pid
        ans['content'] = content
        self.ans = ans
        self.list = content.split()
        return ans

    def find(self, tgt):
        for i, item in enumerate(self.list):
            if(item == tgt):
                return i
        return -1

    def reply(self, theme, content):
        # https://bbs.nga.cn/post.php?action=reply&tid=25732189
        theme = str(theme)
        content = str(content)
        try:
            self.driver.get(
                'https://bbs.nga.cn/post.php?action=reply&tid=%s' % (theme))
            textArea = self.driver.find_element_by_xpath(
                '//*[@id = "xoxoxxxoxoxxoo"]/span/span/table/tbody/tr[5]/td/textarea')
            textArea.send_keys(content)
            submit = self.driver.find_element_by_xpath(
                '//*[@id = "xoxoxxxoxoxxoo"]/span/table[2]/tbody/tr/td[1]/a')
            submit.click()
            return True
        except:
            print('reply fail!!!')
            return False

    def replyFloor(self, theme, floor, content):
        rtn = self.get(theme, floor)
        if(rtn['status'] != 1):
            print('Get floor fail.', floor)
            return False
        return self._replyFloor(theme, floor, rtn['pid'], content)

    def editFloor(self, theme, floor, content):
        rtn = self.get(theme, floor)
        if(rtn['status'] != 1):
            print('Get floor fail.', floor)
            return False
        return self._replyFloor(theme, floor, rtn['pid'], content, mode='modify')

    def _replyFloor(self, theme, floor, pid, content, mode='reply'):
        # https://bbs.nga.cn/post.php?action=reply&tid=25732189
        # https://bbs.nga.cn/post.php?action=modify&tid=25744165&pid=497083038&article=1
        theme = str(theme)
        floor = str(floor)
        pid = str(pid)
        content = str(content)
        try:
            self.driver.get(
                'https://bbs.nga.cn/post.php?action=%s&tid=%s&pid=%s&article=%s' % (mode, theme, pid, floor))
            textArea = self.driver.find_element_by_xpath(
                '//*[@id = "xoxoxxxoxoxxoo"]/span/span/table/tbody/tr[5]/td/textarea')
            if(mode == 'modify'):
                textArea.clear()
            textArea.send_keys(content)
            submit = self.driver.find_element_by_xpath(
                '//*[@id = "xoxoxxxoxoxxoo"]/span/table[2]/tbody/tr/td[1]/a')
            submit.click()
            return True
        except:
            print('_replyFloor fail!!!')
            return False


if __name__ == '__main__':
    # test
    new = crawler()
    new.get('25744165', 3)
    #print(new.find('Reply'))
    #new.get('25730967', 29)
    #new.editFloor('25744165', 1, '这是一个编辑测试\n修改一楼的内容')
    a = input("test")

# https://bbs.nga.cn/post.php?action=reply&tid=25744165&pid=497085199&article=2
