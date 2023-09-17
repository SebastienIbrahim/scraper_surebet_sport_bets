from pathlib import Path
import os
import yaml
from undetected_chromedriver import Chrome, ChromeOptions
from utils.logger import setup_scraper_logger
import json
from datetime import datetime

scraper_logger = setup_scraper_logger()


def dump_json_data(sport, filename):
    """
    Dump the data of a sport to a JSON file.

    Args:
        sport (Sport): The Sport object containing the data to be saved.
        filename (str): The name of the file to save the data to.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename}_{timestamp}.json"
    relative_site_directory = "/".join(filename.split("/")[:-2])
    absolute_site_directory = Path(__file__).parent.parent / relative_site_directory
    if not os.path.exists(absolute_site_directory):
        os.makedirs(absolute_site_directory)
    path = Path(__file__).parent.parent / filename
    dump_path = Path(__file__).parent.parent / "/".join(str(path).split("/")[:-1])

    if not os.path.exists(dump_path):
        os.makedirs(dump_path)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(sport.to_dict(), file, ensure_ascii=False, indent=4)
    # scraper_logger.info(f"Data for {sport.name} saved to {filename}")


class Driver:
    """The driver class to use to get the page with selenium
    Args:
        port (int, optional): The port to use to connect to the driver. Defaults to 2023.
    """

    def __init__(self, port: int = 2023, chromedriver_path=None):
        self.port = port
        self.options = ChromeOptions()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument(f"--remote-debugging-port={self.port}")
        self.driver = Chrome(options=self.options, executable_path=chromedriver_path)


def normalize_teams_name(teams: list) -> list:
    if len(teams) == 3:
        return teams
    elif len(teams) == 2:
        return [teams[0], "Draw", teams[1]]


def load_config_file(filename: str) -> dict[str, str]:
    """Load a YAML config file.
    Args:
        filename (str): The name of the file to load.
        Returns:
            dict: The configuration data.
    """
    path = Path(__file__).parent.parent / "config" / filename
    try:
        with open(f"{path}", "r") as file:
            config_data = yaml.safe_load(file)
            return config_data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {filename} was not found.")
