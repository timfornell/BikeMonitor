from pathlib import Path
import pandas as pd
import sys

from Backend.FacebookMpParser import FacebookMpParser
from Backend.BlocketParser import BlocketParser


class DataManagement():
    def __init__(self, data_storage_location: Path) -> None:
        self.data_storage_location = data_storage_location
        self.web_scrapers = {
            "facebook": FacebookMpParser(),
            "blocket": BlocketParser(),
        }

    def get_data_from_website(self, website: str, search_query: str) -> pd.DataFrame:
        scraped_data = pd.DataFrame()

        if website in self.web_scrapers.keys():
            if not self.data_already_parsed(website):
                scraped_data = self.scrape_data_from_website(website, search_query)
                self.save_website_data_from_website(scraped_data)
            else:
                scraped_data = self.read_data_from_file(website)
        else:
            sys.exit(f"Could not find a webscraper for {website}, exiting...")

        return scraped_data

    def scrape_data_from_website(self, website: str, search_query: str) -> pd.DataFrame:
        self.web_scrapers[website].scrape_data(search_query)

    def read_data_from_file(self, website) -> pd.DataFrame:
        pass

    def save_website_data_from_website(self, data: pd.DataFrame) -> None:
        pass

    def get_supported_websites(self) -> list:
        return list(self.web_scrapers.keys())

    def data_already_parsed(self, website: str) -> bool:
        return False
