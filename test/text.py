# -*- coding: utf-8 -*-
# @Time        : 2019/12/16 17:35
# @Author      : 王诚坤
# @Description :

import requests
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument("cookie=\"_zap=bcef7982-47d5-4456-a93c-63d3471647e0; _xsrf=0YOyTG3zUSSuJHUDszOe8eG6wWOj7LAN; d_c0=\"AECtq62ZQRCPTmaJgtOsjE0LpEz4Uk4RfnY=|1572060268\"; tst=r; q_c1=d61fec4919ec4a20b8c99b452368da78|1576472416000|1576472416000; __utma=155987696.1629157950.1576475861.1576475861.1576475861.1; __utmz=155987696.1576475861.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); tgw_l7_route=116a747939468d99065d12a386ab1c5f; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1576481094,1576481130,1576486148,1576491425; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1576491749; capsion_ticket=\"2|1:0|10:1576491786|14:capsion_ticket|44:YzY3NDUxNDEwMjQ3NDU1MmJjMzhkMDEyNTUwZGMyMWI=|4f691f9b5fc5474a760260dba6b61026f88de4beb27b9b12bb80eea7f3c22a33\"; z_c0=\"2|1:0|10:1576491831|4:z_c0|92:Mi4xM0tjSEFRQUFBQUFBUUsycnJabEJFQ1lBQUFCZ0FsVk5ONm5rWGdBV2NidXR3Ry0zbTRqU1BoSERXc01iWjZhZlZn|80c6515fee6a8cfe37afa36277c5e34895fb923d0f2fa11de0f8dfb0be68bf89\"")
driver = webdriver.Chrome(chrome_options=option)

def split_cookie():
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
    # s = requests.get("https://www.zhihu.com/people/hlmc01/activities", headers=header)
    # print(s.text)
    a = driver.get("https://www.zhihu.com/people/hlmc01/activities")
    print("测试")


if __name__ == '__main__':
    split_cookie()
