#!/usr/bin/env python
#!encoding=utf-8
# import html2text
import sys
import requests
import os
import _mysql
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")

rootUrl = 'http://www.jianshu.com'
def fetchArtiList(url):

    resp  = requests.get(url)
    if resp.status_code != requests.codes.ok:
        print 'connect err'
        return
    # parse html
    soup = BeautifulSoup(resp.text, "html.parser")
    list = soup.find('ul', class_ = 'note-list').find_all('li')
    for child in list:
        articleUrl = child.find('a', class_ = 'title').get('href')
        article = Article()
        article.parseHtml(rootUrl + articleUrl)
        print article
        article.saveToSql()
    print 'download finish'
class Article:
    '''
    this class is a bean of article of jianshu
    '''
    db = _mysql.connect(user='root', passwd='152256')
    db.query('create database if not exists jianshu_blog;')
    db.query('use jianshu_blog')
    db.query('''
    create table if not exists posts(
    id     int unsigned not null primary key auto_increment,
    title  varchar(200),
    author varchar(100),
    publish varchar(50),
    isdeleted int,
    content text,
    visitcount int
    ) CHARACTER SET = utf8mb4;
    ''')

    def __init__(self):
        self.title = 'python article'

    def close(self):
        self.db.close()

    def parseHtml(self, url):
        '''
        parse article object from html
        '''
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            print 'get articles details error'
            return
        soup = BeautifulSoup(resp.text, "html.parser")
        self.title = soup.find('h1', class_ = 'title').contents[0].encode('utf-8')
        author_area = soup.find('div', class_ = 'author')
        self.author= author_area.find('span', class_ = 'name').contents[0].string.encode('utf-8').decode('utf-8')
        self.date = author_area.find('span', class_ = 'publish-time').string.encode('utf-8').decode('utf-8')
        self.isDeleted = 0
        self.content = soup.find('div', class_ = 'show-content').prettify().encode('utf-8').decode('utf-8')
        self.visitCount = 0

    def saveToSql(self):
        '''
        save the article object to mysql
        '''
        self.content = _mysql.escape_string(self.content)
        stat = "insert into posts(title, author, publish, isdeleted, content, visitcount) values('%s', '%s', '%s', %d, '%s', %d);" % (self.title, self.author, self.date, self.isDeleted, self.content,self.visitCount)
        self.db.query(stat)
        self.db.commit()

    def queryPosts(self):
        self.db.query("select * from posts limit 1")
        r = self.db.store_result()
        return r

    def __str__(self):
        return self.title

if __name__ == '__main__':
    # home url
    # pool = ThreadPoolExecutor(max_workers = 5)
    for i in range(100):
        url = 'http://www.jianshu.com/trending/monthly?page=' + str(i) + '&seen_snote_ids%5B%5D=9417518&seen_snote_ids%5B%5D=9975670&seen_snote_ids%5B%5D=9983984&seen_snote_ids%5B%5D=9707970&seen_snote_ids%5B%5D=9650477&seen_snote_ids%5B%5D=10065620&seen_snote_ids%5B%5D=10239288&seen_snote_ids%5B%5D=9917498&seen_snote_ids%5B%5D=10066091&seen_snote_ids%5B%5D=10050042&seen_snote_ids%5B%5D=10443321&seen_snote_ids%5B%5D=9417837&seen_snote_ids%5B%5D=10133511&seen_snote_ids%5B%5D=10189199&seen_snote_ids%5B%5D=9587458&seen_snote_ids%5B%5D=9824208&seen_snote_ids%5B%5D=10465818&seen_snote_ids%5B%5D=10094112&seen_snote_ids%5B%5D=8446458&seen_snote_ids%5B%5D=9654829&seen_snote_ids%5B%5D=10270938&seen_snote_ids%5B%5D=9615234&seen_snote_ids%5B%5D=10214421&seen_snote_ids%5B%5D=9773030&seen_snote_ids%5B%5D=9711009&seen_snote_ids%5B%5D=4037395&seen_snote_ids%5B%5D=9956672&seen_snote_ids%5B%5D=10073961&seen_snote_ids%5B%5D=10426676&seen_snote_ids%5B%5D=9991656&seen_snote_ids%5B%5D=1673306&seen_snote_ids%5B%5D=9758940&seen_snote_ids%5B%5D=8890764&seen_snote_ids%5B%5D=8322472&seen_snote_ids%5B%5D=10030271&seen_snote_ids%5B%5D=9750272&seen_snote_ids%5B%5D=10004435&seen_snote_ids%5B%5D=9948893&seen_snote_ids%5B%5D=10173942&seen_snote_ids%5B%5D=10273136&seen_snote_ids%5B%5D=3917938&seen_snote_ids%5B%5D=10026414&seen_snote_ids%5B%5D=10269783&seen_snote_ids%5B%5D=10358287&seen_snote_ids%5B%5D=9699370&seen_snote_ids%5B%5D=9667708&seen_snote_ids%5B%5D=10470244&seen_snote_ids%5B%5D=10336939&seen_snote_ids%5B%5D=9527534&seen_snote_ids%5B%5D=9840301&seen_snote_ids%5B%5D=10142398&seen_snote_ids%5B%5D=8858992&seen_snote_ids%5B%5D=10006455&seen_snote_ids%5B%5D=9921576&seen_snote_ids%5B%5D=10033208&seen_snote_ids%5B%5D=9832396&seen_snote_ids%5B%5D=10195409&seen_snote_ids%5B%5D=10580212&seen_snote_ids%5B%5D=10501064&seen_snote_ids%5B%5D=9889215'
        fetchArtiList(url)
