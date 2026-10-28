from .action import Action
from ..model.world import World
from ..model.creature import Creature


class WaitAction(Action):

    def execute(
        self,
        world: World,
        creature: Creature,
        n: int
    ):
        effective_turns = max(1, n)

        creature.wait_turns_remaining = (
            effective_turns - 1
        )