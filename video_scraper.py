import time
# from selenium import webdriver
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from pathlib import Path
from requests import get
import requests
from bs4 import BeautifulSoup
from itertools import islice
import moviepy.editor as mymovie
import random


class VideoScraper:
    def __init__(self, execute_browser=True):
        self.baseurl = "https://www.pexels.com/search/videos/"
        self.keyword = "beautiful car"
        self.baseurl_args = "?orientation=portrait"
        self.songs_path = "songs"
        self.results_path = "results"
        self.url = self.baseurl + self.keyword + self.baseurl_args

        self.video_links = []
        self.object_path = None
        if execute_browser:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--lang=en")

            self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
            self.browser.maximize_window()

    def get_video_links_from_keyword(self, url: str = None) -> list:
        """get video links

        :param url:
        :return:
        """
        timeout = 30
        if url is None:
            url = self.url

        self.browser.get(url)
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//video/source")))
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        links = soup.find_all("source")
        for link in links:
            self.video_links.append(link["src"])

        self.object_path = Path(self.results_path, self.keyword)
        if not os.path.isdir(self.object_path):
            os.mkdir(self.object_path)

        with open(f'{Path(self.object_path, self.keyword)}.txt', 'w', newline='', encoding="utf-8") as f:
            for elem in self.video_links:
                f.write(f"{elem}\n")
        return self.video_links

    def set_keyword(self, keyword: str) -> None:
        self.keyword = keyword
        self.url = self.baseurl + self.keyword + self.baseurl_args

    def close(self) -> None:
        self.browser.close()

    def __get_folder_count(self, extensions: str = None) -> int:
        list_dir = os.listdir(self.songs_path)
        count = 0
        for file in list_dir:
            if extensions is not None:
                if file.endswith(extensions):  # eg: '.txt'
                    count += 1
            else:
                count += 1
        return count

    def download_video_series(self, video_links: list = None):
        if self.object_path is None:
            self.object_path = Path(self.results_path, self.keyword)

        if video_links is None:
            video_links = []
            with open(f'{Path(self.object_path, self.keyword)}.txt', 'r', encoding="utf-8") as f:
                video_links.append(f.read().split("\n"))

        self.amount_of_songs = self.__get_folder_count(".mp4")
        # if amount_of_songs <= 0:
        #    raise RuntimeError(f"no songs in '{self.songs_path}' found!")
        print(self.amount_of_songs)

        for link in video_links[0]:
            file_name = link.split("/")[-1].split("?")[0]
            print(link)
            print(file_name)
            print(f"Start to downloading video: {file_name}")
            # create response object
            r = requests.get(link, stream=True)
            # download started
            with open(Path(self.object_path, file_name), 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

            print(f"{file_name} downloaded!")
            exit()
            self.edit_video(file_name)

    def edit_video(self, file):
        # editing the video
        list = random.choice(range(1, self.amount_of_songs))
        clip = mymovie.VideoFileClip(file)
        clip_duration = clip.duration
        audioclip = mymovie.AudioFileClip(f"songs/audio{list}.mp3").set_duration(clip_duration)
        new_audioclip = mymovie.CompositeAudioClip([audioclip])
        finalclip = clip.set_audio(new_audioclip)
        # location = os.path.join("C:\\Users\\python\\Desktop\\videos", f"video{i}.mp4")
        finalclip.write_videofile(f"videos/vid{i}.mp4", fps=60)
        print("%s has been edited!\n" % file)

if __name__ == "__main__":
    vs = VideoScraper(False)
    #video_links = vs.get_video_links_from_keyword()
    # print(video_links)
    #vs.close()
    vs.download_video_series()

    # print(video_links)

    # download all videos
    # download_video_series(video_links)
