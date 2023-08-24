def display_info(label, data):
    print(label + ":")
    for key, value in data.items():
        print(f"\t{key}: {value} (Bookmaker {key.split()[-1]})")


data = {
    "Burnley  vs Manchester City": [
        {
            "Betclic": {
                "odds": {"Burnley": "7,85", "Draw": "4,90", "Manchester City": "1,29"}
            },
            "Parions Sport": {
                "odds": {"Burnley": "7,70", "Draw": "4,80", "Man. City": "1,28"}
            },
        }
    ],
    "Arsenal  vs Nottingham Forest": [
        {
            "Betclic": {
                "odds": {"Arsenal": "1,24", "Draw": "5,40", "Nottingham Forest": "8,45"}
            },
            "Parions Sport": {
                "odds": {"Arsenal": "1,23", "Draw": "5,30", "Nottingham F.": "8,30"}
            },
        }
    ],
    "Bournemouth  vs West Ham": [
        {
            "Betclic": {
                "odds": {"Bournemouth": "2,72", "Draw": "3,20", "West Ham": "2,32"}
            },
            "Parions Sport": {
                "odds": {"Bournemouth": "2,70", "Draw": "3,15", "West Ham": "2,30"}
            },
        }
    ],
    "Brighton  vs Luton": [
        {
            "Betclic": {"odds": {"Brighton": "1,29", "Draw": "4,80", "Luton": "7,75"}},
            "Parions Sport": {
                "odds": {"Brighton Hove": "1,29", "Draw": "4,70", "Luton Town": "7,60"}
            },
        }
    ],
    "Sheffield Utd  vs Crystal Palace": [
        {
            "Betclic": {
                "odds": {
                    "Sheffield Utd": "2,80",
                    "Draw": "3,10",
                    "Crystal Palace": "2,32",
                }
            },
            "Parions Sport": {
                "odds": {
                    "Sheffield Utd": "2,80",
                    "Draw": "3,05",
                    "Crystal Palace": "2,30",
                }
            },
        }
    ],
    "Everton  vs Fulham": [
        {
            "Betclic": {"odds": {"Everton": "2,12", "Draw": "3,25", "Fulham": "3,05"}},
            "Parions Sport": {
                "odds": {"Everton": "2,10", "Draw": "3,25", "Fulham": "3,00"}
            },
        }
    ],
    "Newcastle  vs Aston Villa": [
        {
            "Betclic": {
                "odds": {"Newcastle": "1,64", "Draw": "3,70", "Aston Villa": "4,35"}
            },
            "Parions Sport": {
                "odds": {"Newcastle": "1,63", "Draw": "3,65", "Aston Villa": "4,30"}
            },
        }
    ],
    "Brentford  vs Tottenham": [
        {
            "Betclic": {
                "odds": {"Brentford": "2,82", "Draw": "3,30", "Tottenham": "2,22"}
            },
            "Parions Sport": {
                "odds": {"Brentford": "2,80", "Draw": "3,25", "Tottenham": "2,20"}
            },
        }
    ],
    "Chelsea  vs Liverpool": [
        {
            "Betclic": {
                "odds": {"Chelsea": "2,72", "Draw": "3,35", "Liverpool": "2,25"}
            },
            "Parions Sport": {
                "odds": {"Chelsea": "2,70", "Draw": "3,30", "Liverpool": "2,25"}
            },
        }
    ],
    "Manchester Utd  vs Wolverhampton": [
        {
            "Betclic": {
                "odds": {
                    "Manchester Utd": "1,33",
                    "Draw": "4,65",
                    "Wolverhampton": "7,00",
                }
            },
            "Parions Sport": {
                "odds": {"Man. United": "1,32", "Draw": "4,60", "Wolverhampton": "6,80"}
            },
        }
    ],
}


