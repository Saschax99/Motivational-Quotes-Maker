import time
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
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
        self.pages = 99
        
        for path in [QUOTES_PATH, TEMP_PATH]:
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
    
    def get_all_quotes(self) -> list:
        """Get the links of videos from a search keyword."""
        
        for _ in range(self.pages):    
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="quote"]')))
            element_count = self.browser.find_elements(By.XPATH, '//div[@class="quote"]')
            for element in element_count:
                image_element = element.find_elements(By.XPATH, './/img')
                if len(image_element) > 0:
                    image = image_element[0].get_attribute("src")
                else:
                    image = None
                text = element.find_element(By.XPATH, './/div[@class="quoteText"]').get_attribute("textContent").strip().split("\n")[0]
                autor = element.find_element(By.XPATH, './/span[@class="authorOrTitle"]').get_attribute("textContent").strip()
                print("image:", image)
                print("content:", text)
                print("autor:", autor)
                entry = {
                    "element": {
                        "image": image,
                        "content": text,
                        "autor": autor
                    },
                }
                self.write(entry)
                
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//a[@class="next_page"]')))
            self.browser.find_element(By.XPATH, '//a[@class="next_page"]').click()
    
    def write(self, data):
    # Write the JSON object to a file
        with open(os.path.join(self.quotes_path, self.quotes_file_name), "a", encoding='utf-8') as outfile:
            outfile.write("[")  
            json.dump(data, outfile, ensure_ascii=False)
            outfile.write("]")  
            outfile.write(",")
    
    # def read():
    #     filename = "my_data.json"  # Define the filename once at the beginning

    #     # Load the JSON data into memory
    #     with open(filename, "r") as infile:
    #         loaded_data = json.load(infile)

    #     # Define a function to retrieve a specific variable from the loaded data
    #     def get_variable(variable_name):
    #         if variable_name in loaded_data:
    #             return loaded_data[variable_name]
    #         else:
    #             return None

    #     # Retrieve specific variables from the loaded data using the get_variable function
    #     name = get_variable("person.name")
    #     age = get_variable("person.age")
    #     math_score = get_variable("tests[0].score")
    #     english_score = get_variable("tests[1].score")

    #     # Print the retrieved variables
    #     print("Name:", name)
    #     print("Age:", age)
    #     print("Math Score:", math_score)
    #     print("English Score:", english_score)
    
    def close(self) -> None:
        print("closing browser..")
        self.browser.close()
        
if __name__ == "__main__":
    #quotes = QuotesFetcher()
    #quotes.get_browser()
    #quotes.get_all_quotes()
    with open("quotes/quotes.json", "r", encoding='utf-8') as infile:
        loaded_data = json.load(infile)
    print(len(loaded_data))