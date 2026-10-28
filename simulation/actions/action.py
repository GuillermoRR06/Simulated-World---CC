from abc import ABC, abstractmethod

from ..model.world import World
from ..model.creature import Creature


class Action(ABC):

    consumes_turn = True

    @abstractmethod
    def execute(
        self,
        world: World,
        creature: Creature,
        *args
    ):
        pass

    def _validate_direction(
        self,
        dx: int,
        dy: int
    ):
        valid_directions = {-1, 0, 1}

        if (
            dx not in valid_directions
            or dy not in valid_directions
        ):
            raise ValueError(
                "dx and dy must be -1, 0 or 1"
            )