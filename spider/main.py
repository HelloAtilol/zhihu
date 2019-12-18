# -*- coding: utf-8 -*-
# @Time        : 2019/12/17 10:29
# @Author      : 王诚坤
# @Description : 获取知乎LIVE的相关信息

import pymysql
import requests
import time
import random

# 建立数据库连接
conn = pymysql.Connect(host='localhost', port=3306, user='root', passwd='sim509', db='zhihu', charset='utf8')
cursor = conn.cursor()

header = {
    # ":authority": "www.zhihu.com",
    # ":method": "GET",
    # ":path": "/",
    # ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "_zap=bcef7982-47d5-4456-a93c-63d3471647e0; _xsrf=0YOyTG3zUSSuJHUDszOe8eG6wWOj7LAN; d_c0=\"AECtq62ZQRCPTmaJgtOsjE0LpEz4Uk4RfnY=|1572060268\"; tst=r; q_c1=d61fec4919ec4a20b8c99b452368da78|1576472416000|1576472416000; __utma=155987696.1629157950.1576475861.1576475861.1576475861.1; __utmz=155987696.1576475861.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); tgw_l7_route=116a747939468d99065d12a386ab1c5f; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1576481094,1576481130,1576486148,1576491425; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1576491749; capsion_ticket=\"2|1:0|10:1576491786|14:capsion_ticket|44:YzY3NDUxNDEwMjQ3NDU1MmJjMzhkMDEyNTUwZGMyMWI=|4f691f9b5fc5474a760260dba6b61026f88de4beb27b9b12bb80eea7f3c22a33\"; z_c0=\"2|1:0|10:1576491831|4:z_c0|92:Mi4xM0tjSEFRQUFBQUFBUUsycnJabEJFQ1lBQUFCZ0FsVk5ONm5rWGdBV2NidXR3Ry0zbTRqU1BoSERXc01iWjZhZlZn|80c6515fee6a8cfe37afa36277c5e34895fb923d0f2fa11de0f8dfb0be68bf89\"",
    "referer": "https://www.zhihu.com/signin?next=%2F",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
}


def set_cookie():
    """
    获得已有的cookie
    :return:
    """
    temp_cookies = []
    with open("cookie.txt", 'r') as f:
        while True:
            cookie = f.readline()[:-1]
            if not cookie:
                break
            temp_cookies.append(cookie)
    return temp_cookies


cookies = set_cookie()


def set_header():
    """
    随机切换header
    :return:
    """
    global header
    new_cookie = random.choice(cookies)
    header['cookie'] = new_cookie


def get_followers():
    """
    获得所有follower的id
    :return: 所有未爬取的follower
    """
    s_SQL = "SELECT uid FROM followers WHERE flag = 0"
    res = cursor.execute(s_SQL)
    if res:
        return cursor.fetchall()
    else:
        return []


def get_connection():
    """
    与知乎建立连接
    :return:
    """
    u_ids = get_followers()
    i = 0
    for u_id in u_ids:
        # 将url进行解析并进一步处理
        get_lives(u_id[0])
        i += 1
        if i % 10 == 0:
            set_header()
            time.sleep(3)
        if i % 100 == 0:
            time.sleep(60)
        # 更新u_id的flag，保证断点可以继续
        f_sql = "UPDATE followers SET flag = 1 WHERE uid = '%s' and flag = 0" % u_id
        cursor.execute(f_sql)
        conn.commit()


def get_lives(u_id):
    """
    根据u_id获取返回的json
    :param u_id: follower的id
    :return:
    """
    # 测试id
    # u_id = 'b8f89396e6cc6e7f0ac8679552fb69ec'

    print("正在获取用户ID： %s" % u_id)
    # 初始化
    BASH_URL = "https://api.zhihu.com/people/%s/lives"
    # 访问接口
    try:
        r = requests.get(BASH_URL % u_id, headers=header)
        lives = r.json()['data']
        for live in lives:
            deal_data(u_id, live)
    except KeyError:
        return None
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        get_lives(u_id)
    except pymysql.err.InternalError:
        f_sql = "UPDATE followers SET flag = 2 WHERE uid = '%s'" % u_id
        cursor.execute(f_sql)
    except IndexError as e:
        print("出问题的用户id:%s" % u_id)
        print("错误原因：")
        print(e)
        input()


def deal_data(u_id, live):
    """
    将json数据解析并保存到数据库
    :param u_id: follower的id
    :param live: live的json数据
    :return:
    """

    # 定义一个事务，如果未全部完成，则rollback，避免脏数据
    conn.begin()

    live_id = live['id']
    # 更新relations表
    r_sql = "INSERT INTO relations (u_id, l_id) VALUES ('%s', '%s')" % (u_id, live_id)

    cursor.execute(r_sql)

    # 检查live_id是否存在数据库，如果存在，可以直接跳过
    l_s_sql = "SELECT l_id FROM live_url WHERE l_id = '%s'" % live_id
    r_res = cursor.execute(l_s_sql)
    if r_res:
        return None

    # 获取作者信息
    author_str = []
    authors = []
    speaker = {'a_id': live['speaker']['member']['id'], 'name': live['speaker']['member']['name'],
               'description': live['speaker']['description']}
    authors.append(speaker)
    # 如果有共同作者
    speakers = live['cospeakers']
    for s in speakers:
        author = {'a_id': s['member']['id'], 'name': s['member']['name'], 'description': s['description']}
        authors.append(author)
    # 插入作者
    a_s_sql = "SELECT a_id FROM author WHERE a_id = '%s'"
    a_sql = "INSERT INTO author (a_id, name, description) VALUES ('%s', '%s', '%s')"
    for a in authors:
        author_str.append(a['a_id'])
        # 检查作者是否已经存在
        res = cursor.execute(a_s_sql % a['a_id'])
        if not res:
            cursor.execute(a_sql % (a['a_id'], a['name'], a['description']))

    # 获取live_url表需要的信息
    title = live['subject']
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(live['starts_at']))
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(live['ends_at']))
    try:
        message_count = live['folding_message']['count']
    except TypeError as e:
        message_count = 0
    price = live['fee']['original_price']
    score = live['feedback_score']
    reviewer_num = live['review']['count']
    description = live['description']
    # 处理LIVE标签
    tags = live['tags']
    tag_str = []
    for tag in tags:
        tag_str.append(tag['name'])

    # 插入live_url表
    # print(title)
    l_sql = "INSERT INTO live_url (l_id, start_time, end_time, " \
            "message_count, authors, title, price, score, reviewer_num, description, tag) " \
            "VALUES ('%s', '%s', '%s', %d, '%s', '%s', %.2f, %.2f, %d, '%s', '%s')" % \
            (live_id, start_time, end_time, message_count, ';'.join(author_str), title.replace("💡 ", ""),
             price / 100, score, reviewer_num, description.replace("'", "\\'"),
             ';'.join(tag_str))

    cursor.execute(l_sql)

    print('-*' * 30 + "-")
    print("加入最新的LIVE《%s》" % title)
    print('-*' * 30 + "-")


if __name__ == '__main__':
    get_connection()
    conn.close()
