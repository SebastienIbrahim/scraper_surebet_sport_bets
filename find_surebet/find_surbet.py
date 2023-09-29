import itertools
from typing import Dict, Any, List
import pandas as pd


def display_info(label, data):
    print(label + ":")
    for key, value in data.items():
        print(f"\t{key}: {value} (Bookmaker {key.split()[-1]})")


data = {
    "Burnley  vs Manchester City": [
        {
            "Betclic": {
                "odds": {"Burnley": "7,85", "Draw": "4,90", "Manchester City": "1,29"},
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


data = {
    "Burnley  vs Manchester City": [
        {
            "Betclic": {
                "odds": {"Burnley": "20", "Draw": "4.0", "Manchester City": "3,0"},
                "date": "12/08/2023",
            },
            "Parions Sport": {
                "odds": {"Burnley": "2.2", "Draw": "3.8", "Man. City": "3.5"},
                "date": "12/08/2023",
            },
            "Bet365": {
                "odds": {"Burnley": "2.2", "Draw": "3.0", "Man. City": "30.2"},
                "date": "12/08/2023",
            },
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


def calculate_surebets(match_data):
    surebets = []

    for match_name, bookmakers_data in match_data.items():
        teams = set()
        for bookmaker_odds in bookmakers_data:
            for bookmaker, odds in bookmaker_odds.items():
                teams.update(odds["odds"].keys())

        for team in teams:
            probabilities = []
            bookmaker_odds_info = {}  # To store bookmaker odds information
            for bookmaker_odds in bookmakers_data:
                for bookmaker, odds in bookmaker_odds.items():
                    if team in odds["odds"]:
                        odd = float(odds["odds"][team].replace(",", "."))
                        inverse_odd = 1 / odd
                        probabilities.append(inverse_odd)
                        bookmaker_odds_info[bookmaker] = round(
                            odd, 3
                        )  # Store rounded odds associated with bookmaker

            if len(probabilities) >= 3:
                for combo in itertools.combinations(probabilities, 3):
                    total_probability = sum(combo)
                    if total_probability < 1:
                        surebet = {
                            "Match": match_name,
                            "Bookmakers": [
                                bookmaker for bookmaker in bookmaker_odds_info
                            ],
                            "Surebet Value": round(1 - total_probability, 3),
                            "Teams": [team, team, team],
                            "Inverse Odds": [round(inv_odds, 3) for inv_odds in combo],
                            "Total Inverse Odds": round(sum(combo), 3),
                            "Bookmaker Odds": {
                                bookmaker: odds
                                for bookmaker, odds in bookmaker_odds_info.items()
                            },
                        }
                        surebets.append(surebet)

    return surebets


def calculate_stakes(surebets, bet_amount):
    stakes = []

    for surebet in surebets:
        total_inverse_odds = surebet["Total Inverse Odds"]
        stake_per_bet = bet_amount / total_inverse_odds

        for team, inv_odds, bookmaker in zip(
            surebet["Teams"], surebet["Inverse Odds"], surebet["Bookmakers"]
        ):
            stake = round(stake_per_bet * inv_odds, 3)
            stakes.append(
                {
                    "Match": surebet["Match"],
                    "Team": team,
                    "Stake": stake,
                    "Bookmaker": bookmaker,
                }
            )

    # Group stakes by 3 to get the surebet combination
    grouped_stakes = [stakes[i : i + 3] for i in range(0, len(stakes), 3)]

    return grouped_stakes


def find_surbets_opportunities(
    data: Dict[str, Dict[str, Any]],
    investissement_amount: float = 100,
    nb_way: int = 3,
    draw_position: int = 1,
) -> Dict[str, Any]:
    """Find surbets opportunities among different bookmakers' odds for given matches.
    Args:
        data (_type_): A dictionary containing match names as keys and bookmakers' odds data as values.
        investissement_amount (int, optional): Total investissement for the surbet. Defaults to 100.
        nb_way (int, optional): Number of way for the surbet. Defaults to 3 (win of each team plus draw).
        draw_position (int, optional): Position of the draw in the list of teams. Defaults to 1.

    Returns:
        _type_: opportunities dict with stakes for each bookmaker and team
    """
    opportunities = {}
    count_opportunity = 0
    for teams_str, bookmakers_data_list in data.items():
        try:
            odds_list = []
            teams = teams_str.split(" vs ")
            teams = [team.strip() for team in teams]
            teams.insert(draw_position, "Draw")
            bookmakers_data = bookmakers_data_list[0]
            for bookmaker in bookmakers_data:
                bookmakers_data[bookmaker]["odds"] = {
                    team: odd
                    for team, odd in zip(
                        teams, bookmakers_data[bookmaker]["odds"].values()
                    )
                }
                for team, odd in bookmakers_data[bookmaker]["odds"].items():
                    odds_list.append(
                        {
                            "bookmaker": bookmaker,
                            "team": team,
                            "odds": float(odd.replace(",", ".")),
                            "date": bookmakers_data[bookmaker]["date"],
                        }
                    )
            for combinaison in itertools.combinations(odds_list, nb_way):
                total_proba = sum(
                    1 / combinaison[iter_way]["odds"] for iter_way in range(nb_way)
                )
                is_valide_combinaison = (
                    len(pd.unique([combinaison[i]["team"] for i in range(nb_way)]))
                    == nb_way
                )
                # verify if all odds are from the same date
                same_date = (
                    len(pd.unique([combinaison[i]["date"] for i in range(nb_way)])) == 1
                )
                if total_proba < 1 and is_valide_combinaison and same_date:
                    count_opportunity += 1
                    roi = 1 - total_proba
                    stakes = {
                        combinaison[i]["team"]: {
                            "bookmaker": combinaison[i]["bookmaker"],
                            "odds": combinaison[i]["odds"],
                            "mise": round(
                                1
                                / combinaison[i]["odds"]
                                * (investissement_amount / total_proba),
                                2,
                            ),
                            "gain": round(
                                1
                                / combinaison[i]["odds"]
                                * (investissement_amount / total_proba)
                                * combinaison[i]["odds"],
                                2,
                            ),
                            "roi": f"{100*roi:.2f}%",
                            "date": combinaison[i]["date"],
                        }
                        for i in range(nb_way)
                    }
                    opportunities[f"opportunity_{count_opportunity}"] = stakes
        except Exception as e:
            continue
    return opportunities


opportunities = find_surbets_opportunities(
    data, investissement_amount=100, nb_way=3, draw_position=1
)
