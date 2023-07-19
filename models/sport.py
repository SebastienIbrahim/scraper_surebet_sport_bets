class Sport:
    def __init__(self, name, bloc):
        self.name = name
        self.bloc = bloc
        self.countries = []

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.name
