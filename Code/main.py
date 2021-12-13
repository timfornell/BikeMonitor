import argparse
from Frontend.UserInterface import UserInterface


def main() -> None:
    interface = UserInterface()

    # website, criterion = interface.get_input_from_user()
    # interface.request_data_query(website, criterion)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    a = p.parse_args()

    # main()