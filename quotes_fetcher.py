import time
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
from config import SONGS_PATH, TEMP_PATH, RESULTS_PATH, TIMEOUT

class ShortsFetcher:
    """Class for fetching shorts videos."""
    
    def __init__(self):
        self.url = "https://www.goodreads.com/quotes?page=1"
        self.timeout = TIMEOUT
        self.quotes = []
        
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