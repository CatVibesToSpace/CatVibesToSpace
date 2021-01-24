
from __future__ import unicode_literals
import youtube_dl
import ffmpeg
import bpm_detection

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

        # ffmpeg -stream_loop -1 -i bg.mp4 -i main.mp4 -filter_complex "[0][1]overlay=shortest=1[v]" -map "[v]" -map 1:a -c:a copy output.mp4

        looping = ffmpeg.input("cat.mp4",stream_loop = -1,) # Import tom as a looping stream, tom is 426x240
        looping = ffmpeg.filter(looping, "colorkey", color="0x2bd71c", similarity=0.5, blend=0.1) # This green I got myself from the tom video
        import subprocess

        def get_length(filename):
            result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                     "format=duration", "-of",
                                     "default=noprint_wrappers=1:nokey=1", filename],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            return float(result.stdout)
        duration = get_length(filename)
        if duration <50 and duration > 30:
            start = duration-30
            length = 25
        elif duration < 30:
            start = 2
            length = duration - 4
        else:
            start = (duration/2)-15
            length = 30
        stream = ffmpeg.input(filename, ss=start, t=length) # Get start at 20s in and make the clip 20s
        video = stream.video
        audio = stream.audio
        print("Generating waveform!!!")
        bpm = bpm_detection.generate_wav_bpm(filename)
        looping = ffmpeg.filter(looping, "setpts", "{}*PTS".format(118 /bpm))
        print("BPM = ",bpm)
        video = ffmpeg.filter(video, 'scale', 1280,720) # Resize to 720p
        video = ffmpeg.overlay(stream, looping, shortest=1, y = "0")
        stream = ffmpeg.output(video, audio, '../test.mp4').overwrite_output()
        stream.run()


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
