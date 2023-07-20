class Sport:
    def __init__(self, name, bloc):
        self.name = name
        self.bloc = bloc
        self.countries = []

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.name

    def to_dict(self):
        countries_dict = [country.to_dict() for country in self.countries]
        return {"name": self.name, "countries": countries_dict}
