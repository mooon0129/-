from scrapy.selector import Selector
import xlwt
import re
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'http://search.jd.com/Search?keyword=%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE&sid=1000005720&ev=publishers_%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE%5E&psort=3&click=0',
    'X-Requested-With': 'XMLHttpRequest'
}

def gethtml(url):
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
        print(res.encoding, "is not ok")
        try:
            bb = res.text.encode('gbk')
            code = 'gbk'
        except:
            print("gbk is not ok")
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

data = None
urls = []
new_list = []
ming = []
xie = []
hao = []
lei = []
number = []

print(u'\n数据爬取中，请稍候……')
html = gethtml(r'http://search.jd.com/Search?keyword=%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE&sid=1000005720&ev=publishers_%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE%5E&psort=3&click=0')  # 起始url
# 注意headers中的请求
ss = Selector(text=html).xpath(
        "//ul[@class='gl-warp clearfix']")  # 总标签

file = Selector(text=html).xpath("//a[@class='crumb-select-item']/em/text()").extract()
for s in ss:
    # print(s)

    label = s.xpath("//li/div[@class='gl-i-wrap']/div[1]/@class").extract()
    url = s.xpath("./li/div[@class='gl-i-wrap']/div[@class='p-name']/a/@href").extract()
    for i in range(1):
        if label[i] == 'gl-i-tab':
            url[i] = s.xpath(".//div[@class='tab-content-item tab-cnt-i-selected']/div[@class='p-name']/a/@href").extract()
            urls.append(url[i][1])
        else :
            url = s.xpath("//li/div[@class='gl-i-wrap']/div[@class='p-name']/a/@href").extract()
            for k in range(len(url)) :
                urls.append(url[k])
# for i in range(len(urls)):
#     print(urls[i])
# ----------------------------------(二次请求)获取剩余30本的url----------------------------------
u = r'http://search.jd.com/s_new.php?keyword=%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE&sid=1000005720&psort=3&ev=publishers_%E4%BA%BA%E6%B0%91%E6%96%87%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE%5E&page=2&s=31&scrolling=y&log_id=1532669455.24309&tpl=2_M&show_items=12209562,12093815,11555910,12246051,12226988,11253398,10008248,10008249,11954069,10008245,11049635,10120120,11095900,12105371,11555905,12144001,12276992,11555893,12279401,12299136,11837713,11869571,12349230,12128057,10008478,12299132,12365839,12235207,12108531,11975673'
content = gethtml(u)
label_2 = Selector(text=content).xpath("//li/div[@class='gl-i-wrap']/div[1]/@class").extract()
for i in range(30):
    if label_2[i] == 'gl-i-tab':
        url_2[i] = Selector(text=content).xpath(".//div[@class='tab-content-item tab-cnt-i-selected']/div[@class='p-name']/a/@href").extract()
        urls.append(url_2[i][1])
    else :
        url_2 = Selector(text=content).xpath("//li/div[@class='gl-i-wrap']/div[@class='p-name']/a/@href").extract()
        for k in range(len(url_2)) :
            urls.append(url_2[k])

#----------------------------------获取详情页数据---------------------------------------
for j in range(0,60):
    html2 = gethtml('http:' + urls[j])  # http://item.jd.com/12093815.html
        # print(html2)

    name = Selector(text=html2).xpath(".//div[@class='sku-name']/text()").extract()
    ming.append(name)


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
        print('无作者')
        # time.sleep(2)

# print(len(ming))
# print(len(hao))
# print(len(lei))
# print(len(xie))
#----------------------------------将数据放入一个列表---------------------------------------
for n in range(1, len(ming)+1):
    number.append(n)

for i in range(0, len(ming)):
    # print(ming[i],hao[i],lei[i],xie[i])
    # print(i)
    new_list.append([number[i], ming[i], hao[i], lei[i], xie[i]])
# print(new_list)
#----------------------------------创建Excel文件---------------------------------------
new = xlwt.Workbook()
sheet = new.add_sheet('Book', cell_overwrite_ok=True)
row_num = len(new_list)
heads = [u'排名', u'书名', u'ISBN号', u'分类', u'作者']
#----------------------------------存入数据---------------------------------------
print(u'\n数据录入中……')
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
new.save(str(file).replace('/', '-')+'.xls')
print(u'\n录入完成！')
