# -*- coding: utf-8 -*-
import redis
from redis import StrictRedis
import time
import random
import requests
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

# class ip_filter():

# headers = requests.get('https://www.baidu.com/').headers
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'False',
'Host': 'www.baidu.com',
'Upgrade - Insecure - Requests': '1',
'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 69.0 .3497 .81 Safari / 537.36',
}

proxy_url = 'http://dps.kdlapi.com/api/getdps/?orderid=940485658050223&num=20&pt=1&ut=2&format=json&sep=1'

list_key = 'proxy_list' #api中的proxy，Redis中代理ip池存储的key名

lower = 10 #代理池中最少ip量，不够需补充

used_ip_number = 'used_ip_number'#redis中存储使用过的ip数量的key名

def init_redis():
    # 初始化Redis
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r = redis.Redis(connection_pool=pool)
    return r

def download_ip(proxy_url):
    data = requests.get(proxy_url).json()
    if data.get('data').get('count')>0:
        list = data.get('data').get('proxy_list') #将api中json格式解析，得到代理ip列表
        print('此次共获取%d个IP' % len(list))
        return (list) #转集合去重


def check_ip(ip_list):
    good_ip = []
    # print(len(ip_list))
    # while len(ip_list)>0:
    for i in range(len(ip_list)):
        # ip_test = ip_list[i]#random.choice(ip_list)      #ip_list.pop()
        proxy = 'public:tyc68ox8@' + ip_list[i]
        proxy_hander = ProxyHandler({
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        })

        opener = build_opener(proxy_hander)
        try:
            if opener.open('https://www.baidu.com/').status == 200:
                print('哈哈哈~使用IP:%s请求成功！' % ip_list[i])
                good_ip.append(ip_list[i])
                print('当前可用IP共%d个' % len(good_ip))
                # return set(good_ip)
            else:
                print(opener.open('https://www.baidu.com/').status)
        except URLError as e:
            print(e.reason,'%s不可用' % ip_list[i])
    return (good_ip)
        # time.sleep(2)


def push_ip(r,good_ip):
    """将代理ip加入redis中的ip_list"""
    # print(good_ip)
    n=0
    for i in range(len(good_ip)):
        a = r.set(list_key,good_ip[i])
        if a:
            n+=1
    if n>1:
        print('~~~~~~~~~~~~~~成功push了%s个IP~~~~~~~~~~~~~~'% n)
        ips = r.get(list_key)
        print(ips)
    else:
        print('push操作失败')
    return n


if __name__ == '__main__':
    r = init_redis()
    ip_list = download_ip(proxy_url)
    print(ip_list)  #list
    good_ip = check_ip(ip_list)
    # print(good_ip)
    push_ip(r,good_ip)



