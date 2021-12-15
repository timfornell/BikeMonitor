from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import random
import requests
import selenium
import selenium.webdriver.support.ui as ui
import time

from Backend.WebsiteParser import WebsiteParser

class BlocketParser(WebsiteParser):
    def __init__(self) -> None:
        # Setup Chromedriver for selenium
        self.service = Service(executable_path=ChromeDriverManager().install())
        # Default page containing 'all' objects for sale
        self.default_website_url = "https://www.blocket.se/annonser/"
        supported_query_keys = ["ELLER", "EJ", "*", '""']
        super().__init__(self.default_website_url, supported_query_keys)

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

                    # This part is added to make sure the page is fully loaded before parsing it. Selenium has functions
                    # that takes care of this in a proper way but this works "good enough" for this project.
                    sleep_time = random.random() * 10 + 10
                    print(f"Page opened. Will wait for {sleep_time} before parsing page...")
                    time.sleep(sleep_time)

                    # First page will have a cookie pop up that needs to be accepted
                    self.check_and_approve_cookies(driver)
                    ui.WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.TAG_NAME, "article"))
                    new_links, continue_parsing = self.find_links_and_scrape_data(driver)
                    relevant_links = relevant_links.append(new_links, ignore_index=True)

                    current_page += 1
                    query_url = query_url.replace(f"&page={current_page - 1}", f"&page={current_page}")

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
                        article_dict["location"] = category_location[1] if len(category_location) > 1 else ""
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

    def get_url_search_category(self) -> str:
        combined_string = ""
        if self.website_url == self.default_website_url:
            combined_string = "hela_sverige_alla_annonser"
        else:
            url_parts = self.website_url.replace(self.default_website_url, "").split("?")[0].split("/")
            combined_string = "_".join(url_parts)

        return combined_string

    def create_url_from_query(self, search_query: str) -> str:
        query_url = self.website_url

        if "&sort=date" not in query_url:
            query_url += "&sort=date"

        if search_query:
            query_url+= f"&q={search_query.replace(' ', '+')}"

        return query_url
