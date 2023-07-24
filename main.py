from scrapers.scraper import SiteScraper
from utils.helpers import load_config_file

settings = load_config_file("settings.yaml")
site_name = "betclic"
site_config = load_config_file("sites.yaml")[site_name]
scraper = SiteScraper(site_name, site_config, settings)
scraper.scrape()
