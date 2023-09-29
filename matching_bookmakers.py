import difflib
from dateutil.parser import parse


site_A = {
    "Bookmaker": "Betclic",
    "name": "Angl. Premier League",
    "matches": [
        {
            "teams": "Burnley vs Draw vs Manchester City",
            "date_time": "11/08/2023 21:00",
            "odds": {
                "Burnley - Win": "7,85",
                "Draw": "4,90",
                "Manchester City - Win": "1,29",
            },
        },
        {
            "teams": "Arsenal vs Draw vs Nottingham Forest",
            "date_time": "12/08/2023 13:30",
            "odds": {
                "Arsenal - Win": "1,24",
                "Draw": "5,40",
                "Nottingham Forest - Win": "8,45",
            },
        },
        {
            "teams": "Bournemouth vs Draw vs West Ham",
            "date_time": "12/08/2023 16:00",
            "odds": {
                "Bournemouth - Win": "2,72",
                "Draw": "3,20",
                "West Ham - Win": "2,32",
            },
        },
        {
            "teams": "Brighton vs Draw vs Luton",
            "date_time": "12/08/2023 16:00",
            "odds": {"Brighton - Win": "1,29", "Draw": "4,80", "Luton - Win": "7,75"},
        },
        {
            "teams": "Sheffield Utd vs Draw vs Crystal Palace",
            "date_time": "12/08/2023 16:00",
            "odds": {
                "Sheffield Utd - Win": "2,80",
                "Draw": "3,10",
                "Crystal Palace - Win": "2,32",
            },
        },
        {
            "teams": "Everton vs Draw vs Fulham",
            "date_time": "12/08/2023 16:00",
            "odds": {"Everton - Win": "2,12", "Draw": "3,25", "Fulham - Win": "3,05"},
        },
        {
            "teams": "Newcastle vs Draw vs Aston Villa",
            "date_time": "12/08/2023 18:30",
            "odds": {
                "Newcastle - Win": "1,64",
                "Draw": "3,70",
                "Aston Villa - Win": "4,35",
            },
        },
        {
            "teams": "Brentford vs Draw vs Tottenham",
            "date_time": "13/08/2023 15:00",
            "odds": {
                "Brentford - Win": "2,82",
                "Draw": "3,30",
                "Tottenham - Win": "2,22",
            },
        },
        {
            "teams": "Chelsea vs Draw vs Liverpool",
            "date_time": "13/08/2023 17:30",
            "odds": {
                "Chelsea - Win": "2,72",
                "Draw": "3,35",
                "Liverpool - Win": "2,25",
            },
        },
        {
            "teams": "Manchester Utd vs Draw vs Wolverhampton",
            "date_time": "14/08/2023 21:00",
            "odds": {
                "Manchester Utd - Win": "1,33",
                "Draw": "4,65",
                "Wolverhampton - Win": "7,00",
            },
        },
    ],
}

site_B = {
    "Bookmaker": "Parions Sport",
    "name": "Premier League",
    "matches": [
        {
            "teams": "Burnley vs N vs Man. City",
            "date_time": "vendredi 11 août à 21h00",
            "odds": {
                "Burnley - Win": "7,70",
                "Draw": "4,80",
                "Man. City - Win": "1,28",
            },
        },
        {
            "teams": "Arsenal vs N vs Nottingham F.",
            "date_time": "samedi 12 août à 13h30",
            "odds": {
                "Arsenal - Win": "1,23",
                "Draw": "5,30",
                "Nottingham F. - Win": "8,30",
            },
        },
        {
            "teams": "Sheffield Utd vs N vs Crystal Palace",
            "date_time": "samedi 12 août à 16h00",
            "odds": {
                "Sheffield Utd - Win": "2,80",
                "Draw": "3,05",
                "Crystal Palace - Win": "2,30",
            },
        },
        {
            "teams": "Bournemouth vs N vs West Ham",
            "date_time": "samedi 12 août à 16h00",
            "odds": {
                "Bournemouth - Win": "2,70",
                "Draw": "3,15",
                "West Ham - Win": "2,30",
            },
        },
        {
            "teams": "Everton vs N vs Fulham",
            "date_time": "samedi 12 août à 16h00",
            "odds": {"Everton - Win": "2,10", "Draw": "3,25", "Fulham - Win": "3,00"},
        },
        {
            "teams": "Brighton Hove vs N vs Luton Town",
            "date_time": "samedi 12 août à 16h00",
            "odds": {
                "Brighton Hove - Win": "1,29",
                "Draw": "4,70",
                "Luton Town - Win": "7,60",
            },
        },
        {
            "teams": "Newcastle vs N vs Aston Villa",
            "date_time": "samedi 12 août à 18h30",
            "odds": {
                "Newcastle - Win": "1,63",
                "Draw": "3,65",
                "Aston Villa - Win": "4,30",
            },
        },
        {
            "teams": "Brentford vs N vs Tottenham",
            "date_time": "dimanche 13 août à 15h00",
            "odds": {
                "Brentford - Win": "2,80",
                "Draw": "3,25",
                "Tottenham - Win": "2,20",
            },
        },
        {
            "teams": "Chelsea vs N vs Liverpool",
            "date_time": "dimanche 13 août à 17h30",
            "odds": {
                "Chelsea - Win": "2,70",
                "Draw": "3,30",
                "Liverpool - Win": "2,25",
            },
        },
        {
            "teams": "Man. United vs N vs Wolverhampton",
            "date_time": "lundi 14 août à 21h00",
            "odds": {
                "Man. United - Win": "1,32",
                "Draw": "4,60",
                "Wolverhampton - Win": "6,80",
            },
        },
    ],
}

