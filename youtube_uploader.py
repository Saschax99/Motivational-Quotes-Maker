import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from config import RESULTS_PATH
from os_tools import OsTools

class YoutubeShortsUploader:
    def __init__(self, amount, user, password, remove_files) -> None:
        self.amount = amount
        self.remove_files = remove_files
        self.url = "https://studio.youtube.com"
        self.user = user
        self.password = password
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

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)
        
    def set_title(self, title):
        self.title = title
    
    def set_description(self, description):
        self.description = description
    
    def upload_video_series(self, path: str = None) -> None:
        if path is None:
            path = RESULTS_PATH
        if OsTools.get_folder_count(path) <= 0:
            raise RuntimeError(f"no videos in '{path}' found!")
            
        WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="email"]')))
        input_email = self.browser.find_element(By.XPATH, '//input[@type="email"]')
        input_email.send_keys(self.user)
        
        self.browser.find_element(By.XPATH, '(//button[@jsname="LgbsSe"]//span[@jsname="V67aGc"])[2]').click()
        
        WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]')))
        input_pass = self.browser.find_element(By.XPATH, '//input[@type="password"]')
        input_pass.send_keys(self.password)
        
        self.browser.find_element(By.XPATH, '(//button[@jsname="LgbsSe"]//span[@jsname="V67aGc"])[2]').click()
        
        for _ in range(self.amount):
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
                
                if self.remove_files:
                    print(f"removing {file_path}")
                    os.remove(file_path)
                
            except KeyboardInterrupt:   
                exit()