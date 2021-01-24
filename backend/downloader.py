from __future__ import unicode_literals
import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        filename = d['filename']

def download_video(url):

        ydl_opts = {
        'format': '[filesize<40M]', # File size seems to need to be tweaked - look into it more
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }


    url = input("Please enter a youtube URL: ")
    #url = "https://www.youtube.com/watch?v=gTWz-zy3re4"

    #try:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    #except:
        #print("error: try a shorter video")
