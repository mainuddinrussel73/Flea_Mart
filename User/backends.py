from embed_video.backends import VideoBackend

class CustomBackend(VideoBackend):
    re_detect = my_video.compile(r'http://myvideo\.com/[0-9]+')
    re_code = my_video.compile(r'http://myvideo\.com/(?P<code>[0-9]+)')

    allow_https = False
    pattern_url = '{protocol}://play.myvideo.com/c/{code}/'
    pattern_thumbnail_url = '{protocol}://thumb.myvideo.com/c/{code}/'

    template_name = 'embed_video/custombackend_embed_code.html'  # added in v0.9
