import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from config import RESULTS_PATH, INSTA_USER, INSTA_PASSWORD
from os_tools import OsTools
import random

class InstagramShortsUploader:
    def __init__(self, amount, user, password, remove_files) -> None:
        self.amount = amount
        self.remove_files = remove_files
        self.url = "https://www.instagram.com"
        self.user = user
        self.password = password
        self.timeout = 15
        self.title = "Nature #travel #nature #shorts"
        self.description = [
            "#reels",
            "#reelsinstagram",
            "#instagram",
            "#trending",
            "#viral",
            "#explore",
            "#love",
            "#instagood",
            "#explorepage",
            "#tiktok",
            "#india",
            "#photography",
            "#fyp",
            "#reel",
            "#instadaily",
            "#reelsvideo",
            "#foryou",
            "#music",
            "#travelling",
            "#traveling",
            "#travel",
            "#travelbug",
            "#traveldiary",
            "#instatravel",
            "#travelholic",
            "#travelers",
            "#travelguide",
            "#travellife",
            "#travelgram",
            "#traveldiaries",
            "#wonderlust",
            "#travelgram",
            "#traveler",
            "#traveladdict",
            "#travelblog",
            "#nature",
            "#travelreels",
            "#tourism",
            "#instatraveling",
            "#adventure",
            "#sunset",
            "#sunrise",
            "#naturephotography",
            "#landscape",
            "#naturelovers",
            "#travelphotography",
            "#mountains",
            "#beach",
            "#hiking",
            "#likenowhereelse",
            "#nowehereelse"
            ]
        self.shoutout = "Music by Bass Rebels"

    def get_browser(self, url: str = None):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")
        self.options.add_argument("--log-level=3")

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)
        
    def upload_video_series(self, path: str = None) -> None:
        if path is None:
            path = RESULTS_PATH
        if OsTools.get_folder_count(path) <= 0:
            raise RuntimeError(f"no videos in '{path}' found!")
            
        cookie_popup = WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe x5yr21d x19onx9a"]//button[@class="_a9-- _a9_1"]')))
        cookie_popup.click()
        WebDriverWait(self.browser, self.timeout).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe x5yr21d x19onx9a"]//button[@class="_a9-- _a9_1"]')))
        
        WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="username"]')))
        input_email = self.browser.find_element(By.XPATH, '//input[@name="username"]')
        input_email.send_keys(self.user)
                
        WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
        input_pass = self.browser.find_element(By.XPATH, '//input[@name="password"]')
        input_pass.send_keys(self.password)
        
        self.browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '(//div[@class="x1n2onr6"]/div[@class="x1n2onr6"])[2]')))
        
        WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="_a9-- _a9_1"]')))
        self.browser.find_element(By.XPATH, '//button[@class="_a9-- _a9_1"]').click()  # click on no notification
        
        for _ in range(self.amount):
            try:
                self.browser.find_element(By.XPATH, '(//div[@class="x1n2onr6"]/div[@class="x1n2onr6"])[2]').click()  # click on create
                
                #WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_acan _acap _acas _aj1-"]')))
                #self.browser.find_element(By.XPATH, '//button[@class="_acan _acap _acas _aj1-"]').click()  # click on upload
                
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]')))
                file_input = self.browser.find_element(By.XPATH, '//input[@accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]')
                selected_file = OsTools.select_specific_object_from_folder(RESULTS_PATH, 0)
                print(f"selected file name {selected_file}")
                file_path = os.path.join(RESULTS_PATH, selected_file)
                abs_path = os.path.abspath(file_path)
                file_input.send_keys(abs_path)
                
                if _ <= 0:
                    WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_acan _acap _acaq _acas _acav _aj1-"]')))
                    self.browser.find_element(By.XPATH, '//button[@class="_acan _acap _acaq _acas _acav _aj1-"]').click()  # click on
                
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '(//div[@role="button"]//button[@type="button"]/div[@class="_ab8w  _ab94 _ab97 _ab9h _ab9k _ab9p  _ab9y _aba8 _abcm"])[1]')))
                self.browser.find_element(By.XPATH, '(//div[@role="button"]//button[@type="button"]/div[@class="_ab8w  _ab94 _ab97 _ab9h _ab9k _ab9p  _ab9y _aba8 _abcm"])[1]').click()  # click on change resolution tab
                
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='_ac36 _ac38']//button[@class='_acan _acao _acas _aj1-'])[3]")))
                self.browser.find_element(By.XPATH, "(//div[@class='_ac36 _ac38']//button[@class='_acan _acao _acas _aj1-'])[3]").click()  # click on 9:16

                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa _abcm"]//button[@class="_acan _acao _acas _aj1-"]')))
                self.browser.find_element(By.XPATH, '//div[@class="_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa _abcm"]//button[@class="_acan _acao _acas _aj1-"]').click()  # click on continue
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@style="width: 1090px; max-width: 1195px; min-width: 688px; min-height: 391px; max-height: 898px;"]')))
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa _abcm"]//button[@class="_acan _acao _acas _aj1-"]')))
                self.browser.find_element(By.XPATH, '//div[@class="_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa _abcm"]//button[@class="_acan _acao _acas _aj1-"]').click()  # click on continue
                
                description_content = " ".join(random.sample(self.description, 5)) + " " + self.shoutout
                print(description_content)
                WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="xw2csxc x1odjw0f x1n2onr6 x1hnll1o xpqswwc x5dp1im xl565be xdj266r x11i5rnm xat24cr x1mh8g0r x1w2wdq1 xen30ot x1swvt13 x1pi30zi xh8yej3 x5n08af notranslate"]')))
                description = self.browser.find_element(By.XPATH, '//div[@class="xw2csxc x1odjw0f x1n2onr6 x1hnll1o xpqswwc x5dp1im xl565be xdj266r x11i5rnm xat24cr x1mh8g0r x1w2wdq1 xen30ot x1swvt13 x1pi30zi xh8yej3 x5n08af notranslate"]')
                description.send_keys(description_content)
                
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa _abcm"]//button[@class="_acan _acao _acas _aj1-"]')))
                self.browser.find_element(By.XPATH, '//div[@class="_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9- _abaa _abcm"]//button[@class="_acan _acao _acas _aj1-"]').click()  # click on share/publish
                try:
                    WebDriverWait(self.browser, self.timeout * 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x2b8uid x4zkp8e xw06pyt x10wh9bi x1wdrske x8viiok x18hxmgj" and contains(text(), "has been shared")]')))  # wait until uploaded
                except:
                    WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_acan _acap _acas _aj1-" and contains(text(), "Try again")]')))  # wait until try again button appears
                    self.browser.find_element(By.XPATH, '//button[@class="_acan _acap _acas _aj1-" and contains(text(), "Try again")]').click()  # click on try again
                    WebDriverWait(self.browser, self.timeout * 4).until(EC.presence_of_element_located((By.XPATH, '//span[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x2b8uid x4zkp8e xw06pyt x10wh9bi x1wdrske x8viiok x18hxmgj" and contains(text(), "has been shared")]')))  # wait until uploaded
                    
                WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, '(//div[@class="x1n2onr6"]/div[@class="x1n2onr6"])[2]')))
                self.browser.find_element(By.XPATH, '//div[@class="x78zum5 x6s0dn4 xl56j7k xdt5ytf"]').click()  # click on close modal

                # try:
                #     WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//tp-yt-iron-icon[@class="error-icon style-scope ytcp-uploads-dialog"]')))
                #     print("limit reached")
                #     exit(0)
                # except:
                #     self.browser.find_element(By.XPATH, '//*[@id="done-button"]').click()
                                
                if self.remove_files:
                    print(f"removing {file_path}")
                    os.remove(file_path)
                
            except KeyboardInterrupt:
                exit()
                
if __name__ == "__main__":
    instUploader = InstagramShortsUploader(100, INSTA_USER, INSTA_PASSWORD, True)
    instUploader.get_browser()
    instUploader.upload_video_series()
    exit()
