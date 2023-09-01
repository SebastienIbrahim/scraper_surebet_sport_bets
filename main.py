from scrapers.scraper import SiteScraper
from pathlib import Path
from utils.helpers import load_config_file
from matching_bookmakers import find_similar_matches
from find_surebet.countries_matching import (
    get_matched_countries,
    get_data_from_matched_countries_per_site,
)
from find_surebet.find_surbet import find_surbets_opportunities

settings = load_config_file("settings.yaml")
site_config = load_config_file("sites.yaml")
sites_name = list(site_config.keys())


def main(sites_name, raw_data_path="instance"):
    for site_name in sites_name:
        print(f"Crawl web site: {site_name}")
        SiteScraper(site_name, site_config[site_name], settings).scrape()
    root_dir = Path(__file__).parent / raw_data_path
    print(f"Root directory: {root_dir}")
    matched_countries, not_matched_countries = get_matched_countries(
        root_directory=root_dir, site_number=len(sites_name)
    )
    comptetions_data = get_data_from_matched_countries_per_site(
        matched_countries, not_matched_countries
    )
    similarity_threshold = settings["similarity_threshold"]
    similar_matches = find_similar_matches(comptetions_data, similarity_threshold)
    opportunities = find_surbets_opportunities(
        similar_matches, investissement_amount=100, nb_way=3, draw_position=1
    )
    print(opportunities)


if __name__ == "__main__":
    main(sites_name)
