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
    song_sid_info_file = open(download_path+"/sid_info", 'w')
    for i in range(13):
        value = (ck, spbid, i*15)
        url = formaturl % value
        #print(url)
        req = request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0')
        req.add_header('Referer','http://douban.fm/mine?type=liked')
        context = json.loads(request.urlopen(req).read().decode('utf-8'))
        songs = context['songs']
        print("第%d页列表得到%d首歌" % (i+1, len(songs)))
        song_sum += len(songs)
        for song in songs:
            subject_id = pat.search(song['path']).group(1)
            song_info_dir[song['id'] ] = (subject_id, song['title'])
        song_sid_info_file.write(str(song_info_dir))
    print("总共得到%d首歌的信息,这个可能跟豆瓣统计红心歌曲总数不一致，可能是豆瓣的一个bug...因为你的列表确实是只有这么多歌曲了..." % song_sum)
    song_sid_info_file.close()
    return song_sum, song_info_dir

def main():
    getlist()

if __name__ == "__main__": 
     main()
