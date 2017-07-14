#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
import re
import os
from anoah.items import Grade, Subject
import json
from scrapy.http import FormRequest
from urllib.parse import urlencode
from urllib.request import urlretrieve,quote

downloadPath = '/home/tiger/disk/anoah/'
class AnoahSpider(scrapy.Spider):
    name = 'anoah'
    allow_domains = 'e.anoah.com'
    start_urls = [
        'http://e.anoah.com/index.php?r=book/select&level=1&style=radio&check=book&callback=onsetBookLcsuccess&school_id=158537&displaymode=1&bookids=1001546',
    ]
    reg = re.compile("o\[\d+\].*")
    base_url = 'http://e.anoah.com/index.php'

    # def start_requests(self):
    #     return [scrapy.FormRequest(start_urls[0])]

    # parse subjects and Grade info 
    def parse(self, response):
        #script text
        script = response.xpath("//script")[3].extract()
        scripts = list(map(lambda x: x.replace("\t\t ", ""), script.split("\r\n")))
        datas = list(filter(lambda x: self.reg.match(x) or x == 'var o=[];', scripts))[1:]
        splitIndex = datas.index("var o=[];")
        subjects = datas[:splitIndex]
        dummGrades = datas[splitIndex + 1:][1:]
        grades = dummGrades[dummGrades.index("o[0]= [];"):]

        #parse subject and grades 
        for g in self.parseGradeItem(grades):
            print(g)
            for s in [x for x in self.parseSubjectItem(subjects) if x['grade'] == g['id']]:
                print(s)
                meta = {
                    'periodId': g['period'],
                    'gradeId': g['id'],
                    'subjectId': s['id'],
                }
                url = self.base_url + "?r=book/select/getEditionNew&period_id=" + g['period'] + "&subject_id=" + s['id']
                yield scrapy.Request(url = url, meta = meta, callback=self.parsePress)

    #parse Press
    def parsePress(self, response):
        presses = json.loads(response.body_as_unicode())
        url = self.base_url + "?r=book/select/getBook"
        for press in [x for x in presses]:#{edu_edition_id:'xxx', edition_name:'xxx'}
            data = {
                'page':1,
                'school_id':'',
                'user_id':'',
                'grade_id':'',
                'subject_id':response.meta['subjectId'],
                'period_id':response.meta['periodId'],
                'view_type':'public',
                'knowledge_subject_id':'',
                'period_id':response.meta['periodId'],
                'edition_id':press['edu_edition_id'],
            }
            yield FormRequest(url = url, body = json.dumps(data), callback = self.parseBook)

    # parse Book
    def parseBook(self, response):
        books = json.loads(response.body_as_unicode())
        for book in books['list']:
            # print("--" + book['name'])
            chapterUrl = "http://e.anoah.com/api/?q=json/ebag/resource/Book/getBookChaptersByChapterid&info={\"edu_book_id\":\"" + book['edu_book_id'] + "\",\"edu_chapter_id\":0}"
            meta = {'book': book}
            yield scrapy.Request(url = chapterUrl, meta = meta, callback=self.parseChapter)

    def parseChapter(self, response):
        chapters = json.loads(response.body_as_unicode())
        chapterList = chapters['recordset']['chapterList']
        level1List = list(filter(lambda x: x['tree_level'] == '1', chapterList))
        level2List = list(filter(lambda x: x['tree_level'] == '2', chapterList))
        level3List = list(filter(lambda x: x['tree_level'] == '3', chapterList))
        book = response.meta.get('book')
        params = {
            'r':'common/resource/getResourceList',
            'page':1,
            'pagesize':10,
            'param[search_type]':'0',
            'param[booktype]':'1',
            'param[period]': book['tree']['period'],
            'param[grade]': book['tree']['grade'],
            'param[subject]': book['tree']['subject'],
            'param[book]': book['edu_book_id'],
            'param[chapter]':'',
            'param[m_category_id]':'1',#1: PPT, 4: Media
            'param[category_id]':'0',
            'param[rstype]':'2',
            'param[qtype]':'0',
            'param[difficulty]':'0',
            'param[year]':'0',
            'param[shengid]':'0',
            'param[kpid]':'0',
            'param[orkpid]':'51',
            'param[gradeid]':'0',
            'param[subjectid]':'0',
            'param[mode]':'0',
            'param[usid]':'0',
            'param[keyword]':'',
            'param[order]':'5',
        }
        meta = {
            'page': 1,
            'pagesize': 10,
            'book': book,
            'category':0,
            'realPath': '',
            'params': params,
        }

        for level1 in level1List:
            # print("---" + level1['name'])
            child = list(filter(lambda x: x['parent_id'] == level1['edu_chapter_id'], level2List))
            if(len(child) == 0):
                params['param[chapter]'] = level1['edu_chapter_id']
                params['param[m_category_id]'] = 0
                meta['realPath'] = level1['name']
                url = self.base_url + "?" + urlencode(params)
                yield scrapy.Request(url = url, meta = meta, callback = self.parseData)
                # params['param[m_category_id]'] = 4
                # meta['category'] = 4
                # yield scrapy.Request(url = self.base_url + "?" + urlencode(params), meta = meta, callback=self.parseData)
                continue
            for level2 in child:
                # print("------" + level2['name'])
                child = list(filter(lambda x: x['parent_id'] == level2['edu_chapter_id'], level3List))
                if(len(child) == 0):
                    params['param[chapter]'] = level2['edu_chapter_id']
                    params['param[m_category_id]'] = 0
                    meta['realPath'] = '/'.join([level1['name'], level2['name']])
                    url = self.base_url + "?" + urlencode(params)
                    yield scrapy.Request(url = url, meta = meta, callback = self.parseData)
                    # params['param[m_category_id]'] = 4
                    # meta['category'] = 4
                    # yield scrapy.Request(url = self.base_url + "?" + urlencode(params), meta = meta, callback=self.parseData)
                    continue
                for level3 in child:
                    # get PPT resources info
                    params['param[chapter]'] = level3['edu_chapter_id']
                    params['param[m_category_id]'] = 0
                    url = self.base_url + "?" + urlencode(params)
                    yield scrapy.Request(url = url, meta = meta, callback=self.parseData)
                    # get media resources info
                    # params['param[m_category_id]'] = 4
                    # meta['category'] = 4
                    # yield scrapy.Request(url = self.base_url + "?" + urlencode(params), meta = meta, callback=self.parseData)

    # parse data list
    def parseData(self, response):
        book = response.meta.get('book')
        category = response.meta.get('category')
        realPath = response.meta.get('realPath')
        params = response.meta.get('params')
        result = json.loads(response.body_as_unicode())
        # download data
        if(book['tree_text']['grade'] is None):
            path = [book['tree_text']['period'], book['tree_text']['subject'],book['tree_text']['term'], book['tree_text']['edition'], book['publish_info'], book['name']]
        else:
            path = [book['tree_text']['period'], book['tree_text']['grade'], book['tree_text']['subject'],book['tree_text']['term'], book['tree_text']['edition'], book['publish_info'], book['name']]
        for data in [x for x in result['data'] if 'down_path' in x]:
            down_path = (downloadPath + "/".join(path) + "/" + realPath + "/" + data['file_extension']).replace("//", "/")
            name = data['title']
            if(len(name) > 100):
                name = name[:100]
            savename = name + "_"+ str(data['pkid']) + "." + data['file_extension']
            down_url = data['down_path']
            if not os.path.exists(down_path):
                os.makedirs(down_path)
            print(down_url)
            print(down_path + "/" + savename)
            urlretrieve(quote(down_url, ':/'), down_path + "/" + savename)

        # is last page?
        curpage = response.meta.get('page')
        pagesize = response.meta.get('pagesize')
        total = result['total']
        if(curpage * pagesize < total):
            params['page'] = curpage + 1
            response.meta['page'] = curpage + 1
            response.meta['params'] = params
            yield scrapy.Request(url = self.base_url + "?" + urlencode(params), meta = response.meta, callback = self.parseData)

    def parseGradeItem(self, glist):
        # % 4 =0,1,2,3 items ==> Grade
        index = 0
        pv = lambda x: self.parseValue(glist[x])
        gs = []
        while(index < len(glist)):
            g = Grade(period = pv(index+1), id = pv(index+2), name = pv(index+3))
            index += 4;
            # yield g
            gs.append(g)
        print(gs[-3:])
        return gs

    def parseSubjectItem(self, slist):
        # 0,1,2,3 ==> Subject
        index = 0
        pv = lambda x: self.parseValue(slist[x])
        ss = []
        while(index < len(slist)):
            s = Subject(grade = pv(index+1), id = pv(index+2), name = pv(index+3))
            index += 4;
            # yield s
            ss.append(s)
        return ss

    def parseValue(self, str):
        value = str[str.index('=')+1:]
        return value[value.index("'") + 1: -2]
