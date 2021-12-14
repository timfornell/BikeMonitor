import argparse
from Backend.DataManagement import DataManagement
from Frontend.UserInterface import UserInterface


def main(website: str, search_query: str) -> None:
    interface = UserInterface()

    interface.request_data_query(website, search_query)


if __name__ == "__main__":
    data_manager = DataManagement("")

    search_query_help_text = "\nThe following querys are supported by the different website scrapers:\n"
    for key, scraper in data_manager.web_scrapers.items():
        search_query_help_text += (f"\t- {key}: {str(scraper)}\n")

    p = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("website", help="Which website to scrape.", choices=data_manager.get_supported_websites())
    p.add_argument("--search_query", help=f"Query string to use when scraping. {search_query_help_text}", default="")
    a = p.parse_args()

    main(a.website, a.search_query)