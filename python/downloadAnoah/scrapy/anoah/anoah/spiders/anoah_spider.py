#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest

class AnoahSpider(scrapy.Spider):
    name = 'anoah'
    allowed_domins = ['e.anoah.com', 'www.anoah.com']
    start_urls = ['http://www.anoah.com/ebag/user/index.html']
    headers = {
        'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language':'en-US,zh-CN;q=0.8,zh;q=0.6,en;q=0.4',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Host':'www.anoah.com',
        'Pragma':'no-cache',
        'cookies': 'ebag_login_info=14c4b06b824ec593%25C3%25A3w%25C4%258F%25C2%25A6%25C3%25A5%25C2%2584%25C4%25A5%25C2%25B7%25C3%2585%255E%25C3%2585L%25C2%25B7V%25C3%2587X%25C3%25B1%25C2%258D%25C4%258D%25C2%25A8%25C3%25BB%25C2%258D%25C4%2583%25C2%259C239362517f538b295f4dcc3b5aa765d6%25C2%259Fn%257CK%25C2%258C%255B%25C2%25A3r%25C3%2588%25C2%2597%25C2%25AAy1d8327deb882cf99;ebag_username=liangyaodeng; ebag_password=111111; ebag_remember=1; ebag_proxy=0; uuid=CqsWb1lPL8B4iVnbGDL+Ag==; PHPSESSID=n26b6htrsbqa0kdf4ebf1ger87; SERVERID=6d95a1e4a5b5438037213b565f9be4cd|1498363133|1498361792',
        'Referer':'http://www.anoah.com/ebag/index.php/?r=course',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }

    def start_requests(self):
        return [Request(self.start_urls[0],headers=self.headers,
                        meta={'cookiejar':1},callback=self.post_login)]

    def post_login(self, response):
        print('prepare login')
        print(response.headers)
        return [FormRequest.from_response(response, "http://www.anoah.com/ebag/index.php?r=user/ajaxlogin&callback=jQuery20309346813540861478_1498363131696",
                                          headers=self.headers,
                                          formdata={
                                              'username': 'liangyaodeng',
                                              'password': '111111',
                                              'rememberMe': '0',
                                          }
        )]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
