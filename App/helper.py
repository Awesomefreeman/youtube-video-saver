import logging
import os
import youtube_dl

logger = logging.getLogger("YoutubeVideoSaver")
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def downloader(download_folder, playlist_links: list):
    youtube_options = {
        "ignoreerrors": True,
        "logger": logger,
        "nooverwrites": True,
        "format": "bestvideo+bestaudio",
        "outtmpl": f"{os.getcwd()}/{download_folder}/%(title)s.%(ext)s",
        "simulate": True,
        'cachedir': False,
    }
    yt = youtube_dl.YoutubeDL(youtube_options)
    yt.download(playlist_links)
