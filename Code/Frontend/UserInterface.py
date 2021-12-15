from Backend.DataManagement import DataManagement
from pathlib import Path
import numpy as np
import pandas as pd


class UserInterface():
    def __init__(self) -> None:
        self.data_manager = DataManagement(Path.cwd() / "DataStorage")
        self.search_result = pd.DataFrame()

    def request_data_query(self, website: str, website_url: str, search_query: dict) -> None:
        self.data_manager.get_data_from_website(website, website_url, search_query)

    def visualize_search_results() -> None:
        pass