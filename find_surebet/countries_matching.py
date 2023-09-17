import os
import re
from pathlib import Path
import yaml
from unidecode import unidecode
from nltk.corpus import stopwords
from googletrans import Translator
import json
from matching_bookmakers import traiter_dictionnaire


def get_countries_names(root_directory):
    # Dictionnaire pour stocker les noms de pays par site
    countries_by_site = {}
    all_countries = set()
    # Parcourir tous les fichiers de compétition
    for site_name in ["betclic", "parionsport"]:
        site_directory = os.path.join(root_directory, site_name)
        if os.path.isdir(site_directory):
            countries = set()
            for subdir, _, files in os.walk(os.path.join(site_directory, "countries")):
                for file_name in files:
                    if file_name.endswith(".json"):
                        parts = file_name.split("@")
                        if len(parts) >= 2:
                            country_name = parts[1].split("_")[0]
                            countries.add(country_name)
                            all_countries.add(country_name)
            countries_by_site[site_name] = list(countries)
    return countries_by_site


def convert_country_name_to_english(country_name, src="fr", target_lang="en"):
    translator = Translator()
    translated = translator.translate(country_name, src=src, dest=target_lang)
    return translated.text


# Fonction pour normaliser un nom de pays
def normalize_country(country_name):
    stop_words = set(stopwords.words("french") + stopwords.words("english"))
    normalized = unidecode(country_name.lower())
    words = re.findall(r"\w+", normalized)
    words = [word for word in words if word not in stop_words]
    return " ".join(words)


def load_config_file(filename: str) -> dict[str, str]:
    """Load a YAML config file.
    Args:
        filename (str): The name of the file to load.
        Returns:
            dict: The configuration data.
    """
    path = Path(__file__).parent.parent / "config" / filename
    try:
        with open(f"{path}", "r") as file:
            config_data = yaml.safe_load(file)
            return config_data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {filename} was not found.")


def match_countries_by_site(root_dir):
    country_site_files = {}

    site_dirs = [
        d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))
    ]

    for site_dir in site_dirs:
        site_path = os.path.join(root_dir, site_dir)
        countries_dir = os.path.join(site_path, "countries")

        if not os.path.exists(countries_dir):
            continue

        for country_file in os.listdir(countries_dir):
            if country_file.endswith(".json"):
                country_name = country_file.split("@")[1].split("_")[0]
                country_name_normalized = normalize_country(country_name)
                country_file_path = os.path.join(countries_dir, country_file)

                if country_name_normalized in country_site_files:
                    site_data = country_site_files[country_name_normalized]
                    if site_dir in site_data:
                        site_data[site_dir].append(country_file_path)
                    else:
                        site_data[site_dir] = [country_file_path]
                else:
                    country_site_files[country_name_normalized] = {
                        site_dir: [country_file_path]
                    }
    # Tri des fichiers par date dans l'ordre décroissant pour chaque site
    for country, site_data in country_site_files.items():
        for site, files in site_data.items():
            files.sort(key=lambda f: os.path.getmtime(f), reverse=True)

    return country_site_files


def open_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def get_matched_countries(root_directory, site_number=2):
    country_site_files = match_countries_by_site(root_directory)
    matched_countries = {}
    not_matched_countries = {}
    for country in country_site_files.keys():
        if len(country_site_files[country].keys()) >= site_number:
            matched_countries[country] = country_site_files[country]
        else:
            not_matched_countries[country] = country_site_files[country]
    return matched_countries, not_matched_countries


def get_data_from_matched_countries_per_site(matched_countries, not_matched_countries):
    union_matched_not_matched = {**matched_countries, **not_matched_countries}
    all_data = []
    for country, site_data in union_matched_not_matched.items():
        for site, files in site_data.items():
            for file in files:
                country_data = open_json_file(file)
                for competition_data in country_data["competitions"]:
                    competition_data["Bookmaker"] = site
                    if len(competition_data["matches"]) < 1:
                        continue
                    all_data.append(competition_data)
    all_data = [traiter_dictionnaire(data) for data in all_data]
    return all_data
