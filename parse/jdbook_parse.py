import configparser
import requests
# import geturl
from scrapy.selector import Selector

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept-Charset':'utf-8'
}

config = configparser.ConfigParser()

def getHtml(url):
    # print(url)
    # 返回页面内容
    res = requests.get(url, headers=headers)
    # print(res.encoding)

    bb = None
    code = ''
    try:
        bb = res.text.encode(res.encoding)
        code = res.encoding
    except:
        # print(res.encoding, "is not ok")
        try:
            bb = res.text.encode('gbk')
            code = 'gbk'
        except:
            # print("gbk is not ok")
            try:
                bb = res.text.encode('utf-8')
                code = 'utf-8'
            except:
                print("utf-8 is not ok")

    # print(code, 'is OK')

    try:
        html = bb.decode('gbk')
    except:
        html = bb.decode('utf-8')

    return html


def get_details(str) :

    config.read('item.cfg',encoding = 'utf-8')
    check = config.has_option('detail', str)
    if str == 'allthing':
        name = Selector(text=html).xpath(config.get('detail', 'name'))[0].extract()
        writer = Selector(text=html).xpath(config.get('detail', 'writer'))[0].extract()
        publisher = Selector(text=html).xpath(config.get('detail', 'publisher'))[0].extract()
        print(name+' / ',writer+' / ',publisher)
    else:
        if check:
            # print('Look!I find it:\n')
            detail = Selector(text=html).xpath(config.get('detail', str))[0].extract()
            print(detail)
        else:
            print('sorry,can not find this detail~\n')


def get_items(str):
    config.read('list.cfg',encoding = 'utf-8')
    check = config.has_option('urls',str)
    if check:
        toplist = getHtml(config.get('urls', str))
        urls = Selector(text=toplist).xpath(config.get('items', 'item')).extract()
        # for i in range(len(urls)):
        #     print(urls[i])
        return urls
    else:
        print('sorry,can not find this list~\n')

        # em = Selector(text=html).xpath(config.get('items','item')).extract()
        # print(em)
        # return em



top = input("please input the list you want(changxiao,xinshu):\n")
item_list = get_items(top)

str = input("please input the detail you want(name,writer,publisher,allthing):\n")
for i in range(len(item_list)):
    html = getHtml(r'http:'+item_list[i])
    get_details(str)