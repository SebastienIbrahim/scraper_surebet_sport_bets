from bs4 import BeautifulSoup
from models.sport import Sport
from models.country import Country
from models.competition import Competition
from models.match import Match
from models.team_odd import Team, Odd
from utils.logger import setup_scraper_logger, setup_error_logger, setup_captcha_logger
from utils.helpers import dump_json_data, normalize_teams_name
from utils.helpers import load_config_file
from scrapers.base_scraper import BaseScraper
from lxml import etree
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver
from scrapers.scraper import SiteScraper

scraper_logger, error_logger, captcha_logger = (
    setup_scraper_logger(),
    setup_error_logger(),
    setup_captcha_logger(),
)

settings = load_config_file("settings.yaml")
site_config = load_config_file("sites.yaml")
sites_name = list(site_config.keys())
raw_data_path = "instance"
conf = site_config["france-pari"]

self = SiteScraper("france-pari", conf, settings)

self.scrape()


def safe_get(self, page_obj: BeautifulSoup, selector: str) -> list[etree._Element]:
    """Get the text of the element selected by the selector passed in parameter

    Args:
        page_obj (BeautifulSoup): The page object to get the text from the element selected by the selector
        selector (str): The selector to select the element to get the text from

    Returns:
        str: The text of the element selected by the selector
    """
    page_obj, selector = country.button, self.tags_chamionship["championship_name"]
    type(page_obj)
    dir(page_obj)
    element_html = etree.tostring(page_obj, method="html", encoding="unicode")
    try:
        if isinstance(
            page_obj,
            (undetected_chromedriver.webelement.WebElement, BeautifulSoup, str),
        ):
            html_code = (
                page_obj.get_attribute("outerHTML")
                if isinstance(page_obj, undetected_chromedriver.webelement.WebElement)
                else str(page_obj)
            )

            page_obj = etree.HTML(html_code)
            selected_elems = page_obj.xpath(
                './/li[@class="item-arrow ui-desktop"]//span[@class="label-menu"]/text()'
            )
            dir(page_obj)
            dir(page_obj)
        elif isinstance(page_obj, undetected_chromedriver.Chrome):
            selected_elems = page_obj.find_elements(By.XPATH, selector)
        else:
            selected_elems = page_obj.xpath(selector)
    except Exception as e:
        error_logger.error(
            f"Exception: {e} was raised when we tried to get elements by the selector: {selector}"
        )
        selected_elems = []
    return selected_elems


