# 作者：_江天万里霜_（NGA）
# 项目地址：https://bbs.nga.cn/read.php?tid=24255913

import requests
import time
import os
import json
import re


def clear_html_re(src_html):
    '''
    正则清除HTML标签
    :param src_html:原文本
    :return: 清除后的文本
    '''
    content = re.sub(r"</?(.+?)>", "", src_html)  # 去除标签
    # content = re.sub(r"&nbsp;", "", content)
    dst_html = re.sub(r"\s+", "", content)  # 去除空白字符
    return dst_html


def logging(text):
    if text.find('ERROR 39') == -1:
        print(text)

# 使用cookies登录，从控制台-网络-当前网址-标头中找到字符串形式存储的cookies作为参数传入。
# * 在控制台使用document.cookie返回的cookie无法用于登录，切记


def set_cookies(cookie_str):
    cookies_1 = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies_1[key] = value
    return cookies_1

# 去除可能存在的的控制字符


def remove_control_chars(str_input):
    return str_input

# lite=js会返回js文件，它的主体是一个json，但包含一个变量名，这里是去除掉这个变量名
# 这里输入的参数应该是一个requests请求的返回对象，返回dict


def translate_js(jstext):
    try:
        return json.loads(remove_control_chars(jstext.text)[33:], strict=False)
    except:
        return {'error': {'0': 'translate_js 错误'}}


