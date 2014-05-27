from login_doubanfm import *
from pprint import pprint
from bs4 import BeautifulSoup
import time
import re

def get_cookie():
    urlfm = 'http://douban.fm/mine#!type=liked'
    
    header = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0)\
            Gecko/20100101 Firefox/29.0",
        'Connection':'keep-alive'
    }
    req = request.Request(urlfm, headers=header)
    response = request.urlopen(req)
    for cookie in cj:
        if cookie.name == 'bid':
           bid = cookie.value
        if cookie.name == 'ck':
           ck = cookie.value.strip("\"")
    return ck, bid
    
def getlist():
    ck, bid = get_cookie()
    window_SP = '::'
    spbid = request.quote(window_SP+bid.strip("\""))
    formaturl = "http://douban.fm/j/play_record?ck=%s&spbid=%s&type=liked&start=%d"
    song_sum = 0
    song_info_dir = {}
    pat = re.compile("(\d+)")
    page = 0
    while True:
        value = (ck, spbid, page*15)
        url = formaturl % value
        #print(url)
        req = request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0')
        req.add_header('Referer','http://douban.fm/mine?type=liked')
        context = json.loads(request.urlopen(req).read().decode('utf-8'))
        songs = context['songs']
        per_page_songcnt = len(songs)
        if per_page_songcnt != 0:
            print("第%d页列表得到%d首歌" % (page+1, per_page_songcnt))
            page += 1
        else:
            break
        song_sum += per_page_songcnt
        for song in songs:
            subject_id = pat.search(song['path']).group(1)
            song_info_dir[song['id'] ] = (subject_id, song['title'])
    print("红心歌曲列表共%d页，共得到%d首歌的信息" % (page, song_sum))
    return song_sum, song_info_dir

def test():
    getlist()

if __name__ == "__main__": 
     test()
