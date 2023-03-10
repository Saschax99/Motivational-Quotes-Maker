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
from config import USER, PASSWORD

SONGS_PATH = "songs"
TEMP_PATH = "temp"
RESULTS_PATH = "results"
TIMEOUT = 30

class OsTools:
    @staticmethod
    def get_folder_count(path: str, extensions: str = None) -> int:
        """Get the number of files in a folder with optional extensions."""
        list_dir = os.listdir(path)
        if extensions:
            count = sum(1 for file in list_dir if file.endswith(extensions))
        else:
            count = len(list_dir)
        return count

    @staticmethod
    def select_specific_object_from_folder(path: str, index: int) -> str:
        """Select a specific file from a folder by its index."""
        return os.listdir(path)[index]
        
class YoutubeShortsFetcher:
    """Class for fetching YouTube shorts videos."""
    
    def __init__(self):
        self.baseurl = "https://www.pexels.com/search/videos/"
        self.keyword = "natur"
        self.baseurl_args = "?orientation=portrait"
        self.url = self.baseurl + self.keyword + self.baseurl_args
        self.timeout = TIMEOUT
        self.video_links = []

    def get_browser(self, url: str = None) -> None:
        """Establish a connection to the website using a ChromeDriver."""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)
    
    def get_video_links_from_keyword(self, url: str = None) -> list:
        """Get the links of videos from a search keyword."""
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, "//video/source")))
        
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
        #links = soup.find_all("source") 
        #for link in links:
        #    self.video_links.append(link.get("src"))
        self.video_links = [tag.get("src") for tag in soup.select("source")]

        if not os.path.exists(TEMP_PATH):
            os.makedirs(TEMP_PATH)

        with open(f'{os.path.join(TEMP_PATH, self.keyword)}.txt', 'w', newline='', encoding="utf-8") as f:
            for elem in self.video_links:
                f.write(f"{elem}\n")
        return self.video_links

    def set_keyword(self, keyword: str) -> None:
        self.keyword = keyword
        self.url = self.baseurl + self.keyword + self.baseurl_args

    def close(self) -> None:
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
        
class YoutubeShortsUploader:
    def __init__(self) -> None:
        self.url = "https://studio.youtube.com"
        self.user = USER
        self.password = PASSWORD
        self.timeout = 15
        self.title = "Nature #travel #nature #shorts"
        self.description = """
#shortsclip #gallery #artlife #art #youtube #youtuber 
#subscribe #shortsanity #shortsbeta #shortsfunny
#shortsart #shortscomplitition #instagramyoutube
#youtuberlikes #youtubevide #shortstiktok
#shortsfortnite #shortsbts #shortsbgmi
#shortsassam #shortsads #youtubegrowth
#youtubeusers #instavideo
Music by Bass Rebels"""

    def get_browser(self, url: str = None):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")
        self.options.add_argument("--log-level=3")
        #self.options.add_argument("user-data-dir=C:\\Users\dolsa\\AppData\\Local\\Google\\Chrome\\User Data")
        #self.options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)
        
    def upload_video_series(self, path: str = None, login=True) -> None:
        if path is None:
            path = RESULTS_PATH
        if OsTools.get_folder_count(path) <= 0:
            raise RuntimeError(f"no videos in '{path}' found!")
            
        if login:
            WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="email"]')))
            input_email = self.browser.find_element(By.XPATH, '//input[@type="email"]')
            input_email.send_keys(self.user)
            
            self.browser.find_element(By.XPATH, '(//button[@jsname="LgbsSe"]//span[@jsname="V67aGc"])[2]').click()
            
            WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]')))
            input_pass = self.browser.find_element(By.XPATH, '//input[@type="password"]')
            input_pass.send_keys(self.password)
            
            self.browser.find_element(By.XPATH, '(//button[@jsname="LgbsSe"]//span[@jsname="V67aGc"])[2]').click()
        
        while True:
            try:
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="upload-icon"]')))
                upload_button = self.browser.find_element(By.XPATH, '//*[@id="upload-icon"]')
                upload_button.click()
                               
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/input')))
                file_input = self.browser.find_element(By.XPATH, '//*[@id="content"]/input')
                selected_file = OsTools.select_specific_object_from_folder(RESULTS_PATH, 0)
                file_path = os.path.join(RESULTS_PATH, selected_file)
                abs_path = os.path.abspath(file_path)

                file_input.send_keys(abs_path)
                
                WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '(//div[@id="textbox"])[1]')))
                title = self.browser.find_element(By.XPATH, '(//div[@id="textbox"])[1]')
                title.clear()
                title.send_keys(self.title)
                
                description = self.browser.find_element(By.XPATH, '(//div[@id="textbox"])[2]')
                description.send_keys(self.description)
                
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="next-button"]')))
                self.browser.find_element(By.XPATH, '//*[@id="next-button"]').click()
                self.browser.find_element(By.XPATH, '(//div[@id="radioLabel"]/ytcp-ve[@class="style-scope ytkc-made-for-kids-select"])[2]').click()
                self.browser.find_element(By.XPATH, '//*[@id="next-button"]').click()
                self.browser.find_element(By.XPATH, '//*[@id="next-button"]').click()
                self.browser.find_element(By.XPATH, '//*[@id="next-button"]').click()
                
                self.browser.find_element(By.XPATH, '(//div[@class="style-scope tp-yt-paper-radio-button" and @id="radioLabel"])[4]').click()
                WebDriverWait(self.browser, self.timeout).until(EC.invisibility_of_element((By.XPATH, '//*[@id="done-button" and @disabled=""]')))
                try:
                    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//tp-yt-iron-icon[@class="error-icon style-scope ytcp-uploads-dialog"]')))
                    print("limit reached")
                    exit(0)
                except:
                    self.browser.find_element(By.XPATH, '//*[@id="done-button"]').click()
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//h1[@id="dialog-title"]')))
                self.browser.find_element(By.XPATH, '//ytcp-button[@id="close-button"]').click()
                
                print(f"removing {file_path}")
                os.remove(file_path)
                
            except KeyboardInterrupt:   
                exit()
    
if __name__ == "__main__":
    ytFetcher = YoutubeShortsFetcher()
    #video_links = ytFetcher.get_video_links_from_keyword()
    #print(video_links)
    #ytFetcher.get_browser()
    #ytFetcher.download_video_series()
    #ytFetcher.close()



    ytUploader = YoutubeShortsUploader()
    ytUploader.get_browser()
    ytUploader.upload_video_series(login=True)
    
    
    # print(video_links)

    # download all videos
    # download_video_series(video_links)
