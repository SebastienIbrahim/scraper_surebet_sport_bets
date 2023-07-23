%load_ext autoreload
%autoreload 2
from utils.logger import setup_scraper_logger, setup_error_logger, setup_captcha_logger
from utils.helpers import load_config_file, dump_json_data
from scrapers.base_scraper import BaseScraper
from scrapers.scraper import SiteScraper
from models.sport import Sport
from models.country import Country
from models.competition import Competition
from models.match import Match
from models.team_odd import Team, Odd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree

import undetected_chromedriver

scraper_logger, error_logger, captcha_logger = (
    setup_scraper_logger(),
    setup_error_logger(),
    setup_captcha_logger(),
)

settings = load_config_file("settings.yaml")


site_2_name = "parionsport"
site_config_site_2 = load_config_file("sites.yaml")[site_2_name]


scraper_site_2 = SiteScraper(site_2_name, site_config_site_2, settings)

self = scraper_site_2

home_page = self.get_page(self.home_page)


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
        len(countries_buttons), len(countries_names)
        for country_name, country_button in zip(countries_names, countries_buttons):
            country_name, country_button = countries_names[2], countries_buttons[2]
            type(country_button)
            try:
                self.click_element(country_button)
            except Exception as e:
                scraper_logger.error(
                    f"Failed to click country {country_name} button: {e}"
                )
                continue
            self.get_random_sleep_time()
            country = Country(country_name, country_button)
            competitions = self.extract_competitions(country)
            country.competitions.extend(competitions)
            scraper_logger.info(
                f"Country: Extracted {country_name} country with {len(competitions)} competitions"
            )
            dump_json_data(
                country, f"instance/countries/{self.site_name}@{country.name}"
            )
            countries.append(country)
        return countries


def extract_competitions(self, country: Country) -> list[Competition]:
        competitions = []
        if self.philosophy == "click":
            competitions_buttons = self.safe_get(
                self.driver.driver, self.tags_chamionship["championship"]
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
            competition_button, competition_name = competitions_buttons[0], competitions_names[0]
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
                f"instance/competitions/{self.site_name}@{competition.name}",
            )
            competitions.append(competition)
        return competitions


from bs4 import BeautifulSoup
from utils.helpers import normalize_teams_name
import undetected_chromedriver


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
            matches_blocs = self.safe_get(match_page, self.tags_odd["bloc_match"])
        for match_bloc in matches_blocs:
            teams_name = self.safe_get(match_bloc, self.tags_odd["name_team"])
            teams_name = normalize_teams_name(teams_name)
            teams = [Team(team_name.strip()) for team_name in teams_name]
            date_time = self.safe_get(match_bloc, self.tags_odd["date_hours"])
            odds_elements = self.safe_get(match_bloc, self.tags_odd["odd"])
            odds = [
                Odd(value=v, type=t, team_index=teams.index(e))
                for v, t, e in zip(odds_elements, self.data_odd_type, teams)
            ]
            match = Match(teams, date_time, odds)
            matches.append(match)

        return matches

for m in matches:
    print(m.to_dict())

    def from_html(driver, html_str):
        """Convert an HTML string to a WebElement object

        Args:
            driver (WebDriver): The WebDriver object
            html_str (str): The HTML string

        Returns:
            WebElement: The WebElement object
        """

        element = undetected_chromedriver.chrome.WebElement()
        element._source = html_str
        return element



