class Competition:
    def __init__(self, name):
        self.name = name
        self.matches = []

    def __str__(self):
        return self.name
