import pandas as pd


class WebsiteParser():
    def __init__(self, website_url: str) -> None:
        self.website_url = website_url
        self.website_structure = {}

    def scrape_data(self, criterion: dict) -> pd.DataFrame:
        pass