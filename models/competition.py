class Competition:
    def __init__(self, name):
        self.name = name
        self.matches = []

    def __str__(self):
        return self.name

    def to_dict(self):
        matches_dict = [match.to_dict() for match in self.matches]
        return {"name": self.name, "matches": matches_dict}
