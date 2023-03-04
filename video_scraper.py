import time
# from selenium import webdriver
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
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
        self.temp_path = "temp"
        self.results_path = "results"
        self.url = self.baseurl + self.keyword + self.baseurl_args
        self.scroll_amount = 100
        
        self.video_links = []
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
        for i in range(self.scroll_amount):  # scroll to bottom to load more objects
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
    
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        links = soup.find_all("source")
        for link in links:
            self.video_links.append(link["src"])

        if not os.path.isdir(self.temp_path):
            os.mkdir(self.temp_path)

        with open(f'{os.path.join(self.temp_path, self.keyword)}.txt', 'w', newline='', encoding="utf-8") as f:
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

    def __select_object_from_folder(self, path, count) -> str:
        return os.listdir(path)[count]
    
    def download_video_series(self, video_links: list = None):
        if video_links is None:
            video_links = []
            with open(f'{os.path.join(self.temp_path, self.keyword)}.txt', 'r', encoding="utf-8") as f:
                video_links.append(f.read().split("\n"))

        self.amount_of_songs = self.__get_folder_count(".mp3")
        if self.amount_of_songs <= 0:
            raise RuntimeError(f"no songs in '{self.songs_path}' found!")
        print(self.amount_of_songs)

        for link in video_links[0]:
            self.file_name = link.split("/")[-1].split("?")[0]
            print(link)
            print(self.file_name)
            print(f"Start to downloading video: {self.file_name}")
            # create response object
            r = requests.get(link, stream=True)
            # download started
            self.file_path = os.path.join(self.temp_path, self.file_name)
            with open(self.file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

            print(f"{self.file_name} downloaded!")
            self.edit_video()
            exit()

    def edit_video(self):
        ran_int = random.choice(range(0, self.amount_of_songs))
        music_clip = self.__select_object_from_folder(self.songs_path, ran_int)
        print(self.file_path)
        print(music_clip)
        clip = mymovie.VideoFileClip(self.file_path)
        clip_duration = clip.duration
        audioclip = mymovie.AudioFileClip(os.path.join(self.songs_path, music_clip)).set_duration(clip_duration)
        new_audioclip = mymovie.CompositeAudioClip([audioclip])
        finalclip = clip.set_audio(new_audioclip)
        final_path = os.path.join(self.results_path, self.file_name)
        finalclip.write_videofile(f"{final_path}.mp4", fps=60)
        print(f"{self.file_path} has been edited!")
        exit()

if __name__ == "__main__":
    vs = VideoScraper(False)
    #video_links = vs.get_video_links_from_keyword()
    # print(video_links)
    #vs.close()
    vs.download_video_series()

    # print(video_links)

    # download all videos
    # download_video_series(video_links)
