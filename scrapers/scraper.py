import requests
from bs4 import BeautifulSoup
import time
import random
from utils.logger import setup_scraper_logger, setup_error_logger, setup_captcha_logger
from utils.helpers import load_config_file
from scrapers.base_scraper import BaseScraper


class SiteScraper(BaseScraper):
    def __init__(self, site_config, settings):
        super().__init__(site_config, settings)

    def scrape(self):
        page_content = self.fetch_page()
        if page_content:
            soup = self.parse_page(page_content)
            sports = self.extract_sports(soup)
            return sports
        return []

    def extract_sports(self, soup):
        sports = []
        for sport_tag in soup.select(self.tags["sport"]):
            sport_name = self.get_tag_text(sport_tag, self.tags["sport_name"])
            sport = Sport(sport_name)
            countries = self.extract_countries(sport_tag)
            sport.countries.extend(countries)
            sports.append(sport)
        return sports

    def extract_countries(self, sport_tag):
        countries = []
        for country_tag in sport_tag.select(self.tags["country"]):
            country_name = self.get_tag_text(country_tag, self.tags["country_name"])
            country = Country(country_name)
            competitions = self.extract_competitions(country_tag)
            country.competitions.extend(competitions)
            countries.append(country)
        return countries

    def extract_competitions(self, country_tag):
        competitions = []
        for competition_tag in country_tag.select(self.tags["competition"]):
            competition_name = self.get_tag_text(
                competition_tag, self.tags["competition_name"]
            )
            competition = Competition(competition_name)
            matches = self.extract_matches(competition_tag)
            competition.matches.extend(matches)
            competitions.append(competition)
        return competitions

    def extract_matches(self, competition_tag):
        matches = []
        for match_tag in competition_tag.select(self.tags["match"]):
            teams = self.get_teams(match_tag)
            date_time = self.get_date_time(match_tag)
            match = Match(teams, date_time)
            matches.append(match)
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
