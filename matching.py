site_A = {
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

"""-----------------------------------------------------"""

from dateutil.parser import parse


def format_dates_recursive(data, date_formats=None, output_format="%d/%m/%Y %H:%M"):
    if date_formats is None:
        date_formats = ["%d/%m/%Y %H:%M", "%d-%m-%Y %H:%M", "%Y-%m-%d %H:%M:%S"]

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                # Vérifier si la valeur est une date
                for date_format in date_formats:
                    try:
                        datetime_obj = parse(value, dayfirst=True, yearfirst=True)
                        # Convertir la date au format spécifié
                        data[key] = datetime_obj.strftime(output_format)
                        break
                    except ValueError:
                        pass
            elif isinstance(value, dict) or isinstance(value, list):
                format_dates_recursive(value, date_formats, output_format)
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], str):
                # Vérifier si la valeur est une date
                for date_format in date_formats:
                    try:
                        datetime_obj = parse(data[i], dayfirst=True, yearfirst=True)
                        # Convertir la date au format spécifié
                        data[i] = datetime_obj.strftime(output_format)
                        break
                    except ValueError:
                        pass
            elif isinstance(data[i], dict) or isinstance(data[i], list):
                format_dates_recursive(data[i], date_formats, output_format)


# Exemple d'utilisation avec le dictionnaire site_A
site_A = {
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
        # Autres matchs...
    ],
}

# Appel de la fonction pour mettre les dates au même format
format_dates_recursive(site_A)

# Affichage du dictionnaire site_A avec les dates formatées
print(site_A)


"""-----------------------------------------------------"""


def replace_draw_with_n_recursive(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = (
                    value.replace("DRAW", "N", -1)
                    .replace("Draw", "N", -1)
                    .replace("draw", "N", -1)
                )
            elif isinstance(value, dict) or isinstance(value, list):
                replace_draw_with_n_recursive(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], str):
                data[i] = (
                    data[i]
                    .replace("DRAW", "N", -1)
                    .replace("Draw", "N", -1)
                    .replace("draw", "N", -1)
                )
            elif isinstance(data[i], dict) or isinstance(data[i], list):
                replace_draw_with_n_recursive(data[i])


# Exemple d'utilisation avec le dictionnaire site_A

# Appel de la fonction pour remplacer "DRAW" par "N" (indépendamment de la casse)
replace_draw_with_n_recursive(site_A)

# Affichage du dictionnaire site_A après le remplacement
print(site_A)


"""-------------------------------------------------------"""


def find_similar_matches(site_A, site_B, similarity_threshold=0.13):
    similar_matches = {}

    championship_similarity = difflib.SequenceMatcher(
        None, site_A["name"], site_B["name"]
    ).ratio()

    if championship_similarity < similarity_threshold:
        print("Les championnats ne sont pas similaires.")
        return

    for match_A in site_A["matches"]:
        for match_B in site_B["matches"]:
            teams_similarity = difflib.SequenceMatcher(
                None, match_A["teams"], match_B["teams"]
            ).ratio()

            date_time_similarity = difflib.SequenceMatcher(
                None, match_A["date_time"], match_B["date_time"]
            ).ratio()

            if (
                teams_similarity > similarity_threshold
                and date_time_similarity > similarity_threshold
            ):
                similar_matches[match_A["teams"]] = {
                    "championship": site_A["name"],
                    "date_time": match_A["date_time"],
                    "odds_site_A": match_A["odds"],
                    "odds_site_B": match_B["odds"],
                }

    return similar_matches


# Utilisation de la fonction pour trouver les matchs similaires entre site_A et site_B
similar_matches = find_similar_matches(site_A, site_B)

# Affichage des résultats
for teams, odds in similar_matches.items():
    print("Championnat:", odds["championship"])
    print("Match:", teams)
    print("Date et heure:", odds["date_time"])
    print("Côtes du site A:", odds["odds_site_A"])
    print("Côtes du site B:", odds["odds_site_B"])
    print("------------------------")
