from urllib import request
from scrapy.selector import Selector

def getHtml(url):  #获取URL

    response = request.urlopen(url)
    html = response.read().decode('gbk')
    return html

html = getHtml(r'http://book.jd.com/booksort.html')#'+str(i)+'
sort = Selector(text=html).xpath("//dl/dt/a/text()").extract()

with open('京东图书全部分类.doc', 'w', encoding='utf-8') as f:
    for i in range(1, len(sort)+1):
        sort1 = Selector(text=html).xpath("//dl/dt[position()=" + str(i) + "]/a/text()").extract()
        sort2 = Selector(text=html).xpath("//dl/dd[position()=" + str(i) + "]/em/a/text()").extract()
        print(sort1)
        print(sort2)
        f.write("{}\n{}\n\n\n".format(sort1, sort2))