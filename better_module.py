from selenium import webdriver
import os
import json
import math
import re

import nga_sdk


class crawler:

    def __init__(self, name='cookies'):
        self.nga = nga_sdk.NGA(name)

    def get(self, theme, floor):
        ans = {'status': 1, 'theme': theme, 'floor': floor}
        page = math.ceil((floor+1)/20)
        rtn = self.nga.get_single_post(str(theme), page=page)
        if rtn == False:
            ans['status'] = 0
            return ans
        page_floor = '-1'
        for i, j in rtn['replys'].items():
            # print(i, j['lou'])
            if str(j['lou']) == str(floor):
                page_floor = i
                break
        if page_floor == '-1':
            # print('BUGGG!!!', rtn['replys'])
            ans['status'] = 0
            return ans
        print(rtn['replys'][str(page_floor)]['lou'])
        # print(rtn['users'])
        try:
            ans['id'] = rtn['replys'][str(page_floor)]['authorid']
        except:
            ans['status'] = 0
            return ans
        ans['name'] = rtn['users'][str(ans['id'])]['username']
        ans['pid'] = rtn['replys'][str(page_floor)]['pid']
        try:
            content = rtn['replys'][str(page_floor)]['content']
        except:
            content = 'skip'
        if str(ans['id']) == '60178730':
            content = 'skip'
        if content.find('[b]Reply') != -1:
            if content.find(')[/b]') != -1:
                content = content[content.find(')[/b]')+5:]
        content = re.split(
            '<.+?>+|\[.+?]+', content)
        content = list(filter(None, content))
        # print(content)
        tmp = ''
        for i in content:
            tmp += i+' '
        ans['content'] = tmp
        return ans

    def find(self, tgt):
        for i, item in enumerate(self.list):
            if(item == tgt):
                return i
        return -1

    def prefixOfReply(self, pid, theme, page, uid, username):
        s = f'[b]Reply to [pid={pid},{theme},{page}]Reply[/pid] Post by [uid={uid}]{username}[/uid] (2021-03-07 00:00)[/b]'
        return s

    def reply(self, theme, content):
        # https://bbs.nga.cn/post.php?action=reply&tid=25732189
        theme = str(theme)
        content = str(content)
        return self.nga.reply_post(theme, '', content)

    def replyFloor(self, theme, floor, content):
        rtn = self.get(theme, floor)
        if(rtn['status'] != 1):
            print('Get floor fail.', floor)
            return False
        prefix = self.prefixOfReply(rtn['pid'], theme, math.ceil(
            (floor+1)/20), rtn['id'], rtn['name'])
        return self.nga.reply_reply('733', rtn['pid'], theme, '', prefix+content)

    def editFloor(self, theme, floor, content):
        rtn = self.get(theme, floor)
        if(rtn['status'] != 1):
            print('Get floor fail.', floor)
            return False
        return self.nga.modify_reply('733', rtn['pid'], theme, '', content)


if __name__ == '__main__':
    # test
    #print(math.ceil((0+1)/20))
    #print(math.ceil((5340+1)/20))
    new = crawler('cookies_2')
    print(new.get('25801672', 5660))
    #print(new.find('Reply'))
    #new.get('25730967', 29)
    # new.replyFloor('25809305', 1,'testtesttest')
    # new.editFloor('25809305', 1, '这是一个编辑测试\n修改一楼的内容')
    # a = input("test")

# https://bbs.nga.cn/post.php?action=reply&tid=25744165&pid=497085199&article=2
