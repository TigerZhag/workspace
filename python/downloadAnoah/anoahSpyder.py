import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import urlretrieve, quote, urlopen

base_url = 'http://e.anoah.com'
downloadPath = '/home/tiger/disk/anoah/'

class Grade(object):
    def __init__(self, period, id, name):
        self.period = period
        self.id = id
        self.name = name
    def __str__(self):
        return "id:" + self.id + " period:" + self.period + " name:" + self.name

class Subject(object):
    def __init__(self, grade, id, name):
        self.grade = grade
        self.id = id
        self.name = name
    def __str__(self):
        return "id:" + self.id + " grade:" + self.grade + " name:" + self.name

def parse(response):
    content = BeautifulSoup(response.read(), "lxml")
    script = content.find_all('script')[3].string
    scripts = list(map(lambda x: x.replace("\t\t ", ""), script.split("\r\n")))
    reg = re.compile("o\[\d+\].*")
    datas = list(filter(lambda x: reg.match(x) or x == 'var o=[];', scripts))[1:]
    splitIndex = datas.index("var o=[];")
    subjects = datas[:splitIndex]
    dummGrades = datas[splitIndex + 1:][1:]
    grades = dummGrades[dummGrades.index("o[0]= [];"):]

    ss = parseSubjectItem(subjects)
    for g in parseGradeItem(grades)[-3:]:
        for s in filter(lambda x: x.grade == g.id, ss):
            meta = {
                'pid': g.period,
                'gid': g.id,
                'sid': s.id,
            }
            url = base_url + "?r=book/select/getEditionNew&period_id=" + g.period + "&subject_id=" + s.id
            parsePress(urlopen(url), meta)

def parsePress(response, meta):
    presses = json.loads(response.read().decode('utf-8'))
    url = base_url + "?r=book/select/getBook"
    for press in presses:
        data = {
            'page':1,
            'pagesize':10,
            'school_id':'',
            'user_id':'',
            'grade_id':'',
            'subject_id':meta['sid'],
            'period_id':meta['pid'],
            'view_type':'public',
            'knowledge_subject_id':'',
            'period_id':meta['pid'],
            'edition_id':press['edu_edition_id'],
        }
        parseBook(urlopen(url = url, data = urlencode(data).encode('utf-8')))

def parseBook(response):
    books = json.loads(response.read().decode('utf-8'))
    for book in books['list']:
        chapterUrl = "http://e.anoah.com/api/?q=json/ebag/resource/Book/getBookChaptersByChapterid&info={\"edu_book_id\":\"" + book['edu_book_id'] + "\",\"edu_chapter_id\":0}"
        parseChapter(urlopen(url = chapterUrl), book)

def parseChapter(response, book):
    chapters = json.loads(response.read().decode('utf-8'))
    chapterList = chapters['recordset']['chapterList']
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
        'param[m_category_id]':'1',#1: PPT, 4: Media, 39: doc
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
    for category in [1,4,11,38,39]:
        params['param[m_category_id]'] = category
        if category == 11:
            params['param[keyword]'] = 'mp4'
        else:
            params['param[keyword]'] = ''
        url = base_url + "?" + urlencode(params)
        parseData(urlopen(url), params, chapterList, book)

def parseData(response, params, chapterList, book):
    content = json.loads(response.read().decode('utf-8'))
    for data in content['data']:
        # book path
        if(book['tree_text']['grade'] is None):
            bookpath = [book['tree_text']['period'], book['tree_text']['subject'],book['tree_text']['term'], book['tree_text']['edition'], book['publish_info'], book['name']]
        else:
            bookpath = [book['tree_text']['period'], book['tree_text']['grade'], book['tree_text']['subject'],book['tree_text']['term'], book['tree_text']['edition'], book['publish_info'], book['name']]

        # chapter path
        # for binfo in data['binfo']:
        #     print(binfo['bookname'] + ": " + str(binfo['chapter_id']))
        chapterPath = getChapterPath(data['binfo'][0]['chapter_id'], chapterList)
        name = data['title']
        if(len(name) > 100):
            name = name[:100]
        savename = name + "_"+ str(data['pkid']) + "." + data['file_extension']
        download_path = (downloadPath + '/'.join(bookpath) + chapterPath + "/data/" + data['file_extension']).replace("//", "/")
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        exactName = download_path + "/" + savename
        print("downloading ---" + exactName)
        if not os.path.exists(exactName):
            try:
                urlretrieve(quote(data['down_path'], ":/"), exactName)
            except:
                print("error while downloading" + data['down_path'] + "\n" + str(params))
        # if(len(data['binfo']) > 1):
        #     # copy to other directory
        #     for binfo in data['binfo'][1:]:
        #         download_path = (downloadPath + '/'.join(bookpath) + getChapterPath(binfo['chapter_id']) + "/data/" + data['file_extension']).replace("//", "/")

    if(params['page'] * params['pagesize'] < content['total']):
        params['page'] = params['page'] + 1
        parseData(urlopen(url = base_url + "?" + urlencode(params)), params, chapterList, book)

def getChapterPath(id, chapterList):
    if(id == 0 or id == '0'):
        return ""
    chapters = list(filter(lambda x: x['edu_chapter_id'] == id, chapterList))
    if(len(chapters) > 0):
        chapter = chapters[0]
        if(chapter['parent_id'] == 0):
            return "/" + chapter['name']
        else:
            return getChapterPath(chapter['parent_id'], chapterList) + "/" + chapter['name']
    else:
        print("data not exists in any chapter")
        for chapter in chapterList:
            print(chapter['edu_chapter_id'] + ": " + chapter['name'])
        print(id)
        exit(0)

def parseGradeItem(glist):
    # % 4 =0,1,2,3 items ==> Grade
    index = 0
    pv = lambda x: parseValue(glist[x])
    gs = []
    while(index < len(glist)):
        g = Grade(period = pv(index+1), id = pv(index+2), name = pv(index+3))
        index += 4;
        gs.append(g)
    return gs

def parseSubjectItem(slist):
    # 0,1,2,3 ==> Subject
    index = 0
    pv = lambda x: parseValue(slist[x])
    ss = []
    while(index < len(slist)):
        s = Subject(grade = pv(index+1), id = pv(index+2), name = pv(index+3))
        index += 4;
        ss.append(s)
    return ss
    

def parseValue(str):
    value = str[str.index('=')+1:]
    return value[value.index("'") + 1: -2]

if __name__ == '__main__':
    start_url = 'http://e.anoah.com/index.php?r=book/select&level=1&style=radio&check=book&callback=onsetBookLcsuccess&school_id=158537&displaymode=1&bookids=1001546'
    parse(urlopen(start_url))
