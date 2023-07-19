class Match:
    def __init__(self, teams, date_time, odds=None):
        self.teams = teams
        self.date_time = date_time
        self.odds = odds if odds is not None else []

    def add_odds(self, odds):
        self.odds.extend(odds)

    def __str__(self):
        return f"{self.teams[0]} vs {self.teams[1]}, {self.date_time}, Côtes: {', '.join(self.odds)}"
