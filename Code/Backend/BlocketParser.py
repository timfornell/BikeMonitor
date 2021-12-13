import bs4

from Backend.WebsiteParser import WebsiteParser


class BlocketParser(WebsiteParser):
    def __init__(self) -> None:
        super().__init__("", {})
