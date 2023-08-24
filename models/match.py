from dateutil import parser


class Match:
    def __init__(self, teams, date_time, odds=None):
        self.teams = teams
        if isinstance(date_time, list) and len(date_time) == 1:
            date_time = date_time[0].strip()
        self.date_time = date_time
        self.odds = odds if odds is not None else []

    @staticmethod
    def convert_datetime_format(input_datetime_str):
        try:
            # Convertir la chaîne en objet de date et heure
            input_datetime = parser.parse(input_datetime_str)

            # Formater la date et l'heure dans le nouveau format
            formatted_datetime_str = input_datetime.strftime("%Y/%m/%d/%H/%M")

            return formatted_datetime_str
        except ValueError as e:
            raise ValueError("Format de date et heure invalide.")

    def add_odds(self, odds):
        self.odds.extend(odds)

    def get_teams_str(self):
        return " vs ".join(team.name for team in self.teams)

    def __str__(self):
        teams_str = self.get_teams_str()
        odds_str = ", ".join(str(odd) for odd in self.odds)
        return f"{teams_str}, {self.date_time[0] if isinstance(self.date_time, list) else self.date_time}, Côtes: {odds_str}"

    def to_dict(self):
        teams_str = " vs ".join(team.name for team in self.teams)
        odds_dict = {}
        for odd in self.odds:
            if odd.type == "Win":
                team_name = self.teams[self.odds.index(odd)].name
                odds_dict[f"{team_name} - {odd.type}"] = odd.value
            elif odd.type == "Draw":
                odds_dict["Draw"] = odd.value

        match_dict = {
            "teams": teams_str,
            "date_time": self.convert_datetime_format(self.date_time[0])
            if isinstance(self.date_time, list)
            else self.convert_datetime_format(self.date_time),
            "odds": odds_dict,
        }
        return match_dict
