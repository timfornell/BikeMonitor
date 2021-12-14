from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import bs4
import pandas as pd
import requests

from Backend.WebsiteParser import WebsiteParser

class BlocketParser(WebsiteParser):
    def __init__(self) -> None:
        self.service = Service(executable_path=ChromeDriverManager().install())
        website_url = "https://www.blocket.se/annonser/hela_sverige/fritid_hobby/cyklar?cg=6060&sort=date"
        supported_query_keys = ["ELLER", "EJ", "*", '""']
        super().__init__(website_url, supported_query_keys)

    def scrape_data(self, search_query: str) -> pd.DataFrame:
        query_url = self.create_url_from_query(search_query)

        try:
            current_page = 1
            query_url += f"&page={current_page}"
            
            with webdriver.Chrome(service=self.service) as driver:
                while True:
                    driver.get(query_url)
                    
                    # First page will have a cookie pop up that needs to be accepted 
                    self.check_and_approve_cookies(driver)
                    ui.WebDriverWait(driver, 10).until(lambda d: d.find_element_by_tag_name("h2"))

                    self.find_links_and_scrape_data()
                    current_page += 1
                    query_url = query_url.replace(f"&page={current_page - 1}", f"&page={current_page}")

        except requests.exceptions.HTTPError as e:
            pass

    def check_and_approve_cookies(self, driver: webdriver) -> None:
        for element in driver.find_elements(By.TAG_NAME, "aside"):
            if "cookie" in element.accessible_name:
                for button in element.find_elements(By.TAG_NAME, "button"):
                    if "Jag samtycker" in button.accessible_name:
                        button.click()
                        return

    def find_links_and_scrape_data(self, driver: webdriver) -> pd.DataFrame:
        link_data = pd.DataFrame()
        h2_elements = driver.find_elements(By.TAG_NAME, "h2")
        for element in h2_elements:
            for a_element in element.find_elements(By.TAG_NAME, "a"):
                link = a_element.get_attribute("href")
                if link and "annons" in link:
                    links.append(link)

    def create_url_from_query(self, search_query: str) -> str:
        query_url = self.website_url

        if search_query:
            query_url+= f"&q={search_query}"

        return query_url