site_C = {
    "Bookmaker": "bet365",
    "championship": "Ligue 1",
    "matches": [
        {
            "teams": "Paris Saint-Germain vs Marseille",
            "date_time": "01/09/2023 20:00",
            "odds": {
                "Paris Saint-Germain - Win": "1.50",
                "Draw": "4.00",
                "Marseille - Win": "6.50",
            },
        },
        {
            "teams": "Lyon vs Monaco",
            "date_time": "02/09/2023 15:00",
            "odds": {
                "Lyon - Win": "2.10",
                "Draw": "3.50",
                "Monaco - Win": "3.80",
            },
        },
    ],
}

site_D = {
    "Bookmaker": "Unibet",
    "championship": "Ligue 1",
    "matches": [
        {
            "teams": "Paris SG vs Marseille",
            "date_time": "01/09/2023 20:00",
            "odds": {
                "Paris SG - Win": "1.55",
                "Draw": "3.90",
                "Marseille - Win": "7.00",
            },
        },
        {
            "teams": "Olympique Lyonnais vs AS Monaco",
            "date_time": "02/09/2023 15:00",
            "odds": {
                "Olympique Lyonnais - Win": "2.05",
                "Draw": "3.60",
                "AS Monaco - Win": "3.75",
            },
        },
    ],
}


"""-----------------------------------------------------"""


import re
import datetime
from dateutil.parser import parse

from typing import Optional
import dateparser


def convert_date_to_dd_mm_yyyy_hh_mm(text: str) -> Optional[str]:
    """
    Converts a date string to the format "dd/mm/yyyy hh:mm".

    Args:
        text (str): A date string.
        current_date (datetime): The current date for relative date parsing.

    Returns:
        Optional[str]: The converted date string, or None if parsing fails.
    """
    # Try to parse the date using dateparser
    date = dateparser.parse(text)

    if date:
        return date.strftime("%d/%m/%Y %H:%M")
    else:
        return None  # Unable to parse the date


# Fonction pour formater les chaînes de date et d'heure
def format_date(date_str, time_format="%H:%M"):
    mois = {
        "janvier": 1,
        "février": 2,
        "mars": 3,
        "avril": 4,
        "mai": 5,
        "juin": 6,
        "juillet": 7,
        "août": 8,
        "septembre": 9,
        "octobre": 10,
        "novembre": 11,
        "décembre": 12,
    }
    # Vérifier si la date est au format "jj/mm/aaaa hh:mm"
    if re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}", date_str):
        parties = date_str.split()
        jour, mois, année = map(int, parties[0].split("/"))
        heure, minute = map(int, parties[1].split(":"))
    else:
        # Utiliser des expressions régulières pour extraire les composantes de la date et de l'heure
        correspondance = re.match(
            r"(.+) (\d{1,2}) (\w+) (?:à|at) (\d{1,2})h(\d{2})", date_str
        )
        jour = int(correspondance.group(2))
        mois = mois[correspondance.group(3)]
        année = datetime.datetime.now().year  # Utiliser l'année en cours
        heure = int(correspondance.group(4))
        minute = int(correspondance.group(5))

    # Renvoyer la date et l'heure formatées
    return (
        f"{jour:02d}/{mois:02d}/{année} {heure:02d}:{minute:02d}"
        if time_format == "%H:%M"
        else f"{jour:02d}/{mois:02d}/{année} {heure}h{minute:02d}"
    )


# Fonction pour formater les dates dans un dictionnaire
def format_dates_in_dictionary(input_dict, time_format="%H:%M"):
    output_dict = input_dict.copy()
    for match in output_dict["matches"]:
        try:
            match["date_time"] = convert_date_to_dd_mm_yyyy_hh_mm(match["date_time"])
        except Exception as e:
            print(f"Failed to format date: {e}")
            continue
    return output_dict


# Fonction pour remplacer le nom d'une clé dans un dictionnaire de manière récursive
def remplace_nom_clé_récursif(input_dict, ancienne_clé, nouvelle_clé):
    output_dict = {}
    for clé, valeur in input_dict.items():
        if isinstance(valeur, dict):
            output_dict[clé] = remplace_nom_clé_récursif(
                valeur, ancienne_clé, nouvelle_clé
            )
        else:
            output_dict[clé if clé != ancienne_clé else nouvelle_clé] = valeur
    return output_dict


