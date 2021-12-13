from pathlib import Path
import pandas as pd


class DataManagement():
    def __init__(self, data_storage_location: Path) -> None:
        self.data_storage_location = data_storage_location

    def get_data_from_website(self, website: str, criterion: dict) -> pd.Dataframe:
        pass

    def scrape_data_from_website(self, website: str) -> pd.DataFrame:
        pass

    def save_website_data_from_website(self, data: pd.DataFrame) -> None:
        pass