class NGA(object):
    def __init__(self, name):
        self.url = "https://bbs.nga.cn"    # 设置泥潭的URL，默认为bbs.nga.cn * 总之记得加斜杠
        self.get_cookies(name)
        self.login()

    def get_cookies(self, name):
        # 在同一目录下存储一个名为cookies的文件储存字符串形式的cookies
        if name in os.listdir('.'):
            logging("检测到已经存在的cookies，尝试使用该cookies...")
            with open(name, "r") as f:
                self.cookies = set_cookies(f.read())
            return True
        else:
            logging("没有检测到cookies，请输入一个...")
            cookie_str = input()
            self.cookies = set_cookies(cookie_str)
            with open("cookies", "w") as f:
                f.write(cookie_str)
            return True

    def login(self):
        # 将cookies写入session
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        # 水区需要登录才能访问，用来做验证
        r = self.session.get(url=self.url + "/thread.php?fid=-7&lite=js")
        if "[查看所需的权限/条件]" not in r.text:
            logging("登录成功...")
            return True
        else:
            logging("登陆失败，打印返回值。你可能需要更新cookies...")
            logging(r.text)
            return False

    # 添加附件(在做了在做了)
    def upload_attachments(self):
        return "", ""

    # 自动翻译检查
    def check_auto_translate(self):
        return 0

    # 获取主题列表
    # thread.php单独访问时显示论坛内的全部主题，添加限制条件可以用于筛选主题，例如此函数所做的那样
    # 而添加一个searchpost字段(默认会赋值1，实际上无需赋值)会显示论坛内的全部回复
    def get_posts(self, fid=0, page=1, recommend=0, order_by=0, nounion=0, authorid=0, searchpost=False):
        fid = f"&fid={fid}" if fid else ""
        page = f"&page={page}"
        recommend = "&recommend=1" if recommend else ""         # 是否搜寻精品贴
        # 排序依据，postdatedesc为按照发帖时间排序，lastpostdesc为按照回复时间排序(默认)
        order_by = f"&order_by={order_by}" if order_by else ""
        authorid = f"&authorid={authorid}" if authorid else ""  # 搜索特定用户的发言
        # 是否搜寻子版面，0为搜寻1为不搜寻
        nounion = f"&nounion={nounion}"
        searchpost = "&searchpost=1" if searchpost else ""      # 见上方注释
        url = self.url + "/thread.php?lite=js" + fid + page + \
            recommend + order_by + nounion + authorid + searchpost
        r = self.session.get(url)
        thread = translate_js(r)

        if 'error' in thread:
            # 如果检测到错误
            logging("ERROR：" + thread['error']['0'])
            return False

        # 原数据是一个键为字符串编号的dict，这里直接转化为list输出更方便索引
        return [i for i in thread['data']['__T'].values()]

    # 获取特定主题的内容
    def get_single_post(self, tid, page=1, authorid=0):
        tid = f"&tid={tid}"                                     # 这里tid就是必选的了
        page = f"&page={page}"
        authorid = f"&authorid={authorid}" if authorid else ""  # 搜索特定用户的发言
        url = self.url + "/read.php?lite=js" + tid + page + authorid
        r = self.session.get(url)
        read = translate_js(r)

        if 'error' in read:
            # 如果检测到错误
            logging("ERROR：" + read['error']['0'])
            return False

        # 这里需要输出主题信息、主题中的用户信息以及每层的内容，就不转化为list了(可能存在抽楼，楼层号不一定是连续的)，就改一下键名
        return {
            "forum": read['data']['__F'],
            "post": read['data']['__T'],
            "replys": read['data']['__R'],
            "users": read['data']['__U']
        }

    # 发表新主题，要求的是fid(版面号)

    def new_post(self, fid, post_subject, post_content):
        return self.posting(fid=fid, url=self.url + f"/post.php?fid={fid}&lite=js", action='new', subject=post_subject, content=post_content)

    # 回复一个主题，要求的是tid(主题号)
    def reply_post(self, tid, reply_subject, reply_content):
        return self.posting(tid=tid, url=self.url + f"/post.php?tid={tid}&lite=js", action='reply', subject=reply_subject, content=reply_content)

    # 编辑一个主题，要求的是tid
    def modify_post(self, tid, post_subject, post_content):
        return self.posting(tid=tid, url=self.url + f"/post.php?tid={tid}&lite=js", action='modify', subject=post_subject, content=post_content)

    # 回复一个回复
    # 1. 对回复的操作除了pid(回复号)，fid和tid也都需要提供(为什么呀)
    # 2. 事实上回复一个回复是通过引用的形式完成的，即你点击回复按钮之后会在输入栏里默认加载类似于
    #    [b]Reply to [pid=450243169,15617411,1]Reply[/pid] Post by [uid=36270126]_江天万里霜_[/uid] (2020-09-05 01:01)[/b]
    #    的内容，但是使用API发表回复时你需得手动添加进去。
    # 3. 虽然但是，即使回复中没有引用的内容，只要是通过reply这一post请求发送的回复都会使被回复方收到消息。
    def reply_reply(self, fid, pid, tid, reply_subject, reply_content):
        return self.posting(pid=pid, url=self.url+f"/post.php?pid={pid}&tid={tid}&lite=js", action='reply', subject=reply_subject, content=reply_content)

    # 编辑一个回复，同上
    def modify_reply(self, fid, pid, tid, reply_subject, reply_content):
        return self.posting(pid=pid, url=self.url+f"/post.php?pid={pid}&tid={tid}&lite=js", action='modify', subject=reply_subject, content=reply_content)

    # 处理发帖
    def posting(self, fid=0, tid=0, pid=0, url="", action="", subject="", content="内容过短或过长"):
        # 步骤1：在发帖/回复/引用/编辑页面加上lite=js参数和即可输出javscript格式的数据(我他妈也不知道这一步有什么用)
        # 那就不要了
        # 步骤2：添加附件
        attachments, attachments_check = self.upload_attachments()

        # 步骤3：查询版面是否存在强制分类

        # 步骤4：获取版面翻译表
        has_auto_translate = self.check_auto_translate()

        # 步骤5：提交POST
        post_data = {
            "step": 2,
            "action": action,
            "post_subject": subject,
            "post_content": content,
            "attachments": attachments,
            "attachments_check": attachments_check,
            "has_auto_translate": has_auto_translate,
            "__inchst": "UTF8"
        }
        if fid:
            post_data['fid'] = fid
        if tid:
            post_data['tid'] = tid
        if pid:
            post_data['pid'] = pid

        r = self.session.post(url=url, data=post_data, cookies=self.cookies)
        result = translate_js(r)

        if result['data']['__MESSAGE']['0'] == "":
            # __MESSAGE字段的0是错误ID，不返回则说明发帖成功，打印提示信息文字(字段1和2)并返回True
            # 注意二哥给的数据接口文档里字段2是HTTP状态码，但是现在是3
            logging(result['data']['__MESSAGE']['1'])
            return True
        else:
            # 若错误则返回错误的具体内容
            logging("ERROR " + result['error']['0'] + " " +
                    result['error']['1'] + " " + result['error']['2'])
            return False


if __name__=='__main__':
    new=NGA('cookies_2')
    new.get_single_post(25801672)
