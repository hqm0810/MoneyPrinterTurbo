import yt_dlp


def get_youtube_info(video_url, proxy=None):
    
    ydl_opts = {
        "quiet": True,  # 不输出日志
        "skip_download": True,  # 只获取元数据，不下载视频
    }

    if proxy is not None:   ydl_opts["proxy"] = proxy

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 提取视频信息
        info = ydl.extract_info(video_url, download=False)

        return info

    return None