class SiteScraper(BaseScraper):
    def __init__(self, site_name, site_config, settings):
        super().__init__(site_name, site_config, settings)

    def scrape(self) -> None:
        """Scrape the website

        Returns:
            None
        """
        home_page = self.get_page(self.home_page)
        time.sleep(5)
        if self.tags_button.get("cookies"):
            self.accept_cookies(self.tags_button["cookies"])
        self.get_random_sleep_time()
        sports = self.extract_sports(home_page)
        for sport in sports:
            dump_json_data(
                sport, f"instance/{self.site_name}/sports/{self.site_name}@{sport.name}"
            )

    def extract_sports(self, home_page: BeautifulSoup) -> list[Sport]:
        """Extract all sports from the home page
        Args:
            home_page (str): The home page of the website to scrape

        Returns:
            list[Sport]: The list of all sports
        """
        sports = []
        if self.philosophy == "click":
            sports_buttons = self.safe_get(
                self.driver.driver, self.tags_chamionship["sport"]
            )
        else:
            sports_buttons = self.safe_get(home_page, self.tags_chamionship["sport"])

        sports_name = self.safe_get(home_page, self.tags_chamionship["sport_name"])
        len(sports_buttons), len(sports_name)
        for sport_button, sport_name in zip(sports_buttons, sports_name):
            sport_button, sport_name = sports_buttons[0], sports_name[0]
            try:
                self.click_element(sport_button)
            except Exception as e:
                scraper_logger.error(f"Failed to click sport {sport_name} button: {e}")
                continue
            self.get_random_sleep_time()
            sport = Sport(sport_name, sport_button)
            countries = self.extract_countries(sport)
            sport.countries.extend(countries)
            scraper_logger.info(
                f"Processing of Sport {sport_name} with {len(countries)} countries"
            )
            sports.append(sport)
        return sports

    def extract_countries(self, sport: Sport) -> list[Country]:
        countries = []
        if self.philosophy == "click":
            countries_buttons = self.safe_get(
                self.driver.driver, self.tags_chamionship["country"]
            )
        else:
            countries_buttons = self.safe_get(
                sport.button, self.tags_chamionship["country"]
            )
        countries_names = self.safe_get(
            sport.button, self.tags_chamionship["country_name"]
        )
        close_country_buttons = self.safe_get(
            self.driver.driver, self.tags_chamionship.get("close_country")
        )
        len(countries_buttons), len(countries_names), len(close_country_buttons)

        if len(close_country_buttons) == 0:
            close_country_buttons = [None] * len(countries_buttons)

        for country_name, country_button, close_country_button in zip(
            countries_names, countries_buttons, close_country_buttons
        ):
            country_name, country_button, close_country_button = (
                countries_names[0],
                countries_buttons[0],
                close_country_buttons[0],
            )
            try:
                self.click_element(country_button)
                self.get_random_sleep_time()
            except Exception as e:
                scraper_logger.error(
                    f"Failed to click country {country_name} button: {e}"
                )
                continue
            self.get_random_sleep_time()
            country = Country(country_name, country_button)
            competitions = self.extract_competitions(country)
            if close_country_button is not None:
                self.click_element(close_country_button)
                print("=======close country button clicked======")
                self.get_random_sleep_time()
            country.competitions.extend(competitions)
            scraper_logger.info(
                f"Country: Extracted {country_name} country with {len(competitions)} competitions"
            )
            dump_json_data(
                country,
                f"instance/{self.site_name}/countries/{self.site_name}@{country.name}",
            )
            countries.append(country)

        return countries

    def extract_competitions(self, country: Country) -> list[Competition]:
        competitions = []
        if self.philosophy == "click":
            competitions_buttons = self.safe_get(
                self.driver.driver,
                self.tags_chamionship["championship"],
            )
        else:
            competitions_buttons = self.safe_get(
                country.button, self.tags_chamionship["championship"]
            )
        competitions_names = self.safe_get(
            country.button, self.tags_chamionship["championship_name"]
        )

        len(competitions_buttons), len(competitions_names)
        for competition_button, competition_name in zip(
            competitions_buttons, competitions_names
        ):
            competition_button, competition_name = (
                competitions_buttons[0],
                competitions_names[0],
            )
            try:
                self.click_element(competition_button)
                self.get_random_sleep_time()
            except Exception as e:
                scraper_logger.error(
                    f"Failed to click competition {competition_name} button: {e}"
                )
                continue
            competition = Competition(competition_name)
            matches = self.extract_matches(competition_button)
            competition.matches.extend(matches)
            scraper_logger.info(
                f"Competition: Extracted {competition_name} competition with {len(matches)} matches"
            )
            dump_json_data(
                competition,
                f"instance/{self.site_name}/competitions/{self.site_name}@{competition.name}",
            )
            competitions.append(competition)
        try:
            self.click_element(country.button)
        except Exception as e:
            print(f"Failed to click again on country {country.name} button: {e}")
        self.get_random_sleep_time()
        return competitions

    def extract_matches(self, competition_button) -> list[Match]:
        """Extract all matches from the competition link

        Args:
            competition_link (str): The competition link

        Returns:
            list[Match]: The list of all matches
        """
        matches = []
        match_page = None
        if self.philosophy == "link":
            match_page = self.get_page(self.normalize_url(competition_button))
            self.get_random_sleep_time()
        if self.tags_button.get("bet_filter"):
            self.click_on_button(self.tags_button["bet_filter"])
            self.get_random_sleep_time()
            match_page = BeautifulSoup(self.driver.driver.page_source, "html.parser")
            self.get_random_sleep_time()
        if self.philosophy == "click":
            matches_blocs = self.safe_get(
                self.driver.driver, self.tags_odd["bloc_match"]
            )
        else:
            matches_blocs = self.safe_get(
                match_page,
                self.tags_odd["bloc_match"],
            )
        len(matches_blocs)
        for match_bloc in matches_blocs:
            teams_name = self.safe_get(match_bloc, self.tags_odd["name_team"])
            try:
                teams_name = normalize_teams_name(teams_name)
                teams = [Team(team_name.strip()) for team_name in teams_name]
            except Exception as e:
                scraper_logger.error(
                    f"Failed to extract teams name: {teams_name} with {e}"
                )
                continue
            date_time = self.safe_get(match_bloc, self.tags_odd["date_hours"])
            odds_elements = self.safe_get(match_bloc, self.tags_odd["odd"])
            odds = [
                Odd(value=v, type=t, team_index=teams.index(e))
                for v, t, e in zip(odds_elements, ["Win", "Draw", "Win"], teams)
            ]
            match = Match(teams, date_time, odds)
            matches.append(match)
            match.to_dict()
        return matches