def extract_countries(self, sport: Sport) -> list[Country]:
        countries = []
        # countries_buttons = self.safe_get(
        #     self.driver.driver, self.tags_chamionship["country"]
        # )
        countries_buttons = self.safe_get(
            sport.button, self.tags_chamionship["country"]
        )
        dir(self.driver.driver)
        len(countries_buttons)
        type(sport.button), type(self.driver.driver)
        countries_names = self.safe_get(
            sport.button, self.tags_chamionship["country_name"]
        )
        len(countries_buttons), len(countries_names)
        
        for country_name, country_button in zip(countries_names, countries_buttons):
            print(i)
            i+=1
            pass
            country_name, country_button = countries_names[0], countries_buttons[0]
            country_button
            outer_html = etree.tostring(country_button).decode('utf-8')
            self.driver.driver.find_elements(By.LINK_TEXT, country_name)
            dir(self.driver.driver)
            t = self.driver.driver.find_elements_recursive(By.XPATH, self.tags_chamionship["country"])
            for i, v in enumerate(t):
                 print(i)
            type(country_button)
            country_button.keys()
            dir(country_button)
            country_button.getchildren()[0]
            country_button.values()[0]
            country_button.sourceline
            country_button.click()
            country_button.tag
            country_button.get_attribute("outerHTML")
            a = country_button.xpath(self.tags_chamionship["country"])
            
            html_code = etree.tostring(country_button).decode("utf-8")
            wait = WebDriverWait(self.driver.driver, 10)
            wait.until(EC.element_to_be_clickable(country_button))

            a = [ s for s in  country_button.text]
            country_button
            try:
                tmp_element = undetected_chromedriver.WebElement(self.driver.driver,html_code)
                tmp_element.click()
                self.driver.driver.find_elements(By.LINK_TEXT, country_name).click()
                self.driver.driver.(self.tags_chamionship["country"]).click()
                self.driver.driver.create_web_element(tmp_element).click()
                self.driver.driver.create_web_element
                script = "arguments[0].click();"
                self.driver.driver.execute_script(script, tmp_element)
                self.driver.driver.page_source
                self.click_element(tmp)
                tmp = undetected_chromedriver.WebElement(self.driver.driver, a)
                tmp.click()
                self.driver.driver.execute_script("arguments[0].click();", country_button)
                type(country_button)
                tmp = country_button.xpath(self.tags_chamionship["country"])[0]
                type(tmp)
            except Exception as e:
                scraper_logger.error(
                    f"Failed to click country {country_name} button: {e}"
                )
                continue
            self.get_random_sleep_time()
            country = Country(country_name, country_button)
            competitions = self.extract_competitions(country)
            country.competitions.extend(competitions)
            scraper_logger.info(
                f"Country: Extracted {country_name} country with {len(competitions)} competitions"
            )
            dump_json_data(country, f"instance/countries/{country.name}")
            countries.append(country)
        return countries


def extract_competitions(self, country: Country) -> list[Competition]:
        competitions = []
        competitions_buttons = self.safe_get(self.driver.driver, self.tags_chamionship["championship"])
        competitions_names = self.safe_get(
            country.button, self.tags_chamionship["championship_name"]
        )
        for competition_button, competition_name in zip(competitions_buttons, competitions_names):
            competition_button.click()
            competition = Competition(competition_name)
            matches = self.extract_matches(competition_button)
            competition.matches.extend(matches)
            scraper_logger.info(
                f"Competition: Extracted {competition_name} competition with {len(matches)} matches"
            )
            dump_json_data(competition, f"instance/competitions/{competition.name}")
            competitions.append(competition)
        return competitions


def normalize_teams_name(teams: list) -> list:
    if len(teams)==3:
         return teams
    elif len(teams)==2:
        return [teams[0], "Draw", teams[1]]
        
def extract_matches(self) -> list[Match]:
        """Extract all matches from the competition link

        Args:
            competition_link (str): The competition link

        Returns:
            list[Match]: The list of all matches
        """
        matches = []
        if self.tags_button.get("bet_filter"):
            self.click_on_button(self.tags_button["bet_filter"])
            self.get_random_sleep_time()
        matches_blocs = self.safe_get(self.driver.driver, self.tags_odd["bloc_match"])
        for match_bloc in matches_blocs:
            teams_name = self.safe_get(match_bloc, self.tags_odd["name_team"])
            teams_name = normalize_teams_name(teams_name)
            teams = [Team(team_name.strip()) for team_name in teams_name]
            date_time = self.safe_get(match_bloc, self.tags_odd["date_hours"])
            odds_elements = self.safe_get(match_bloc, self.tags_odd["odd"])
            odds = [Odd(value=v, type=t, team_index=teams.index(e)) for v, t, e in zip(odds_elements, self.data_odd_type, teams)]
            match = Match(teams, date_time, odds)
            matches.append(match)

        return matches


match.to_dict()


# from scrapers.scraper import SiteScraper
# from utils.helpers import load_config_file

# settings = load_config_file("settings.yaml")
# site_name = "parionsport"
# site_config = load_config_file("sites.yaml")[site_name]
# scraper = SiteScraper(site_config, settings)
# url = "https://www.enligne.parionssport.fdj.fr/paris-football/international/coupe-du-monde-f-2023"

# scraper.scrape()
