注意：代码平台是Ubuntu14.04 python版本是3.4,安装的额外的包是beautifulsoup4.3

在Linux下，如果安装了python3, bs4包也安装了，则可以下载源代码，在源代码目录下输入python3 doubanfm.py
即可运行，可以下载歌曲

在windows下，也是安装python3.4, bs4包，在GUI下，直接运行；或在cmd下运行python doubanfm.py,在命令行下需要将python安装目录写入系统环境变量中，具体请google或baidu。

1 输入用户名，密码，验证码实现豆瓣fm自动登录。

提示：因为豆瓣需要验证码，将验证码图片下载到当前目录的starsongs目录下，打开图片需要自己输入验证码，从而登录，本来想过用ocr等自动识别，自己用pyocr也试了试，可是木有识别成功，只好把图片下载下来，自己输入了。。。。

2 登录成功后即可下载自己红心列表中的歌曲，是豆瓣fm自己的源文件。路径是会在当前路径下创建一个starsongs文件夹，图片歌曲都会下载到这里。

以上是自己刚写出来的，也许会有地方不对，或写的不好，希望各位多多包涵，同时不足的提出来，我会修改的～～～

