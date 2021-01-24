import ffmpeg

def render(videofilename, bpm):

    looping = ffmpeg.input("cat.mp4", stream_loop = -1) # Import tom as a looping stream, tom is 426x240
    looping = ffmpeg.filter(looping, "colorkey", color="0x2bd71c", similarity=0.3, blend=0) # This green I got myself from the tom video

    stream = ffmpeg.input(filename, ss=90, t=25) # Get start at 20s in and make the clip 20s
    video = stream.video
    audio = stream.audio

    looping = ffmpeg.filter(looping, "setpts", "{}*PTS".format(118 /bpm))
    video = ffmpeg.filter(video, 'scale', 1280,720) # Resize to 720p
    video = ffmpeg.overlay(stream, looping, shortest=1, y = "0")
    stream = ffmpeg.output(video, audio, './output.mp4').overwrite_output()
    stream.run()
