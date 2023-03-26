import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class WebScraper:
    def __init__(self):
        self.url = "https://www.goodreads.com/quotes?page=1"
        self.timeout = 30

    def get_browser(self, url: str = None):
        """Establish a connection to the website using a ChromeDriver."""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")

        self.browser = webdriver.Chrome(use_subprocess=True, options=self.options)
        self.browser.maximize_window()
        if url is None:
            url = self.url
        self.browser.get(url)
        print(f"established connection to {url}")
        return self.browser
    
    def wait_for_element_to_be_visible(self, xpath: str, timeout: int = None) -> None:
        if timeout is None:
            timeout = self.timeout
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def find_element(self, xpath, reference_element = None):
        if reference_element is not None:
            element = reference_element.find_element(By.XPATH, xpath)
        element = self.browser.find_element(By.XPATH, xpath)
        return element
    
    def find_elements(self, xpath, reference_element = None):
        if reference_element is not None:
            element = reference_element.find_elements(By.XPATH, xpath)
        element = self.browser.find_elements(By.XPATH, xpath)
        return element
    
    def get_attribute(self, element, attribute):
        return element.get_attribute(attribute)
    
    def close(self) -> None:
        print("closing browser..")
        self.browser.close()