def find_surebets(data, total_stake):
    surebets = {}

    for match, bookmakers_list in data.items():
        n = len(bookmakers_list)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    bookmaker_a, data_a = list(bookmakers_list[i].items())[0]
                    bookmaker_b, data_b = list(bookmakers_list[j].items())[0]
                    bookmaker_c, data_c = list(bookmakers_list[k].items())[0]
                    cote_victoire_a = data_a["victoire_equipe_a"]
                    cote_victoire_b = data_b["victoire_equipe_b"]
                    cote_match_nul = data_c["match_nul"]

                    # Vérification d'une opportunité de surebet
                    if (
                        1 / cote_victoire_a + 1 / cote_victoire_b + 1 / cote_match_nul
                        < 1
                    ):
                        M = total_stake / (
                            1 / cote_victoire_a
                            + 1 / cote_victoire_b
                            + 1 / cote_match_nul
                        )
                        mise_victoire_a = round(M / cote_victoire_a, 2)
                        mise_victoire_b = round(M / cote_victoire_b, 2)
                        mise_match_nul = round(M / cote_match_nul, 2)

                        gain_victoire_a = round(mise_victoire_a * cote_victoire_a, 2)
                        gain_victoire_b = round(mise_victoire_b * cote_victoire_b, 2)
                        gain_match_nul = round(mise_match_nul * cote_match_nul, 2)
                        gain_total = round(
                            gain_victoire_a + gain_victoire_b + gain_match_nul, 2
                        )

                        # Vérification des gains strictement positifs
                        if M > 0 and gain_total > total_stake:
                            surebet = {
                                "Match": match,
                                "Cotes": {
                                    "Cote victoire équipe A": cote_victoire_a,
                                    "Cote victoire équipe B": cote_victoire_b,
                                    "Cote match nul": cote_match_nul,
                                },
                                "Montants de mise": {
                                    "Mise victoire équipe A": mise_victoire_a,
                                    "Mise victoire équipe B": mise_victoire_b,
                                    "Mise match nul": mise_match_nul,
                                },
                                "Mise_totale": round(M, 2),
                                "Gains": {
                                    "Gain victoire équipe A": gain_victoire_a,
                                    "Gain victoire équipe B": gain_victoire_b,
                                    "Gain match nul": gain_match_nul,
                                },
                                "Gain_total": gain_total,
                            }
                            surebets[(bookmaker_a, bookmaker_b, bookmaker_c)] = surebet

    return surebets


"""

La fonction find_surebets(data, total_stake) prend en entrée un dictionnaire data contenant les informations sur les paris sportifs (les cotes de différents bookmakers pour chaque match) et total_stake qui représente le montant total que vous prévoyez de parier.

La fonction commence par initialiser un dictionnaire vide surebets qui sera utilisé pour stocker les opportunités de surebet identifiées.

Ensuite, elle parcourt chaque match et les bookmakers associés à ce match en utilisant une boucle for.

À l'aide de trois boucles for imbriquées, la fonction sélectionne toutes les combinaisons possibles de trois bookmakers différents pour chaque match. Cela permettra de comparer les cotes de chaque bookmaker et d'identifier s'il y a une opportunité de surebet.

Pour chaque combinaison de bookmakers, la fonction vérifie si la somme inverse des cotes est inférieure à 1. Si c'est le cas, cela signifie qu'il y a une opportunité de surebet.

Si une opportunité de surebet est trouvée, la fonction calcule les mises à effectuer sur chaque issue (victoire de l'équipe A, victoire de l'équipe B ou match nul) pour exploiter cette opportunité.

La fonction vérifie ensuite que les mises sont strictement positives et que le gain total attendu est supérieur à la mise totale initiale (total_stake).

Si toutes les conditions sont remplies, les informations concernant l'opportunité de surebet sont stockées dans le dictionnaire surebets.

Une fois toutes les combinaisons de bookmakers pour tous les matchs évaluées, la fonction renvoie le dictionnaire surebets contenant les meilleures opportunités de surebet avec des gains positifs.

L'exemple d'utilisation fourni utilise les données d'un seul match avec trois bookmakers. Il affiche les informations sur les opportunités de surebet identifiées, notamment les bookmakers à choisir, les mises à effectuer et les gains attendus pour chaque issue


"""

from typing import Dict, Any, List


