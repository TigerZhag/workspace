import requests

header = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safiri/537.36',
    'referer' : 'http://e.anoah.com/index.php?r=book/select&level=1&style=radio&check=book&callback=onsetBookLcsuccess&school_id=158537&displaymode=1&bookids=1001546',
}
cookies = {
    'ebag_login_info': '14c4b06b824ec593%25C3%25B7%25C2%258B%25C3%25BA%25C2%2591%25C3%25AF%25C2%258E%25C3%2593e%25C3%258Fh%25C3%25BF%25C2%2586%25C4%259B%25C2%25BA%25C3%25A4u%25C3%2589e%25C4%2598%25C2%25B3%25C3%2593e%25C4%2597%25C2%25B0239362517f538b295f4dcc3b5aa765d6%25C3%259B%25C2%25AA%25C3%2595%25C2%25A4%25C3%25A0%25C2%25AF%25C2%258C%255B%25C3%25AB%25C2%25BA%25C2%25B7%25C2%25861d8327deb882cf99',
    'ebag_username': 'liangyaodeng',
    'ebag_password': '111111',
    'ebag_remember': '0',
    'ebag_proxy': '0',
    'Hm_lvt_9f5a18df6da91ec7f0ee7b1d6fe05304': '1499302707,1499321050',
    'Hm_lpvt_9f5a18df6da91ec7f0ee7b1d6fe05304': '1499321050'
}

def preLogin():
    url = 'http://www.anoah.com/ebag/user/index.html'
    r = requests.get(url, headers = header)
    for k,v in r.cookies.iteritems():
        cookies[k] = v

def login(username, password):
    url = 'http://www.anoah.com/ebag/index.php'
    header['referer'] = url
    data = {'username': username, 'password': password, 'rememberMe': '0'}
    r = requests.post(url, headers = header, data = data, cookies=cookies)
    for k,v in r.cookies.iteritems():
        cookies[k] = v

def homepage():
    url = 'http://e.anoah.com/ebag/index.php?r=course#entry/{"bookId":33500,"isHistory":0,"chapterId":0,"courseHourId":0,"sectionTypeId":0}'
    header['referer'] = url
    print(url)
    r = requests.get(url, headers = header, cookies = cookies)
    for k,v in r.cookies.iteritems():
        cookies[k] = v
    print(r.content)

def getBook():
    url = 'http://e.anoah.com/index.php?r=book/select/getBook'
    data = {
        'page':1,
        'school_id':'',
        'user_id':'',
        'grade_id':'',
        'subject_id':2,
        'period_id':2,
        'view_type':'public',
        'knowledge_subject_id':'',
        'period_id':2,
        'edition_id':666,
    }
    r = requests.post(url, headers = header, data = data, cookies = cookies)
    print(r.content)

def getBaseInfo():
    url = 'http://e.anoah.com/index.php?r=book/select&level=1&style=radio&check=book&callback=onsetBookLcsuccess&school_id=158537&displaymode=1&bookids=1001546'
    header['referer'] = url
    data = {
        'r': 'book/select',
        'level': 1,
        'style': 'radio',
        'check': 'book',
        'callback': 'onsetBookLcsuccess',
        'school_id': 158537,
        'displaymode': 1,
        'bookids': 1001546,
    }
    r = requests.get(url, headers = header, cookies = cookies, params = data)
    print(r.content)

if __name__ == '__main__':
    # preLogin() 
    # login('liangyaodeng', '111111')
    # homepage()
    getBaseInfo()
    # getBook()
