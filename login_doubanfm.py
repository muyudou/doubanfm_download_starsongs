from urllib import request, parse, error
from http import cookiejar
import json
import os
import platform

#设置cookie自动管理
cj = cookiejar.CookieJar()
cookieSupport = request.HTTPCookieProcessor(cj)
opener = request.build_opener(cookieSupport, request.HTTPHandler)
request.install_opener(opener)

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0)\
         Gecko/20100101 Firefox/29.0",
     'Host':'douban.fm'
    }

#判断运行平台
sysstr = platform.system()
if sysstr == 'Windows':
    download_path = '.\\starsongs\\'
elif sysstr == 'Linux':
    download_path='./starsongs/'

#请求验证码图片id和获得验证码图片不需要请求头，可以直接获得
def getdata():
    data = {
	'source':'radio'
    }
    user_name = input("请输入豆瓣账户用户名: ")
    user_pswd = input("请输入密码: ")
    data['alias'] = user_name
    data['form_password'] = user_pswd

    captcha_id_url = 'http://douban.fm/j/new_captcha'
    captcha_id = json.loads(request.urlopen(captcha_id_url).read().decode('utf-8'))
    data['captcha_id'] = captcha_id

     #创建歌曲文件夹
    if os.path.exists(download_path) == False:
        os.mkdir(download_path)
    captcha_pic_url = "http://douban.fm/misc/captcha?size=m&id=%s" % captcha_id
    request.urlretrieve(captcha_pic_url, download_path+"captchapic.jpg")
    captcha = input("请输入验证码：")
    data['captcha_solution'] = captcha
    return data

def login():
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0)\
            Gecko/20100101 Firefox/29.0",
        'Host':'douban.fm',
        'Referer':'http://douban.fm/'
    }
    #登录网址
    login_url = 'http://douban.fm/j/login'
    data = parse.urlencode(getdata()).encode(encoding='utf-8')
    req = request.Request(login_url, data=data, headers=headers)
    response = request.urlopen(req)
    login_info = json.loads(response.read().decode('utf-8'))
    if login_info['r'] == 0:
        print("登录成功！")
    else:
        print("登录失败，失败原因：%s" % login_info['err_msg'])
        reply = input("是否继续登录？y:是，n:否")
        if reply == 'y':
            login()
        elif reply == 'n':
            return
        else:
            print("输入错误！")      

def test():
    login()

if __name__=='__main__':test()


