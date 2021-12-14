from os import link
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import bs4
import pandas as pd
import random
import requests
import selenium.webdriver.support.ui as ui
import time

from Backend.WebsiteParser import WebsiteParser

class BlocketParser(WebsiteParser):
    def __init__(self) -> None:
        self.service = Service(executable_path=ChromeDriverManager().install())
        website_url = "https://www.blocket.se/annonser/hela_sverige/fritid_hobby/cyklar?cg=6060&sort=date"
        supported_query_keys = ["ELLER", "EJ", "*", '""']
        super().__init__(website_url, supported_query_keys)

    def scrape_data(self, search_query: str) -> pd.DataFrame:
        relevant_links = pd.DataFrame()
        query_url = self.create_url_from_query(search_query)

        try:
            continue_parsing = True
            current_page = 1
            query_url += f"&page={current_page}"
            
            with webdriver.Chrome(service=self.service) as driver:
                while continue_parsing:
                    print(f"Parsing {query_url}...")
                    driver.get(query_url)
                    
                    # First page will have a cookie pop up that needs to be accepted 
                    self.check_and_approve_cookies(driver)
                    ui.WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.TAG_NAME, "article"))
                    new_links, continue_parsing = self.find_links_and_scrape_data(driver)
                    relevant_links = relevant_links.append(new_links, ignore_index=True)

                    current_page += 1
                    query_url = query_url.replace(f"&page={current_page - 1}", f"&page={current_page}")

                    sleep_time = random.random() * 10 + 5
                    print(f"Parsing finished. Will wait for {sleep_time} before loading next page...")
                    time.sleep(sleep_time)

        except requests.exceptions.HTTPError as e:
            pass

        return relevant_links

    def check_and_approve_cookies(self, driver: webdriver) -> None:
        for element in driver.find_elements(By.TAG_NAME, "aside"):
            if "cookie" in element.accessible_name:
                for button in element.find_elements(By.TAG_NAME, "button"):
                    if "Jag samtycker" in button.accessible_name:
                        button.click()
                        return

    def find_links_and_scrape_data(self, driver: webdriver) -> pd.DataFrame:
        link_data = pd.DataFrame()
        continue_parsing = True

        articles = driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            article_dict = {
                "category": "",
                "location": "",
                "time": "",
                "link": ""
            }

            try:
                article_data = article.find_element(By.CSS_SELECTOR, "div[class^='styled__Content']")
                header_wrapper = article_data.find_element(By.CSS_SELECTOR, "div[class^='styled__LocationTimeWrapper']")
                subject_wrapper = article_data.find_element(By.CSS_SELECTOR, "div[class^='styled__SubjectWrapper']")
                
                for p_element in header_wrapper.find_elements(By.TAG_NAME, "p"):
                    class_name = p_element.get_attribute("class")
                    if "TopInfoWrapper" in class_name:
                        category_location = p_element.text.split(" · ")
                        article_dict["category"] = category_location[0]
                        article_dict["location"] = category_location[1]
                    elif "Time" in class_name:
                        article_dict["time"] = p_element.text

                article_dict["link"] = subject_wrapper.find_element(By.CSS_SELECTOR, "a[class^='Link']").get_attribute("href")
                
                # Only keep the articles uploaded today
                if "Idag" in article_dict["time"]:
                    link_data = link_data.append(article_dict, ignore_index=True)
                else:
                    continue_parsing = False
                    break
                
            except selenium.common.exceptions.NoSuchElementException as e:
                print(f"Got {e} while trying to parse {article}")

        if link_data.empty:
            continue_parsing = False

        return link_data, continue_parsing

    def scrape_data_from_link(driver: webdriver, link: str):
        pass

    def create_url_from_query(self, search_query: str) -> str:
        query_url = self.website_url

        if search_query:
            query_url+= f"&q={search_query}"

        return query_url
