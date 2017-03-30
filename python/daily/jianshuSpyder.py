#!/usr/bin/env python
#!encoding=utf-8
import html2text
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == '__main__':
    # home url
    # with open("./article.html", "r") as reader:
    #     content = reader.read()
    #     markdown = html2text.html2text(content)
    #     with open("./article.md", "w") as writer:
    #         writer.write(markdown)
    test = '<img src="http://upload-images.jianshu.io/upload_images/1262158-b2e867db018b6cc3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240">中文</img>'
    soup = BeautifulSoup(test, "html.parser")
    print soup.img.contents[0].encode('utf-8')
    # print html2text.html2text(test)
