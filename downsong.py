from bs4 import BeautifulSoup
import os
from login_doubanfm import *

def valid_name(filename):
    return filename.encode().translate(None, b'?~/\\*-()').decode()

#根据专辑页面得到歌曲的ssid
def get_song_ssid(sid, sub_path, song_name):
    try:
        data = request.urlopen(sub_path).read().decode('utf-8')
        soup = BeautifulSoup(data)
        tag = soup.find('li', class_="song-item", id=sid)
        ssid = tag['data-ssid']
    except Exception as e:
        print("获得歌曲%s的ssid发生异常，" % song_name, e)
        return None
    else:
        return tag['data-ssid']

def down_song(sid, ssid):
    starturl = 'http://douban.fm/?start=%s' % (str(sid)+'g'+ssid+'g')
    header = headers
    header['Referer'] = 'http://www.douban.com/'
    req = request.Request(starturl, headers = header)
    request.urlopen(req)    

    playlisturl= 'http://douban.fm/j/mine/playlist?type=n&sid=&pt=0.0&channel=0&from=mainsite'
    playlistreq = request.Request(playlisturl)
    playlistreq.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0')
    playlistreq.add_header('Referer',starturl)
    playlistreq.add_header('Host',"douban.fm")

    response = request.urlopen(playlistreq)
    playlist = json.loads(response.read().decode('utf-8'))
    song = playlist['song'][0]
    song_singer = valid_name(song['artist'])
    songname = "%s(%s)" % (valid_name(song['title']), song_singer)  
    songpath = download_path+songname+'.mp3'
    if sid == song['sid']:
        if os.path.exists(songpath):
	        print("歌曲已经存在")
        else:
            print(("下载歌曲：%s\t歌手是:%s\tloading...")%(valid_name(song['title']),
			song_singer)) 
            try:
                request.urlretrieve(song['url'], songpath)
            except error.URLError as e:
                print("下载%s歌曲发生异常，下载失败！" % songname, e)
            else:
                print("%s下载完成" % songname)
    else:
        print("获得的列表错误！")
 
def test():
    sid = '1393408'
    sub_id = '2775668'
    sub_path = "http://music.douban.com/subject/%s" % sub_id
    ssid = get_song_ssid(sid, sub_path)
    down_song(sid, ssid)    

if __name__ == "__main__": 
     test()
