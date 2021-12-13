import pandas as pd


class WebsiteParser():
    """
    Parent class for all data scrapers
    """

    def __init__(self, website_url: str, website_structure: dict) -> None:
        """
        Parameters:
        - website_url (str): A string with the website url
        - website_structure (dict): A dict representing the webpage structure of the webpage
        """
        
        self.website_url = website_url
        self.website_structure = {}

    def scrape_data(self, criterion: dict) -> pd.DataFrame:
        """
        Scrape data from self.website_url using the structure defined in self.website_structure

        Parameters:
        - criterion (dict): Criterion to use to find matching items on website
        """
        pass