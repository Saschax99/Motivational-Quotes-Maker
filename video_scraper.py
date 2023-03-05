import time
# from selenium import webdriver
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from requests import get
import requests
from bs4 import BeautifulSoup
import moviepy.editor as mymovie
import random
import uuid

songs_path = "songs"
temp_path = "temp"
results_path = "results"

class OsTools:
    @staticmethod
    def get_folder_count(path, extensions: str = None) -> int:
        list_dir = os.listdir(path)
        count = 0
        for file in list_dir:
            if extensions is not None:
                if file.endswith(extensions):  # eg: '.txt'
                    count += 1
            else:
                count += 1
        return count

    @staticmethod
    def select_specific_object_from_folder(path, count) -> str:
        return os.listdir(path)[count]
    

class YoutubeShortsFetcher:
    def __init__(self):
        self.baseurl = "https://www.pexels.com/search/videos/"
        self.keyword = "natur"
        self.baseurl_args = "?orientation=portrait"
        self.url = self.baseurl + self.keyword + self.baseurl_args
        
        self.video_links = []

    def __establish_connection(self, url: str = None) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)
    
    def get_video_links_from_keyword(self, url: str = None) -> list:
        timeout = 30
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//video/source")))
        
        reached_page_end = False
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        while not reached_page_end:
            self.browser.find_element_by_xpath('//body').send_keys(Keys.END)   
            time.sleep(1.5)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                    reached_page_end = True
            else:
                last_height = new_height
    
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        links = soup.find_all("source") 
        for link in links:
            self.video_links.append(link.get("src"))

        if not os.path.isdir(temp_path):
            os.mkdir(temp_path)

        with open(f'{os.path.join(temp_path, self.keyword)}.txt', 'w', newline='', encoding="utf-8") as f:
            for elem in self.video_links:
                f.write(f"{elem}\n")
        return self.video_links

    def set_keyword(self, keyword: str) -> None:
        self.keyword = keyword
        self.url = self.baseurl + self.keyword + self.baseurl_args

    def close(self) -> None:
        self.browser.close()
    
    def download_video_series(self, video_links: list = None):
        if video_links is None:
            video_links = []
            video_links_path = os.path.join(temp_path, self.keyword)
            with open(f'{video_links_path}.txt', 'r', encoding="utf-8") as f:
                video_links.append(f.read().split("\n"))

        self.amount_of_songs = OsTools.get_folder_count(songs_path, ".mp3")
        if self.amount_of_songs <= 0:
            raise RuntimeError(f"no songs in '{songs_path}' found!")
        print(self.amount_of_songs)

        for index, link in enumerate(video_links[0]):
            if link is None:
                continue
            
            self.file_name = link.split("/")[-1].split("?")[0]
            print(link)
            print(self.file_name)
            print(f"Start to downloading video: {self.file_name}")
            # create response object
            r = requests.get(link, stream=True)
            # download started
            self.file_path = os.path.join(temp_path, f"{uuid.uuid1().hex}.mp4")
            with open(self.file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

            print(f"{self.file_name} downloaded!")
            self.edit_video()
            
            # removing temp file and row in .txt file
            os.remove(self.file_path)
            
            with open(f"{video_links_path}.txt", 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                f.writelines(line for i, line in enumerate(lines) if i != 0)
                f.truncate()
                
            print(f"{self.file_path} removed!")

    def edit_video(self):
        ran_int = random.choice(range(0, self.amount_of_songs))
        music_clip =OsTools.select_specific_object_from_folder(songs_path, ran_int)
        print(self.file_path)
        print(music_clip)
        
        
        video = mymovie.VideoFileClip(self.file_path)
        video_duration = video.duration
        audio = mymovie.AudioFileClip(os.path.join(songs_path, music_clip)).set_duration(video_duration).audio_fadeout(.33)
        #new_audioclip = mymovie.CompositeAudioClip([audioclip])
        video_with_music = video.set_audio(audio)
        final_path = os.path.join(results_path, f"{uuid.uuid1().hex}.mp4")
        video_with_music.write_videofile(f"{final_path}", fps=60, codec="libx264")
        video.close()
        
        print(f"{final_path} has been edited!")
        
class YoutubeShortsUploader:
    def __init__(self) -> None:
        self.url = "https://studio.youtube.com"

        self.__establish_connection()

    def __establish_connection(self, url: str = None) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("user-data-dir=C:\\Users\dolsa\\AppData\\Local\\Google\\Chrome\\User Data")
        self.options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)
        
    def upload_video_series(self):
        if OsTools.get_folder_count(results_path) <= 0:
            raise RuntimeError(f"no videos in '{results_path}' found!")
            
        time.sleep(3)
        upload_button = self.browser.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(5)

        file_input = self.browser.find_element(By.XPATH, '//*[@id="content"]/input')
        simp_path = 'videos/vid{}.mp4'.format(str(i+1))
        abs_path = os.path.abspath(simp_path)
        
        file_input.send_keys(abs_path)

        time.sleep(7)

        next_button = self.browser.find_element(By.XPATH, '//*[@id="next-button"]')
        for i in range(3):
            next_button.click()
            time.sleep(5)

        done_button = self.browser.find_element(By.XPATH, '//*[@id="done-button"]')
        done_button.click()
        time.sleep(5)    
    
    
if __name__ == "__main__":
    vsf = YoutubeShortsFetcher()
    #video_links = vsf.get_video_links_from_keyword()
    #print(video_links)
    vsf.download_video_series()
    #vsf.__establish_connection()
    #vs.close()

    # print(video_links)

    # download all videos
    # download_video_series(video_links)
