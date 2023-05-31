gst-launch-1.0 filesrc location=tvlogo.png ! pngdec ! alphacolor ! \
  videoconvert ! videobox border-alpha=0 alpha=1 top=-20 left=-10 ! \
  videomixer name=mix ! videoconvert ! pngenc ! \
filesink location=video_mix.png videotestsrc num-buffers=2 ! \
  video/x-raw, width=320, height=240 ! mix.
