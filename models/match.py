class Match:
    def __init__(self, teams, date_time, odds=None):
        self.teams = teams
        self.date_time = date_time
        self.odds = odds if odds is not None else []

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
            odds_dict.setdefault(odd.type, []).append(odd.value)

        match_dict = {
            "teams": teams_str,
            "date_time": self.date_time[0]
            if isinstance(self.date_time, list)
            else self.date_time,
            "odds": odds_dict,
        }
        return match_dict
