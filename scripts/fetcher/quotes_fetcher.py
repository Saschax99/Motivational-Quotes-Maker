import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from config import QUOTES_PATH, TEMP_PATH, TIMEOUT
import json


class QuotesFetcher:
    """Class for fetching shorts videos."""

    def __init__(self):
        self.url = "https://www.goodreads.com/quotes?page=1"
        self.timeout = TIMEOUT
        self.quotes = []
        self.quotes_file_name = "quotes.json"
        self.quotes_path = QUOTES_PATH
        self.pages = 100

        for path in [QUOTES_PATH, TEMP_PATH]:
            if not os.path.exists(path):
                os.makedirs(path)

    def get_browser(self, url: str = None) -> None:
        """Establish a connection to the website using a ChromeDriver.

        Args:
            url (str, optional): url of website. Defaults to None.
        """
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)

    def get_all_quotes(self):
        """Get the links of videos from a search keyword
        """
        for _ in range(self.pages):
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="quote"]')))
            element_count = self.browser.find_elements(By.XPATH, '//div[@class="quote"]')
            for element in element_count:
                image_element = element.find_elements(By.XPATH, './/img')
                if len(image_element) > 0:
                    image = image_element[0].get_attribute("src")
                else:
                    image = None
                text = \
                    element.find_element(By.XPATH, './/div[@class="quoteText"]').get_attribute(
                        "textContent").strip().split(
                        "\n")[0]
                author = element.find_element(By.XPATH, './/span[@class="authorOrTitle"]').get_attribute(
                    "textContent").strip()
                print("image:", image)
                print("content:", text)
                print("author:", author)
                entry = {
                    "element": {
                        "image": image,
                        "content": text,
                        "author": author
                    },
                }
                self.write(entry)

            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="next_page"]')))
            self.browser.find_element(By.XPATH, '//a[@class="next_page"]').click()

    def write(self, data):
        """write the JSON object to a file

        Args:
            data (list): data to write
        """
        with open(os.path.join(self.quotes_path, self.quotes_file_name), "a", encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
            outfile.write(",\n")

    def close(self) -> None:
        print("closing browser..")
        self.browser.close()
