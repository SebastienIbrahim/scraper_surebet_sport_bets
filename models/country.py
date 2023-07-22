class Country:
    def __init__(self, name, button):
        self.name = name
        self.button = button
        self.competitions = []

    def __str__(self):
        return self.name

    def to_dict(self):
        competitions_dict = [competition.to_dict() for competition in self.competitions]
        return {"name": self.name, "competitions": competitions_dict}
