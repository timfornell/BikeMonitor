from Code.Backend.DataManagement import DataManagement
import numpy as np
import pandas as pd


class UserInterface():
    def __init__(self) -> None:
        self.data_manager = DataManagement()
        self.search_result = pd.DataFrame()

    def get_input_from_user(self) -> None:
        pass

    def request_data_query(website: str, criterion: dict) -> None:
        pass

    def visualize_search_results() -> None:
        pass