# Fonction pour supprimer le suffixe "- Win" des clés de cotes dans un dictionnaire de manière récursive
def supprime_suffixe_win_récursif(input_dict):
    output_dict = {}
    for clé, valeur in input_dict.items():
        if isinstance(valeur, dict):
            if clé == "odds":
                nouvelles_cotes = {
                    k.replace(" - Win", ""): v for k, v in valeur.items()
                }
                output_dict[clé] = nouvelles_cotes
            else:
                output_dict[clé] = supprime_suffixe_win_récursif(valeur)
        elif isinstance(valeur, list):
            output_dict[clé] = [supprime_suffixe_win_récursif(item) for item in valeur]
        else:
            output_dict[clé] = valeur
    return output_dict


# Fonction pour nettoyer les noms d'équipes en supprimant "vs", "N" et "Draw"
def nettoie_noms_equipes(input_dict):
    output_dict = input_dict.copy()
    for match in output_dict["matches"]:
        try:
            equipes = match["teams"]
            equipes_propres = equipes.replace("vs N ", " ").replace("vs Draw ", " ")
            match["teams"] = equipes_propres
        except Exception as e:
            print(f"Failed to clean team names: {e}")
            continue
    return output_dict


def traiter_dictionnaire(input_dict):
    site_formatte = format_dates_in_dictionary(input_dict)
    site_renommé = remplace_nom_clé_récursif(site_formatte, "name", "championship")
    site_sans_win = supprime_suffixe_win_récursif(site_renommé)
    site_noms_propres = nettoie_noms_equipes(site_sans_win)
    return site_noms_propres


# Utilisation de la fonction pour traiter les dictionnaires site_A et site_B
site_A_traite = traiter_dictionnaire(site_A)
site_B_traite = traiter_dictionnaire(site_B)
site_C_traite = traiter_dictionnaire(site_C)
site_D_traite = traiter_dictionnaire(site_D)

sites = [site_A_traite, site_B_traite, site_C_traite, site_D_traite]
# Afficher les dictionnaires traités
print("Site A traité:")
print(site_A_traite)
print("\nSite B traité:")
print(site_B_traite)


"""-------------------------------------------------------"""
import difflib


def process_team_name(team_name):
    # TODO: Normalize team name by removing stop words and accents
    # Split team name by spaces and convert to lowercase
    parts = [team.strip() for team in team_name.lower().split(" vs ")]
    return parts


def calculate_team_similarity(team_a_parts, team_b_parts):
    # Calculate the average similarity between the parts of two team names
    total_similarity = sum(
        difflib.SequenceMatcher(None, a, b).ratio()
        for a in team_a_parts
        for b in team_b_parts
    )
    avg_similarity = total_similarity / (len(team_a_parts) * len(team_b_parts))
    return avg_similarity


def find_similar_matches(sites, similarity_threshold=0.13):
    similar_matches = {}

    for i, site_A in enumerate(sites):
        championship_A = site_A["championship"]
        if championship_A not in similar_matches:
            similar_matches[championship_A] = {}

        for j, site_B in enumerate(sites):
            if i >= j:
                continue  # Skip combinations we've already processed or self-combinations
            championship_B = site_B["championship"]
            for match_A in site_A["matches"]:
                teams_A = process_team_name(match_A["teams"])
                for match_B in site_B["matches"]:
                    teams_B = process_team_name(match_B["teams"])

                    teams_similarity = calculate_team_similarity(teams_A, teams_B)
                    try:
                        date_time_similarity = difflib.SequenceMatcher(
                            None, match_A["date_time"], match_B["date_time"]
                        ).ratio()
                    except Exception as e:
                        continue
                    championship_similarity = difflib.SequenceMatcher(
                        None, championship_A, championship_B
                    ).ratio()

                    if (
                        teams_similarity > similarity_threshold
                        and date_time_similarity > similarity_threshold
                        and championship_similarity > similarity_threshold
                    ):
                        match_key = match_A["teams"]
                        if match_key not in similar_matches[championship_A]:
                            similar_matches[championship_A][match_key] = []

                        similar_match = {
                            site_A["Bookmaker"]: {
                                "odds": match_A["odds"],
                                "date": match_A["date_time"],
                            },
                            site_B["Bookmaker"]: {
                                "odds": match_B["odds"],
                                "date": match_B["date_time"],
                            },
                        }
                        similar_matches[championship_A][match_key].append(similar_match)
    return {k: v for k, v in similar_matches.items() if len(v) > 1}


# Utilisation de la fonction pour trouver les matchs similaires entre site_A et site_B
similar_matches = find_similar_matches(
    [site_A_traite, site_B_traite, site_C_traite, site_D_traite],
    similarity_threshold=0.43,
)


for championship, matches in similar_matches.items():
    print(f"========= Championship: {championship} =========")
    for match, odds in matches.items():
        print(f"Match: {match}")
        for site, odds in odds[0].items():
            print(f"Site: {site}")
            print(f"Odds: {odds}")
        print("------------------------")
