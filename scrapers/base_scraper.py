import time
import random
from bs4 import BeautifulSoup
from lxml import etree
from utils.helpers import Driver
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver
from utils.logger import setup_scraper_logger, setup_error_logger, setup_captcha_logger

scrapper_logger, error_logger, captcha_logger = (
    setup_scraper_logger(),
    setup_error_logger(),
    setup_captcha_logger(),
)


class BaseScraper:
    """Base class for all scrapers

    Attributes:
        home_page (str): The home page of the website to scrape
        absolute_url (bool): True if the url is absolute, False otherwise
        tags (dict): The tags to use to scrape the website
        sleep_delay (dict): The sleep delay to use between each request
        driver (Driver): The driver to use to scrape the website
    """

    def __init__(self, site_name, site_config, settings):
        self.site_name = site_name
        self.home_page = site_config["home_page"]
        self.absolute_url = site_config["absolute_url"]
        self.tags_chamionship = site_config["tags_chamionship"]
        self.tags_button = site_config["tags_button"]
        self.data_odd_type = site_config["data-odd-type"]
        self.tags_odd = site_config["tags_odd"]
        self.sleep_delay = settings["sleep_delay"]
        self.philosophy = site_config["philosophy"]
        self.driver = Driver(
            port=settings["port"], chromedriver_path=settings["chromedriver_path"]
        )

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
            error_logger.error(msg)
            # TODO: log this exception wtih logging module and also display with popupmsg alert
            return None
        bs = BeautifulSoup(self.driver.driver.page_source, "html.parser")
        if self.check_captcha(bs):
            msg = f"Be carefule, we have captcha when we try to get the page: {url}, please check and resolve it"
            captcha_logger.warning(msg)
            # TODO: log this exception wtih logging module and also display with popupmsg alert
        return bs

    def accept_cookies(self, cookie_selector: str) -> None:
        try:
            # Rechercher le bouton/élément pour accepter les cookies (utilisez le sélecteur approprié)
            # Exemple : recherche par XPath
            accept_button = self.driver.driver.find_element(By.XPATH, cookie_selector)

            wait = WebDriverWait(self.driver.driver, 10)
            wait.until(EC.element_to_be_clickable((By.XPATH, cookie_selector)))
            # Cliquer sur le bouton pour accepter les cookies
            accept_button.click()
            scrapper_logger.info("Cookies accepted")
        except Exception as e:
            msg = f"This exception: {e} was raise when we try to accept cookies"
            error_logger.error(msg)

    def safe_get(self, page_obj: BeautifulSoup, selector: str) -> list[etree._Element]:
        """Get the text of the element selected by the selector passed in parameter

        Args:
            page_obj (BeautifulSoup): The page object to get the text from the element selected by the selector
            selector (str): The selector to select the element to get the text from

        Returns:
            str: The text of the element selected by the selector
        """
        try:
            if isinstance(
                page_obj,
                (undetected_chromedriver.webelement.WebElement, BeautifulSoup, str),
            ):
                html_code = (
                    page_obj.get_attribute("outerHTML")
                    if isinstance(
                        page_obj, undetected_chromedriver.webelement.WebElement
                    )
                    else str(page_obj)
                )
                page_obj = etree.HTML(html_code)
                selected_elems = page_obj.xpath(selector)
            elif isinstance(page_obj, undetected_chromedriver.Chrome):
                selected_elems = page_obj.find_elements(By.XPATH, selector)
            else:
                selected_elems = page_obj.xpath(selector)
        except Exception as e:
            error_logger.error(
                f"Exception: {e} was raised when we tried to get elements by the selector: {selector}"
            )
            selected_elems = []
        if all(isinstance(elem, str) for elem in selected_elems):
            selected_elems = [elem.strip() for elem in selected_elems if elem.strip()]
        return selected_elems

    def click_on_button(self, button_selector: str) -> None:
        """Click on a button

        Args:
            button_selector (str): The selector of the button to click on
        """
        try:
            button = self.driver.driver.find_element(By.XPATH, button_selector)
            button.click()
            # TODO: if we have captcha, log it and display it with popupmsg alert
        except Exception as e:
            msg = f"This exception: {e} was raise when we try to click on the button: {button_selector}"
            error_logger.error(msg)
            # TODO: log this exception wtih logging module and also display with popupmsg alert

    def click_element(
        self, element: undetected_chromedriver.webelement.WebElement
    ) -> None:
        """Click on a button
        Args:
            element undetected_chromedriver.webelement.WebElement: The element to click on
            Returns:
        """
        if isinstance(element, undetected_chromedriver.webelement.WebElement):
            try:
                wait = WebDriverWait(self.driver.driver, 10)
                element = wait.until(EC.element_to_be_clickable(element))
                element.click()
                print("element clicked first try")
            except Exception:
                try:
                    # Scroll to the element if it is not in the visible area
                    actions = ActionChains(self.driver.driver)
                    print("ActionChains instantiated")
                    actions.move_to_element(element).perform()
                    print("element moved to")
                    wait = WebDriverWait(self.driver.driver, 10)
                    print("WebDriverWait instantiated")
                    element = wait.until(EC.element_to_be_clickable(element))
                    print("element clickable")
                    element.click()
                    print("element clicked second try")
                except Exception:
                    print("element not clickable")
                    self.driver.driver.execute_script("arguments[0].click();", element)
                    print("element clicked third try")

    def get_random_sleep_time(self) -> None:
        """Get a random sleep time between min_delay and max_delay"""
        time.sleep(
            random.randint(
                self.sleep_delay.get("min_secondes", 3),
                self.sleep_delay.get("max_secondes", 5),
            )
        )

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
