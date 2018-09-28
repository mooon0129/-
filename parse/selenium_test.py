# -*- coding: utf-8 -*-

'''模拟人为操作浏览器浏览器对动态页面进行获取'''

from selenium import webdriver
from scrapy.selector import Selector

broswer = webdriver.Chrome(executable_path="D:/tools/chromedriver.exe")


url_list = ['http://item.jd.com/11967827.html','http://item.jd.com/11796725.html']
for i in range(2):

    broswer.get(url_list[i])

    # print(broswer.page_source)

    t_selector = Selector(text=broswer.page_source)

    for sel in t_selector.xpath("//div[@class='product-intro m-item-grid clearfix']"):
        name = sel.xpath(".//div[@class='sku-name']/text()").extract_first().split()
        price = sel.xpath(".//strong[@class='p-price']/text()").extract_first().split()
        # comment = sel.xpath(".//p[@class='comment-con']/text()").extract_first()
        print(name,price)
    # print(comment)

# print(t_selector.css('div.p-name').xpath('string(.//em)').extract_first())
broswer.quit()