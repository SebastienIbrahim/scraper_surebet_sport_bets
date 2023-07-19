from pathlib import Path
import yaml
from undetected_chromedriver import Chrome, ChromeOptions


class Driver:
    """The driver class to use to get the page with selenium
    Args:
        port (int, optional): The port to use to connect to the driver. Defaults to 2023.
    """

    def __init__(self, port: int = 2023):
        self.port = port
        self.options = ChromeOptions()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument(f"--remote-debugging-port={self.port}")
        self.driver = Chrome(options=self.options)


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
