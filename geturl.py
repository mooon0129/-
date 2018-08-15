from urllib import request
from scrapy.selector import Selector
import urllib.request
# headers = {
#      'Cache-Control': 'max-age=0',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9'
# }
#
# #----------------------------------代理ip---------------------------------------
# proxy_url = "175.44.108.92:21325"
# username = "public"
# password = "tyc68ox8"
# proxy_values = "http://{0}:{1}@{2}/".format(username, password, proxy_url)
# proxy_handler = {"http": proxy_values, "https": proxy_values, }
# handler = request.ProxyHandler(proxy_handler)
# opener = request.build_opener(handler)

def getHtml(url):  #获取URL


    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

urls = []
# final = []
finalurl = []
urlist = ['http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10003-1#comfort','http://book.jd.com/booktop/0-1-0.html?category=1713-0-1-0-10003-1#comfort']
for m in range(2):
    html = getHtml(urlist[m])#'+str(i)+'

    url2 = Selector(text=html).xpath("//div[@class='mc']/a/@href").extract()
    for i in range(len(url2)):
        urls.append(url2[i])
        # print(url2[i])

    url22 = Selector(text=html).xpath("//div[@class='mc']/dl/dt/a/@href").extract()
    # print("二级子排行")
    for i in range(len(url22)):
        urls.append(url22[i])
        # print(url22[i])

    url3 = Selector(text=html).xpath("//div[@class='m m-category']/div[@class='mc']/dl/dd/a/@href").extract()
    # print("三级子排行")
    for i in range(len(url3)):
        urls.append(url3[i])
        # print(url3[i])

with open('urls.txt', 'w', encoding='utf-8') as f:
    for i in range(len(urls)):
        finalurl.append(str(urls[i]).replace('10001-1.html#comfort','10003-1'))
        # finalurl.append(str(final[i]).replace('10001-10007-1.html#comfort','10003-10007-'))

        # print(finalurl[i])
        f.write("{}  {}\n".format(i,finalurl[i]))
        # print()
del finalurl[0]
del finalurl[58]
# print(finalurl)
print(len(finalurl))