# Nouvelle fonction plus générique
def find_surebets(
    data: Dict[str, List[Dict[str, Any]]], total_stake: float
) -> Dict[str, Any]:
    """
    Find surebets among different bookmakers' odds for given matches.

    Args:
        data (dict): A dictionary containing match names as keys and bookmakers' odds data as values.
        total_stake (float): The total stake for the surebet.

    Returns:
        dict: A dictionary containing surebet opportunities and their details.
    """
    surebets = {}

    for match, bookmakers_list in data.items():
        teams = list(
            bookmakers_list[0][list(bookmakers_list[0].keys())[0]]["odds"].keys()
        )
        n = len(list(bookmakers_list[0].keys()))

        odds_list = []
        bookmakers = []

        # for i in range(n):
        for bookmaker in bookmakers_list[0].keys():
            odds = [
                float(odds.replace(",", "."))
                for odds in bookmakers_list[0][bookmaker]["odds"].values()
            ]
            odds_list.append(odds)
            bookmakers.append(bookmaker)

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    stake = total_stake / (
                        sum(1 / odds[i] for odds in odds_list)
                        + sum(1 / odds[j] for odds in odds_list)
                        + sum(1 / odds[k] for odds in odds_list)
                    )
                    gain = stake * (
                        sum(odds[i] for odds in odds_list)
                        + sum(odds[j] for odds in odds_list)
                        + sum(odds[k] for odds in odds_list)
                    )

                    # Check for surebet opportunity
                    if gain > total_stake:
                        surebet = {
                            "Match": match,
                            "Bookmakers": [bookmakers[i], bookmakers[j], bookmakers[k]],
                            "Stake": stake,
                            "Gain": gain,
                        }

                        for team in teams:
                            surebet["Cotes_" + team] = [
                                odds[i][team],
                                odds[j][team],
                                odds[k][team],
                            ]

                        surebets[
                            (bookmakers[i], bookmakers[j], bookmakers[k])
                        ] = surebet

    return surebets


data = {
    "Burnley  vs Manchester City": [
        {
            "Betclic": {
                "odds": {"Burnley": "20", "Draw": "4.0", "Manchester City": "3,0"}
            },
            "Parions Sport": {
                "odds": {"Burnley": "2.2", "Draw": "3.8", "Man. City": "3.5"}
            },
            "Bet365": {"odds": {"Burnley": "2.2", "Draw": "3.0", "Man. City": "30.2"}},
        }
    ]
}

total_stake = 100

# ========================== Find surbet ========================
from typing import Dict, Any, List


def find_surebets(
    data: Dict[str, List[Dict[str, Any]]], total_stake: float
) -> Dict[str, Any]:
    """
    Find surebets among different bookmakers' odds for given matches.

    Args:
        data (dict): A dictionary containing match names as keys and bookmakers' odds data as values.
        total_stake (float): The total stake for the surebet.

    Returns:
        dict: A dictionary containing surebet opportunities and their details.
    """
    surebets = {}

    for match, bookmakers_list in data.items():
        teams = list(
            bookmakers_list[0][list(bookmakers_list[0].keys())[0]]["odds"].keys()
        )
        n = len(list(bookmakers_list[0].keys()))

        odds_list = []
        bookmakers = []

        for bookmaker in bookmakers_list[0].keys():
            odds = {
                team: float(odds.replace(",", "."))
                for team, odds in zip(
                    teams, bookmakers_list[0][bookmaker]["odds"].values()
                )
            }
            odds_list.append(odds)
            bookmakers.append(bookmaker)

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    print([odds[team] for odds in odds_list for team in teams])
                    stake = total_stake / (
                        sum(1 / odds[team] for odds in odds_list for team in teams)
                    )
                    gain = stake * (
                        sum(odds[team] for odds in odds_list for team in teams)
                    )

                    # Check for surebet opportunity
                    if gain > total_stake:
                        surebet = {
                            "Match": match,
                            "Bookmakers": [bookmakers[i], bookmakers[j], bookmakers[k]],
                            "Stake": stake,
                            "Gain": gain,
                        }

                        for team in teams:
                            surebet["Cotes_" + team] = [
                                odds_list[i][team],
                                odds_list[j][team],
                                odds_list[k][team],
                            ]

                        surebets[
                            (bookmakers[i], bookmakers[j], bookmakers[k])
                        ] = surebet

    return surebets


surebets = find_surebets(data, total_stake)
print(surebets)
