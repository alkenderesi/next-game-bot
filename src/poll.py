import json
from discord import Member
from typing import Protocol
from dataclasses import dataclass


with open("config/games.json", "r") as game_config:
    GAMES: dict[str, list[int]] = json.load(game_config)


class PollState(Protocol):
    def is_active(self) -> bool:
        ...

    def is_complete(self) -> bool:
        ...

    def add(self, participants: list[Member]) -> None:
        ...

    def active_participant(self) -> Member:
        ...

    def submit(self, game: str) -> None:
        ...

    def result(self) -> str:
        ...


class PollContext(Protocol):
    participants: list[Member]
    games: list[str]

    def set_state(self, state: PollState) -> None:
        ...

    def is_active(self) -> bool:
        ...

    def is_complete(self) -> bool:
        ...

    def add(self, participants: list[Member]) -> None:
        ...

    def active_participant(self) -> Member:
        ...

    def submit(self, game: str) -> None:
        ...

    def result(self) -> str:
        ...


@dataclass
class Inactive:
    poll: PollContext

    def is_active(self) -> bool:
        return False

    def is_complete(self) -> bool:
        return False

    def add(self, participants: list[Member]) -> None:
        if len(participants) < 2:
            raise ValueError("Not enough participants.")

        self.poll.participants.extend(participants)

        for game, squad_options in GAMES.items():
            if len(participants) in squad_options:
                self.poll.games.append(game)

        if len(self.poll.games) == 0:
            raise ValueError(f"No games with squad size: {len(participants)}")

        elif len(self.poll.games) == 1:
            self.poll.set_state(Complete(self.poll))

        else:
            self.poll.set_state(Active(self.poll))

    def active_participant(self) -> Member:
        raise RuntimeError("Poll is not active.")

    def submit(self, game: str) -> None:
        raise RuntimeError("Poll is not active.")

    def result(self) -> str:
        raise RuntimeError("Poll is not complete.")


@dataclass
class Active:
    poll: PollContext

    def is_active(self) -> bool:
        return True

    def is_complete(self) -> bool:
        return False

    def add(self, participants: list[Member]) -> None:
        raise RuntimeError("Poll is already active.")

    def active_participant(self) -> Member:
        return self.poll.participants[
            len(self.poll.games) % len(self.poll.participants)
        ]

    def submit(self, game: str) -> None:
        if game in self.poll.games:
            self.poll.games.remove(game)

        if len(self.poll.games) == 1:
            self.poll.set_state(Complete(self.poll))

    def result(self) -> str:
        raise RuntimeError("Poll is not complete.")


@dataclass
class Complete:
    poll: PollContext

    def is_active(self) -> bool:
        return False

    def is_complete(self) -> bool:
        return True

    def add(self, participants: list[Member]) -> None:
        raise RuntimeError("Poll is already complete.")

    def active_participant(self) -> Member:
        raise RuntimeError("Poll is already complete.")

    def submit(self, game: str) -> None:
        raise RuntimeError("Poll is already complete.")

    def result(self) -> str:
        return self.poll.games[0]


class Poll:
    def __init__(self) -> None:
        self.state: PollState = Inactive(self)
        self.participants: list[Member] = []
        self.games: list[str] = []

    @property
    def active_participant(self) -> Member:
        return self.state.active_participant()

    def is_active(self) -> bool:
        return self.state.is_active()

    def is_complete(self) -> bool:
        return self.state.is_complete()

    def add(self, participants: list[Member]) -> None:
        return self.state.add(participants)

    def submit(self, game: str) -> None:
        return self.state.submit(game)

    def result(self) -> str:
        return self.state.result()

    def set_state(self, state: PollState) -> None:
        self.state = state

    def reset(self) -> None:
        self.participants.clear()
        self.games.clear()
        self.set_state(Inactive(self))
