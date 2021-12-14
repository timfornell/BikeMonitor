from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from Backend.WebsiteParser import WebsiteParser

class FacebookMpParser(WebsiteParser):
    """
    Class with the capability to parse facebook marketplace for articles fulfilling some search_query
    """
    def __init__(self) -> None:
        website_url = "https://www.facebook.com/marketplace/110680185620981/search/?query"
        supported_query_keys = []
        super().__init__(website_url, supported_query_keys)

    def scrape_data(self, search_query: str) -> pd.DataFrame:
        pass

    def create_url_from_query(self, search_query: str) -> str:
        pass
