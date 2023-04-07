'''
USED FOR SHORTS FROM PEXELS.COM
DOWNLOADING FROM PEXELS.COM OVERLAY IT WITH MUSIC AND SAVE VIDEOS IN RESULT PATH
AT THE MOMENT UNSUSED MIGHT DELETE LATER
'''

import time
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import requests
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip, AudioFileClip
import random
import uuid
from config import SONGS_PATH, TEMP_PATH, RESULTS_PATH, TIMEOUT
from ..utils.omp_tools import OsTools
        
class ShortsFetcher:
    """Class for fetching shorts videos."""
    
    def __init__(self):
        self.baseurl = "https://www.pexels.com/search/videos/"
        self.keyword = "nature"
        self.baseurl_args = "?orientation=portrait"
        self.url = self.baseurl + self.keyword + self.baseurl_args
        self.timeout = TIMEOUT
        self.video_links = []
        
        for path in [SONGS_PATH, TEMP_PATH, RESULTS_PATH]:
            if not os.path.exists(path):
                os.makedirs(path)

    def get_browser(self, url: str = None) -> None:
        """Establish a connection to the website using a ChromeDriver."""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)
    
    def get_video_links_from_keyword(self) -> list:
        """Get the links of videos from a search keyword."""
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, "//video/source")))
        
        reached_page_end = False
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        print("starting to fetch video links..")
        try:
            while not reached_page_end:
                self.browser.find_element(By.XPATH, '//body').send_keys(Keys.END)
                time.sleep(2.5)
                new_height = self.browser.execute_script("return document.body.scrollHeight")
                if last_height == new_height:
                        reached_page_end = True
                else:
                    last_height = new_height
        except KeyboardInterrupt:
          print("stopping fetching video links..")
    
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        #links = soup.find_all("source") 
        #for link in links:
        #    self.video_links.append(link.get("src"))
        self.video_links = [tag.get("src") for tag in soup.select("source")]

        file_path = f"{os.path.join(TEMP_PATH, self.keyword)}.txt"
        with open(file_path, 'w', newline='', encoding="utf-8") as f:
            for elem in self.video_links:
                f.write(f"{elem}\n")
        print(f"wrote video_links into {file_path}")
        return self.video_links

    def set_keyword(self, keyword: str) -> None:
        self.keyword = keyword
        self.url = self.baseurl + self.keyword + self.baseurl_args
        print(f"keyword with url {self.url} was set")
    
    def close(self) -> None:
        print("closing browser..")
        self.browser.close()
        
    @staticmethod
    def get_video_length(file_path: str) -> int:
        video = VideoFileClip(file_path)
        # Get the duration of the video in seconds
        duration = video.duration
        # Close the video file
        video.close()
        return duration
    
    def download_video_series(self, video_links: list = None) -> None:
        if video_links is None:
            video_links = []
            video_links_path = os.path.join(TEMP_PATH, f"{self.keyword}.txt")
            with open(video_links_path, 'r', encoding="utf-8") as f:
                video_links.append(f.read().split("\n"))
        print(f"fetched video links in {video_links_path}")
        print(video_links)

        self.amount_of_songs = OsTools.get_folder_count(SONGS_PATH, ".mp3")
        if self.amount_of_songs <= 0:
            raise RuntimeError(f"no songs in '{SONGS_PATH}' found!")
        print(self.amount_of_songs)

        for link in video_links[0]:
            if link is None:
                continue
            
            self.file_name = link.split("/")[-1].split("?")[0]
            print(link)
            print(self.file_name)
            print(f"Start to downloading video: {self.file_name}")
            
            # create response object
            # r = requests.get(link, stream=True)
            # # download started
            self.file_path = os.path.join(TEMP_PATH, f"{uuid.uuid1().hex}.mp4")
            # with open(self.file_path, 'wb') as f:
            #     for chunk in r.iter_content(chunk_size=1024 * 1024):
            #         if chunk:
            #             f.write(chunk)
            with requests.get(link, stream=True) as r:
                r.raise_for_status()
                with open(self.file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

            print(f"{self.file_name} downloaded!")
            
            video_length = self.get_video_length(self.file_path)
            if video_length >= 7.0 and video_length < 60.0:
                self.edit_video()
            else:
                print(f"video length to short going to delete it - {video_length}s")
 
            
            # removing temp file and row in .txt file
            os.remove(self.file_path)
            
            with open(video_links_path, 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                f.writelines(line for i, line in enumerate(lines) if i != 0)
                f.truncate()
                
            print(f"{self.file_path} removed!")

    def edit_video(self):
        ran_int = random.choice(range(0, self.amount_of_songs))
        music_clip =OsTools.select_specific_object_from_folder(SONGS_PATH, ran_int)
        print(self.file_path)
        print(music_clip)
        
        with VideoFileClip(self.file_path) as video:
            video_duration = video.duration
            with AudioFileClip(os.path.join(SONGS_PATH, music_clip)).set_duration(video_duration).audio_fadeout(.33) as audio:
                video_with_music = video.set_audio(audio)
                final_path = os.path.join(RESULTS_PATH, f"{uuid.uuid1().hex}.mp4")
                video_with_music.write_videofile(f"{final_path}", fps=60, codec="libx264")
        # video = VideoFileClip(self.file_path)
        # video_duration = video.duration
        # audio = AudioFileClip(os.path.join(SONGS_PATH, music_clip)).set_duration(video_duration).audio_fadeout(.33)
        # video_with_music = video.set_audio(audio)
        # final_path = os.path.join(RESULTS_PATH, f"{uuid.uuid1().hex}.mp4")
        # video_with_music.write_videofile(f"{final_path}", fps=60, codec="libx264")
        # video.close()
        
        print(f"{final_path} has been edited!")
            
if __name__ == "__main__":
    ytFetcher = ShortsFetcher()
    print()
