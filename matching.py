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


def merge_dicts_with_odds(*site_dicts):
    merged_odds = {}

    for site_data in site_dicts:
        site_name = site_data["name"]
        matches = site_data["matches"]

        for match in matches:
            teams = match["teams"]
            odds = match["odds"]

            for outcome, value in odds.items():
                full_key = f"{teams} - {outcome}"
                if site_name not in merged_odds:
                    merged_odds[site_name] = {}

                merged_odds[site_name][full_key] = value

    return merged_odds


merged_data = merge_dicts_with_odds(site_A, site_B)
print(merged_data)
