import requests

def login(username, password):
    url = 'http://www.anoah.com/ebag/index.php'
    header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safiri/537.36'}
    data = {'username': username, 'password': password, 'rememberMe': '0'}
    r = requests.post(url, headers=header, data=data)
    for k,v in r.cookies.iteritems():
        print k," : ", v
if __name__ == '__main__':
    login('liangyaodeng', '111111')
