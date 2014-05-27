from login_doubanfm import *
from get_star_list import getlist
from downsong import *
import threading

error_songs = []
mylock = threading.RLock()  #存放下载失败的歌曲

class downsong_thread(threading.Thread):
    def __init__(self, name, song_list):
        threading.Thread.__init__(self)
        self.name = name
        self.song_list = song_list

    def run(self):
        for song_info in self.song_list:
            song_sid, sub_id, song_name = song_info[0], song_info[1][0], song_info[1][1]
            sub_path = "http://music.douban.com/subject/%s" % sub_id
            song_ssid = get_song_ssid(song_sid, sub_path, song_name)
            if song_ssid != None:
                down_song(song_sid, song_ssid)
            else:
                mylock.acquire()
                print("导致歌曲%s下载失败！" % song_name)
                error_songs.append(song_name)
                mylock.release()

def doubanfm():
    login()
    song_sum, song_sid_dir = getlist()
    allsong_list = [(k, v) for (k, v) in song_sid_dir.items()]
    thread_num = int(song_sum / 30)+1  #这里写的每个线程下载30首歌，可以更改
    song_thread = [None]*thread_num
   
    for i in range(thread_num):
        if song_sum < 30:
            song_list = allsong_list[0 : song_sum]
        else:
            song_list = allsong_list[i*30:(i+1)*30]
        thread_name = "线程"+str(i+1)
        song_thread[i] = downsong_thread(thread_name, song_list) 
        try:       
            song_thread[i].start()
            print(thread_name+"开始启动...")
        except RuntimeError as e:
            print(thread_name+"创建错误: ", e) 
    #等待所有线程执行完成
    for i in range(thread_num):
        song_thread[i].join()

    err_song_cnt = len(error_songs)
    print("下载歌曲完毕！共成功下载%d首歌，失败%d首歌" % (song_sum - err_song_cnt, err_song_cnt))
    if err_song_cnt != 0:
        print("下载失败的歌曲如下:")
        for song in error_songs:
            print(song)
        print("您可以选择重新运行程序，或从其他地方下载这些歌曲～～～，暂不提供单个歌曲下载～")

if __name__ == "__main__": 
    doubanfm()
