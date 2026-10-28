from .action import Action
from ..model.world import World
from ..model.creature import Creature


class SayAction(Action):

    consumes_turn = False

    def execute(
        self,
        world: World,
        creature: Creature,
        value
    ) -> str:
        return str(value)