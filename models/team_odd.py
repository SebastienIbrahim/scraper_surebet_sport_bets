from typing import NamedTuple


class Team(NamedTuple):
    name: str


class Odd(NamedTuple):
    value: str
    type: str
    team_index: int = None

    def __str__(self):
        return f"{self.type}: {self.value}"
