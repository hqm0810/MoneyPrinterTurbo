from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from google.auth.transport.requests import Request
from google.auth.credentials import AnonymousCredentials
import requests
import yt_dlp
import os
import httplib2


# YouTube API 配置
API_KEY = "AIzaSyBjJYSCLBmfpobS8sm8Ed7Lx2ceyMpTUTw"  # 替换为你的 API 密钥
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# os.environ["http_proxy"] = "http://localhost:7890"
# os.environ["https_proxy"] = "http://localhost:7890"





# 使用 YouTube Data API 搜索视频
def search_youtube(keyword, max_results=5):
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY, 
    #                 http=http)
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "id,snippet",
        "q": keyword,
        "type": "video",
        "maxResults": 5,
        "key": API_KEY
    }
    response = requests.get(url, params=params, proxies=proxies)
    response_data = response.json()

    videos = []
    for item in response_data["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"title": title, "url": url})

    return videos

def get_video_info(video_url):
    """
    使用 yt-dlp 提取视频信息，包括时长。
    
    :param video_url: 视频的 URL
    :return: 包含标题、时长和其他信息的字典
    """
    # yt-dlp 配置
    ydl_opts = {
        "quiet": True,  # 不输出日志
        "skip_download": True,  # 只获取元数据，不下载视频
    }

    ydl_opts["proxy"] = "http://127.0.0.1:7890"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 提取视频信息
        info = ydl.extract_info(video_url, download=False)
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),  # 时长（以秒为单位）
            "url": info.get("webpage_url"),
        }

def youtube_video_downloader(video_url, video_path):

    ydl_opts = {
        "quiet": True,  # 不输出日志
        "skip_download": True,  # 先提取信息
        "proxy": "http://127.0.0.1:7890"

    }

    # 提取视频格式信息
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get("formats", [])


    ydl_opts = {
        "outtmpl": video_path,  # 文件保存路径
        "format": "bestvideo+bestaudio/best",  # 下载最佳质量的视频和音频
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"  # 转换为 mp4 格式
            }
        ],
        "proxy": "http://127.0.0.1:7890"
    }



    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# def search_youtube(keyword, max_results=5):
#     proxy_info = httplib2.ProxyInfo(
#         httplib2.socks.PROXY_TYPE_HTTP,
#         proxy_host="http://localhost",  # 代理地址
#         proxy_port=7890,            # 代理端口
#     )

#     # 使用代理构建 HTTP 对象
#     http = httplib2.Http(proxy_info=proxy_info)

#     # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
#     youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY, 
#                     http=http)
    
#     search_response = youtube.search().list(
#         q=keyword,  # 搜索关键词
#         part="id,snippet",
#         maxResults=max_results,
#         type="video"  # 只搜索视频
#     ).execute()

#     videos = []
#     for item in search_response["items"]:
#         video_id = item["id"]["videoId"]
#         title = item["snippet"]["title"]
#         url = f"https://www.youtube.com/watch?v={video_id}"
#         videos.append({"title": title, "url": url})

#     return videos

http = "http://127.0.0.1:7890"
https = "http://127.0.0.1:7890"

if __name__ == '__main__':
    
    # res = search_youtube('skiing', 2)
    # print(res)

    # get_video_info('https://www.youtube.com/shorts/ozFfDbF4ZFQ')
    # youtube_video_downloader('https://www.youtube.com/shorts/ozFfDbF4ZFQ', 'test')

    from app.services.material import download_videos

    download_videos(
        "test123", ["Money Exchange Medium"], audio_duration=100, source="youtube"
    ) 
    pass