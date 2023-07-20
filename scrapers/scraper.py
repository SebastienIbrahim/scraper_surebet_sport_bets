from bs4 import BeautifulSoup
from models.sport import Sport
from models.country import Country
from models.competition import Competition
from models.match import Match
from models.team_odd import Team, Odd
from utils.logger import setup_scraper_logger, setup_error_logger, setup_captcha_logger
from utils.helpers import dump_json_data
from scrapers.base_scraper import BaseScraper
from lxml import etree

scraper_logger, error_logger, captcha_logger = (
    setup_scraper_logger(),
    setup_error_logger(),
    setup_captcha_logger(),
)


class SiteScraper(BaseScraper):
    def __init__(self, site_config, settings):
        super().__init__(site_config, settings)

    def scrape(self) -> list[dict]:
        """Scrape the website

        Returns:
            list[dict]: The list of all sports per country per competition per match per date
        """
        home_page = self.get_page(self.home_page)
        self.accept_cookies(self.tags_button["cookies"])
        self.get_random_sleep_time()
        sports = self.extract_sports(home_page)
        for sport in sports:
            dump_json_data(sport, f"instance/sports/{sport.name}")

    def extract_sports(self, home_page: BeautifulSoup) -> list[Sport]:
        """Extract all sports from the home page
        Args:
            home_page (str): The home page of the website to scrape

        Returns:
            list[Sport]: The list of all sports
        """
        sports = []
        sports_blocs = self.safe_get(home_page, self.tags_chamionship["sport"])
        sports_name = self.safe_get(home_page, self.tags_chamionship["sport_name"])
        for sport_bloc, sport_name in zip(sports_blocs, sports_name):
            sport = Sport(sport_name, sport_bloc)
            countries = self.extract_countries(sport)
            sport.countries.extend(countries)
            scraper_logger.info(
                f"Extracted {sport_name} sport with {len(countries)} countries"
            )
            sports.append(sport)
        return sports

    def extract_countries(self, sport: Sport) -> list[Country]:
        countries = []
        countries_names = self.safe_get(
            sport.bloc, self.tags_chamionship["country_name"]
        )
        for country_name in countries_names:
            country = Country(country_name)
            competitions = self.extract_competitions(sport)
            country.competitions.extend(competitions)
            scraper_logger.info(
                f"Extracted {country_name} country with {len(competitions)} competitions"
            )
            dump_json_data(country, f"instance/countries/{country.name}")
            countries.append(country)
        return countries

    def extract_competitions(self, sport: Sport) -> list[Competition]:
        competitions = []
        competitions_links = [
            self.normalize_url(url)
            for url in self.safe_get(
                sport.bloc, self.tags_chamionship["link_championship"]
            )
        ]
        competitions_names = self.safe_get(
            sport.bloc, self.tags_chamionship["championship_name"]
        )
        for competition_link, competition_name in zip(
            competitions_links, competitions_names
        ):
            competition = Competition(competition_name)
            matches = self.extract_matches(competition_link)
            competition.matches.extend(matches)
            scraper_logger.info(
                f"Extracted {competition_name} competition with {len(matches)} matches"
            )
            dump_json_data(competition, f"instance/competitions/{competition.name}")
            competitions.append(competition)
        return competitions

    def extract_matches(self, competition_link: str) -> list[Match]:
        """Extract all matches from the competition link

        Args:
            competition_link (str): The competition link

        Returns:
            list[Match]: The list of all matches
        """
        matches = []
        match_page = self.get_page(competition_link)
        self.get_random_sleep_time()
        if self.tags_button.get("bet_filter"):
            self.click_on_button(self.tags_button["bet_filter"])
            self.get_random_sleep_time()
            match_page = BeautifulSoup(self.driver.driver.page_source, "html.parser")
        matches_blocs = self.safe_get(match_page, self.tags_odd["bloc_match"])
        data_odd_type = self.data_odd_type
        for match_bloc in matches_blocs:
            teams_name = self.safe_get(match_bloc, self.tags_odd["name_team"])
            teams = [Team(team_name) for team_name in teams_name]
            date_time = self.safe_get(match_bloc, self.tags_odd["date_hours"])
            odds_elements = self.safe_get(match_bloc, self.tags_odd["odd"])
            odds = [Odd(value=v, type=t) for v, t in zip(odds_elements, data_odd_type)]
            match = Match(teams, date_time, odds)
            matches.append(match)

        return matches
