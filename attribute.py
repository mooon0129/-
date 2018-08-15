from urllib import request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import xlwt
import urllib.request
import gzip
import re
import requests
import time

headers = {
     'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

#----------------------------------代理ip---------------------------------------
proxy_url = "175.44.108.92:21325"
username = "public"
password = "tyc68ox8"
proxy_values = "http://{0}:{1}@{2}/".format(username, password, proxy_url)
proxy_handler = {"http": proxy_values, "https": proxy_values, }
handler = request.ProxyHandler(proxy_handler)
opener = request.build_opener(handler)
#---------------------------------------获取url---------------------------------------
count=0
def gethtml(url):

    res = requests.get(url, headers=headers)
    html = res.text
    global count
    count=count+1
    return html


data = None
new_list = []
ming = []
xie = []
hao = []
lei = []

# ----------------------------------起始页列表---------------------------------------
#start_urls = [
#         'http://list.jd.com/list.html?tid=1000921',  童书0-2
#         'http://list.jd.com/list.html?tid=1000922',  童书3-6
#         'http://list.jd.com/list.html?tid=1000923',  童书7-10
#         'http://list.jd.com/list.html?tid=1000925',  童书7-10
#         'http://list.jd.com/list.html?cat=1713,3263,4761',  童书 绘本
#         'http://list.jd.com/list.html?cat=1713,3263,3394',  童书 儿童文学
#         'http://list.jd.com/list.html?cat=1713,3263,3395',  童书 幼儿启蒙
#         'http://list.jd.com/list.html?cat=1713,3263,3399',  童书 科普百科
#         'http://list.jd.com/list.html?cat=1713,3263,3396',  童书 手工游戏
#         'http://list.jd.com/list.html?cat=1713,3263,3391',  童书 动漫卡通
#         'http://list.jd.com/list.html?cat=1713,3263,3401',  童书 少儿英语
#         'http://list.jd.com/list.html?cat=1713,3289,4766',  1年级
#         'http://list.jd.com/list.html?cat=1713,3289,4767',  2年级
#         'http://list.jd.com/list.html?cat=1713,3289,4768',  3年级
#         'http://list.jd.com/list.html?cat=1713,3289,4769',  4年级
#         'http://list.jd.com/list.html?cat=1713,3289,4770',  5年级
#         'http://list.jd.com/list.html?cat=1713,3289,4771',  6年级
#         'http://list.jd.com/list.html?cat=1713,3289,4772',  小升初
#         'http://list.jd.com/list.html?cat=1713,3289,3849',  奥数
#         'http://list.jd.com/list.html?cat=1713,3289,4773',  初一
#         'http://list.jd.com/list.html?cat=1713,3289,4774',  初二
#         'http://list.jd.com/list.html?cat=1713,3289,4775',  初三
#         'http://list.jd.com/list.html?cat=1713,3289,4776',  中考
#         'http://list.jd.com/list.html?cat=1713,3289,3839',  中小学课外读物
#         'http://list.jd.com/list.html?cat=1713,3289,4777',  高一
#         'http://list.jd.com/list.html?cat=1713,3289,4778',  高二
#         'http://list.jd.com/list.html?cat=1713,3289,4779',  高三
#         'http://list.jd.com/list.html?cat=1713,3289,4780'   高考

# ----------------------------------循环列表页页数---------------------------------------
print(u'\n数据爬取中，请稍候……')
for i in range(1, 11):
    html = gethtml(
        r'http://list.jd.com/list.html?cat=1713,3289,4776&page=' + str(i))  # 起始url
    file = Selector(text=html).xpath("//div[@class='trigger']/span/text()").extract()
    # print(wenjianming)
    # Request Response
    # 生成scrapy selector
    ss = Selector(text=html).xpath(
        '//ul[@class="gl-warp clearfix"]')  # 总标签
    #  print(ss)
    # print(len(ss)
#----------------------------------循环详情页---------------------------------------
    for s in ss:
        url = s.xpath(".//div[@class='p-name']/a/@href").extract()
        # print(hh)
#----------------------------------获取详情页数据---------------------------------------
        for j in range(0,60):
            html2 = gethtml('http:' + url[j])  # http://item.jd.com/12093815.html
            # print(html2)
            # print('-'*20)

            name = Selector(text=html2).xpath(".//div[@class='sku-name']/text()").extract()
            print(len(name),name)
            print(url[j])

            ming.append(name)
            # print(ming[i])


            isbn=''
            isbns = Selector(text=html2).xpath(".//ul[@id='parameter2']/li/text()").extract()
            flag=False
            for i in isbns:
                if re.search(r".*ISBN.*", i):
                    isbn = i
                    # print(isbn)
                    hao.append(isbn)
                    flag=True

            if not flag:
                # print(url[j])
                hao.append('NO-ISBN')
            # print(isbn)
            category = Selector(text=html2).xpath(".//div[@class='crumb fl clearfix']/div[@class='item'][position()>0]/a/text()").extract()
            lei.append(category)
            # print(category)
            wr = Selector(text=html2).xpath(".//div[@class='p-author']/a/text()").extract()
            if wr is not None:
                writer = Selector(text=html2).xpath(".//div[@class='p-author']/a/text()").extract()
                xie.append(writer)
            else:
                xie.append('无作者')
            # time.sleep(2)
#----------------------------------将数据放入一个列表---------------------------------------

for i in range(0, len(ming)):
    # print(ming[i],hao[i],lei[i],xie[i])
    # print(i)
    new_list.append([ming[i], hao[i], lei[i], xie[i]])
# print(new_list)
#----------------------------------创建Excel文件---------------------------------------
new = xlwt.Workbook()
sheet = new.add_sheet('Book', cell_overwrite_ok=True)
row_num = len(new_list)
heads = [u'书名', u'ISBN号', u'分类', u'作者']
#----------------------------------存入数据---------------------------------------
# print(u'\n数据录入中……')
ii = 0
# 写入表头项
for head in heads:
    sheet.write(0, ii, head)
    ii += 1
i = 1
# 写入图书信息
for list in new_list:
    j = 0
    for data in list:
        sheet.write(i, j, data)
        j += 1
    i += 1
new.save(str(file).replace('/','-')+'.xls')
print(u'\n录入完成！')
print(count)
