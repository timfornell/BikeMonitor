import pandas as pd
from selenium import webdriver


class WebsiteParser():
    """
    Parent class for all data scrapers
    """

    def __init__(self, website_url: str, supported_query_keys: list) -> None:
        """
        Parameters:
        - website_url (str): A string with the website url
        - supported_query_keys (list): A list of operations that are supported by the websites search function
        """
        
        self.website_url = website_url
        self.supported_query_keys = supported_query_keys

    def __str__(self) -> str:
        """
        This function is only ever used to print the help text for the program. 
        """
        return ", ".join(self.supported_query_keys) if self.supported_query_keys else "None"

    def scrape_data(self, search_query: str) -> pd.DataFrame:
        """
        Scrape data from self.website_url

        Parameters:
        - search_query (dict): Criterion to use to find matching items on website
        """
        pass

    def create_url_from_query(self, search_query: str) -> str:
        """
        Use the search_query to create a search string
        """
        pass