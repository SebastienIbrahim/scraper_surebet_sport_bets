from scrapers.scraper import SiteScraper
from pathlib import Path
from utils.helpers import load_config_file
from matching_bookmakers import find_similar_matches
import time
from find_surebet.countries_matching import (
    get_matched_countries,
    get_data_from_matched_countries_per_site,
)
from find_surebet.find_surbet import find_surbets_opportunities

settings = load_config_file("settings.yaml")
site_config = load_config_file("sites.yaml")
sites_name = list(site_config.keys())
raw_data_path = "instance"


def main(sites_name, raw_data_path="instance"):
    for site_name in sites_name:
        print(f"Crawl web site: {site_name}")
        SiteScraper(site_name, site_config[site_name], settings).scrape()
    root_dir = Path(__file__).parent / raw_data_path
    print(f"Root directory: {root_dir}")
    data_matches = {}
    matched_countries, not_matched_countries = get_matched_countries(
        root_directory=root_dir, site_number=len(sites_name)
    )
    comptetions_data = get_data_from_matched_countries_per_site(
        matched_countries, not_matched_countries
    )
    data_list = [
        item
        for item in comptetions_data
        if "matches" in item and all(match.get("teams") for match in item["matches"])
    ]

    similarity_threshold = settings["similarity_threshold"]
    t0 = time.time()
    similar_matches = find_similar_matches(data_list, similarity_threshold)
    t1 = time.time()
    print(f"Time to find similar matches: {(t1-t0)/60} minutes")
    len(similar_matches.keys())
    for match in similar_matches.values():
        data_matches.update(match)
    len(data_matches.keys())
    opportunities = find_surbets_opportunities(
        data_matches, investissement_amount=100, nb_way=3, draw_position=1
    )
    print(opportunities)


if __name__ == "__main__":
    main(sites_name)
