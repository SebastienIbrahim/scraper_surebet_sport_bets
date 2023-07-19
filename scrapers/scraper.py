import requests
from bs4 import BeautifulSoup
import time
import random
from models.sport import Sport
from models.country import Country
from models.competition import Competition
from models.match import Match
from models.team_odd import Team, Odd
from utils.logger import setup_scraper_logger, setup_error_logger, setup_captcha_logger
from utils.helpers import load_config_file
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

    def scrape(self):
        home_page = self.get_page(self.home_page)
        self.accept_cookies(self.tags_button["cookies"])
        self.get_random_sleep_time()
        sports = self.extract_sports(home_page)
        for sport in sports:
            scraper_logger.info(sport.name)
            countries = self.extract_countries(sport)
            for contry in countries:
                scraper_logger.info(contry.name)
                competitions = self.extract_competitions(sport)
                for competition in competitions:
                    scraper_logger.info(competition.name)
                    matches = self.extract_matches(competition)
                    for match in matches:
                        scraper_logger.info(match)
                        # TODO: continue to implement the scraper

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
            competitions.append(competition)
        return competitions

    def extract_matches(self, competition_link):
        matches = [Match("test", "test")]
        return matches

    def extract_matches_day(self, day_tag):
        matches = []
        for match_tag in day_tag.select(self.tags["match"]):
            teams = self.get_teams(match_tag)
            date_time = self.get_date_time(match_tag)
            match = Match(teams, date_time)
            matches.append(match)
        return matches

    def extract_teams(self, match_tag):
        teams = []
        for team_tag in match_tag.select(self.tags["team"]):
            team_name = self.get_tag_text(team_tag, self.tags["team_name"])
            team = Team(team_name)
            teams.append(team)
        return teams

    def extract_odds(self, match_tag):
        odds = []
        for odd_tag in match_tag.select(self.tags["odd"]):
            odd_name = self.get_tag_text(odd_tag, self.tags["odd_name"])
            odd = Odd(odd_name)
            odds.append(odd)
        return odds
