from pathlib import Path
from selenium import webdriver
import pandas as pd
import sys
import datetime

from Backend.FacebookMpParser import FacebookMpParser
from Backend.BlocketParser import BlocketParser


class DataManagement():
    def __init__(self, data_storage_location: Path) -> None:
        self.data_storage_location = data_storage_location
        self.web_scrapers = {
            "facebook": FacebookMpParser(),
            "blocket": BlocketParser(),
        }

        # Check if outputfolder exitts
        if data_storage_location and not data_storage_location.exists():
            data_storage_location.mkdir(parents=True)

    def get_data_from_website(self, website: str,  website_url: str, search_query: str) -> pd.DataFrame:
        scraped_data = pd.DataFrame()

        if website in self.web_scrapers.keys():
            webscraper = self.web_scrapers[website]

            if website_url:
                webscraper.change_website_url(website_url)

            if not self.data_already_parsed(website):
                scraped_data = self.scrape_data_from_website(website, website_url, search_query)

                if True:
                    self.save_website_data_from_website(scraped_data, webscraper, search_query)
            else:
                scraped_data = self.read_data_from_file(website)
        else:
            sys.exit(f"Could not find a webscraper for {website}, exiting...")

        return scraped_data

    def scrape_data_from_website(self, website: str, website_url: str, search_query: str) -> pd.DataFrame:
        return self.web_scrapers[website].scrape_data(search_query)

    def read_data_from_file(self, website) -> pd.DataFrame:
        pass

    def save_website_data_from_website(self, data: pd.DataFrame, webscraper: webdriver, search_query: str) -> None:
        """
        Save the parsed in the output folder. The data is saved in a file that is based on the provided query and url.
        Results are saved in sub directorys based on the current date. Each file contains the date and time it was
        created.
        """
        current_date = datetime.datetime.now()
        sub_dir = Path(self.data_storage_location / current_date.strftime("%Y_%m_%d"))
        if not sub_dir.exists():
            sub_dir.mkdir()

        filename = f"{current_date.strftime('%Y_%m_%d:%H-%M-%S')}"
        filename += f"_{webscraper.__class__.__name__}"
        filename += f"_{webscraper.get_url_search_category()}"
        filename += "_".join(search_query.split(' '))

        file_path = sub_dir / f"{filename}.pkl"

    def get_supported_websites(self) -> list:
        return list(self.web_scrapers.keys())

    def data_already_parsed(self, website: str) -> bool:
        return False
