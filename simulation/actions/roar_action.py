from .action import Action
from ..model.world import World
from ..model.creature import Creature


class RoarAction(Action):

    def execute(self, world: World, creature: Creature,value):
        return world.emit_roar(creature, value)