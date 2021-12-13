import pandas as pd

from Backend.WebsiteParser import WebsiteParser

class FacebookMpParser(WebsiteParser):
    """
    Class with the capability to parse facebook marketplace for articles fulfilling some criterion
    """
    def __init__(self) -> None:
        website_url = "https://www.facebook.com/marketplace/110680185620981/search/?query"
        super().__init__(website_url, {})

    def scrape_data(self, criterion: dict) -> pd.DataFrame:
        pass

    def create_url_from_query(self, criterion: dict) -> str:
        pass
