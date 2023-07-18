import time
import random
from bs4 import BeautifulSoup
from lxml import etree
from utils.helpers import Driver
from urllib.parse import urlparse


class BaseScraper:
    """Base class for all scrapers

    Attributes:
        home_page (str): The home page of the website to scrape
        absolute_url (bool): True if the url is absolute, False otherwise
        tags (dict): The tags to use to scrape the website
        sleep_delay (dict): The sleep delay to use between each request
        driver (Driver): The driver to use to scrape the website
    """

    def __init__(self, site_config, settings):
        self.home_page = site_config["home_page"]
        self.absolute_url = site_config["absolute_url"]
        self.tags = site_config["tags"]
        self.sleep_delay = settings["sleep_delay"]
        self.driver = Driver(port=settings["port"])

    def get_page(self, url) -> BeautifulSoup:
        """Get the page with the url passed in parameter
        Args:
            url (str): The url of the page to get
            Returns:
                BeautifulSoup: The page object
        """
        try:
            self.driver.driver.get(url)
        except Exception as e:
            msg = f"This exception: {e} was raise when we try to get the page: {url}"
            # TODO: log this exception wtih logging module and also display with popupmsg alert
            return None
        bs = BeautifulSoup(self.driver.driver.page_source, "html.parser")
        if self.check_captcha(bs):
            msg = f"Be carefule, we have captcha when we try to get the page: {url}, please check and resolve it"
            # TODO: log this exception wtih logging module and also display with popupmsg alert
        return bs

    def click_on_button(self, button_selector: str) -> None:
        """Click on a button

        Args:
            button_selector (str): The selector of the button to click on
        """
        try:
            button = self.driver.find_element_by_xpath(button_selector)
            button.click()
        except Exception as e:
            msg = f"This exception: {e} was raise when we try to click on the button: {button_selector}"
            # TODO: log this exception wtih logging module and also display with popupmsg alert

    def get_random_sleep_time(self) -> None:
        """Get a random sleep time between min_delay and max_delay"""
        time.sleep(
            random.randint(
                self.sleep_delay.get("min_secondes", 20),
                self.sleep_delay.get("max_secondes", 60),
            )
        )

    def safe_get(self, page_obj: BeautifulSoup, selector: str) -> str:
        """Get the text of the element selected by the selector passed in parameter

        Args:
            page_obj (BeautifulSoup): The page object to get the text from the element selected by the selector
            selector (str): The selector to select the element to get the text from

        Returns:
            str: The text of the element selected by the selector
        """
        selected_elems = etree.HTML(str(page_obj)).xpath(selector)
        if selected_elems is not None and len(selected_elems) > 0:
            try:
                return "\n".join([elem.text.strip() for elem in selected_elems])
            except Exception as e:
                return "\n".join([elem for elem in selected_elems])
        return ""

    def check_captcha(self, page_obj: BeautifulSoup) -> bool:
        """Check if the page has captcha

        Args:
            page_obj (BeautifulSoup): The page object to check if it has captcha

        Returns:
            bool: True if the page has captcha, False otherwise
        """
        is_captchat_found = False
        try:
            selected_elems = self.safe_get(page_obj, self.tags.get("captcha"))
            is_captchat_found = selected_elems is not None and len(selected_elems) > 0
        # TODO: handle this exception explicitly
        except:
            pass
        return is_captchat_found

    def normalize_url(self, url: str) -> str:
        """Normalize the url passed in parameter
        Args:
            url (str): The url to normalize

        Returns:
            str: The normalized url
        """
        home_page = urlparse(self.home_page)
        if not urlparse(url).netloc:
            if not url.startswith("/"):
                url = "/" + url
            return "{}://{}".format(home_page.scheme, home_page.netloc) + url
        return url
