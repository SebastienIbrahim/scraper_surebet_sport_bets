# Sports Betting Odds Scraping Project

This README file provides a general overview of the sports betting odds scraping project. The project is organized into multiple folders and files, each serving a specific purpose. Below is an overview of the various components of the project.

# Project Structure
The project is structured as follows:

## Main Folders

config: Contains YAML configuration files for project settings.
  settings.yaml: Main configuration file for project settings.
  sites.yaml: Configuration file for target websites.
  
find_surebet: Contains Python files for finding surebets.
  countries_matching.py: Module for country matching.
  display_surbet.py: Module for displaying surebets.
  find_surbet.py: Main module for finding surebets.
  
instance: Contains instant data generated by the project.
  competitions: Contains JSON files with competition data.
  countries: Contains JSON files with country data.
  organize.py: Script for organizing generated data.
  
logs: Contains project log files.
  captcha.log: Log for captchas.  
  errors.log: Log for errors.
  scraper.log: Log for scraping.
  
models: Contains Python files for data models.
  competition.py: Model for sports competitions.
  country.py: Model for countries.
  match.py: Model for sports matches.
  sport.py: Model for sports.
  team_odd.py: Model for team odds.
  
organized: Contains organized data by date.
  competitions: Contains JSON files organized by date for competitions.
  countries: Contains JSON files organized by date for countries.
  sports: Contains JSON files organized by date for sports.
  
scrapers: Contains Python files for scrapers.
  base_scraper.py: Base module for scrapers.
  scraper.py: Main module for scrapers.
  
utils: Contains Python utilities for the project.
  helpers.py: Utility functions.
  logger.py: Logging module.
  
# Main Files

debug.py: Python file for debugging the project.
Football.html: HTML file.
LICENSE: Project license.
main.py: Main entry point for the project.
matchig.json: JSON file.
matching_bookmakers.py: Module for matching bookmakers.
README.md: This README file.
requirements.txt: List of required Python dependencies for the project.
run2.py: Script for running the project.
matching_bookmakers.cpython-39.pyc: Cache file for a Python module.

# Using the Project
Ensure you have the required dependencies installed by running pip install -r requirements.txt.

Configure project settings in the config/settings.yaml file according to your needs.

Execute the project using python main.py.

Scraped data will be stored in the instance folder.

You can use the matching, displaying, and surebet finding modules to analyze the generated data.

Feel free to explore the different files and folders to learn more about each component of the project. If you have questions or encounter issues, check the logs in the logs folder for error information.
