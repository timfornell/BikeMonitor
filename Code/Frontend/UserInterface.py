from Backend.DataManagement import DataManagement
from pathlib import Path
import numpy as np
import pandas as pd


class UserInterface():
    def __init__(self) -> None:
        self.data_manager = DataManagement(Path.cwd() / "DataStorage")
        self.search_result = pd.DataFrame()

    def get_input_from_user(self) -> tuple:
        print(
        "Please provide the follwing arguments one by one:" +
        "\n\t- website" +
        "\n\t- search criterion"
        )

        supported_sites = [f"\t- {site}" for site in self.data_manager.get_supported_websites()]
        supported_sites = "\n".join(supported_sites)

        website = input(
            f"\nPlease type the name of the website, the following website are supported:\n {supported_sites}\n"
        )

        criterion = input("Please type the criterion you want to include in the query as a comma separated list:\n")

        return website, criterion

    def request_data_query(self, website: str, criterion: dict) -> None:
        self.data_manager.get_data_from_website(website, criterion)

    def visualize_search_results() -> None:
        pass