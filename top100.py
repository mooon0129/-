# _*_ coding:utf-8 _*_
import sys
from urllib import request
from scrapy.selector import Selector
import xlwt
import re
import requests
import urllib.request
import gzip
import geturl


# 加上headers
headers = {
    # 'Host': 'book.jd.com',
    # # 'Referer': 'http://item.jd.com/12093815.html',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Charset':'utf-8',

}

def getHtml(url):
    print(url)
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

def getitems(url):
    data = None
    new_list = []
    number = []  # 排名
    ming = []  # 书名
    # jia = []#价格
    xie = []  # 作者
    hao = []  # isbn号
    lei = []  # 分类
    chu = []  # 出版社
    print(u'\n数据获取中，请稍候...')
    for i in range(1,6): #遍历排行榜每一页
        html = getHtml(r'http:'+url+str(i)+'.html')#'+str(i)+'
        # =================文件名组成=================
        file = Selector(text=html).xpath("//li[@class='curr']/a/text()").extract()
        mfile = Selector(text=html).xpath("//dl[@class='curr']/dt/a/text()").extract()
        mmfile = Selector(text=html).xpath("//a[@class='curCate']/text()").extract()
    # print(wenjianming)

        ss = Selector(text=html).xpath("//div[@class='p-detail']")

        for s in ss:

        # ====================================URLs====================================
            urls = s.xpath("./a/@href").extract()
            sku = []
            pattern1 = re.compile(r'\d+')
            sku.append(pattern1.findall(str(urls)))
            # print(urls)
            # print(sku)
        # ====================================书名====================================
            name = s.xpath("./a/@title").extract()
            # print(name)
            ming.append(name)
        # print(ming)
        # ====================================出版社(列表页)====================================
            publisher = s.xpath("./dl[2]/dd/a/@title").extract()
            chu.append(publisher)
            # print(urls)
            # print(publisher)

        # ====================================价格====================================
        #     u = r'http://p.3.cn/prices/mgets?type=1&skuIds=J_12093815,J_12093815,J_12093815,J_12209562,J_12209562,J_12209562,J_11757204,J_11757204,J_11757204,J_12378376,J_12378376,J_12378376,J_12332117,J_12332117,J_12332117,J_12111106,J_12111106,J_12111106,J_10033621,J_10033621,J_10033621,J_10033620,J_10033620,J_10033620,J_12377573,J_12377573,J_12377573,J_12239650,J_12239650,J_12239650,J_12090377,J_12090377,J_12090377,J_11757834,J_11757834,J_11757834,J_11941728,J_11941728,J_11941728,J_11501914,J_11501914,J_11501914,J_12351952,J_12351952,J_12351952,J_12257413,J_12257413,J_12257413,J_12125924,J_12125924,J_12125924,J_11911791,J_11911791,J_11911791,J_11687858,J_11687858,J_11687858,J_12327282,J_12327282,J_12327282&callback=jQuery7233592&_=1531997332379'
        #     content = getHtml(u)
        #     json_str = content[len(r'jQuery7233592('): -1]
        #     pattern = re.compile(r'\"op\"\:\"[\d.]*\"')
        #     jia = pattern.findall(json_str)
        #     # print(jia)

            for j in range(0, len(urls)):  #开始从详情页拿信息
                html2 = getHtml('http:' + urls[j])
                # print(html2)
        # ====================================isbn号====================================
                isbn = []
                # for i in isbns:
                #     if i.find('ISBN')!=-1 or i.find('商品编码')!=-1:
                #         print(i)
                #         isbn=i
                isbns = Selector(text=html2).xpath(".//ul[@id='parameter2']/li/text()").extract()
                flag = False
                for i in isbns:
                    if re.search(r".*ISBN.*", i):
                        isbn = i
                        # print(isbn)
                        hao.append(isbn)
                        flag = True

                if not flag:
                    # print(url[j])
                    hao.append('NO-ISBN')
                # print(isbn)
        # ====================================分类====================================
                category = Selector(text=html2).xpath(".//div[@class='crumb fl clearfix']/div[@class='item'][position()>0]/a/text()").extract()
                lei.append(category)
                # print(category)
        # ====================================作者====================================
                wr = Selector(text=html2).xpath(".//div[@class='p-author']/a/text()").extract()
                if wr is not None:
                    writer = Selector(text=html2).xpath(".//div[@class='p-author']/a/text()").extract()
                    xie.append(writer)
    # print(ming)
    # print(xie)
    # print(hao)
    # print(chu)
    #----------------------------------将数据放入一个列表---------------------------------------
    for n in range(1, len(ming)+1):
        number.append(n)

    # print(len(number))
    # print(len(ming))
    # print(len(hao))
    # print(len(lei))
    # print(len(chu))
    # print(len(xie))
    # print(len(jia))
    # for i in range(len(sku)):
    #     print(sku[i])
    print(file, mfile, mmfile)
    for i in range(0, len(ming)):
        # print(number[i],ming[i], hao[i], lei[i],chu[i], xie[i])
        # print(i)
        new_list.append([number[i], ming[i], hao[i], lei[i], chu[i], xie[i]])
    # print(new_list)
    #----------------------------------创建Excel文件---------------------------------------
    new = xlwt.Workbook()
    sheet = new.add_sheet('Book', cell_overwrite_ok=True)
    row_num = len(new_list)
    heads = [u'排名', u'书名', u'ISBN号', u'分类', u'出版社', u'作者']
    #----------------------------------存入数据---------------------------------------
    print(u'\n数据写入中...')
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
    new.save(str(file+mfile+mmfile).replace('/', '-')+'.xls')
    print(u'\n写入完成！')

for u in range(len(geturl.finalurl)):
    getitems(geturl.finalurl[u])