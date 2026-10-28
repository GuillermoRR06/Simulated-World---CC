from .action import Action
from ..model.world import World
from ..model.creature import Creature


class ConsumeAction(Action):

    def execute(self, world: World, creature: Creature, dx: int, dy: int, damage: int, heal: int):

        self._validate_direction(dx,dy)

        if creature.x is None or creature.y is None:
            raise ValueError(
                "Creature is not placed in the world"
            )

        # Consumir el terreno bajo la criatura
        if dx == 0 and dy == 0:
            cell = world.get_cell(creature.x, creature.y)

            cell.terrain.resource -= damage
            creature.heal(heal)

            return

        target_x = creature.x + dx
        target_y = creature.y + dy

        # Fuera del mapa: no ocurre nada
        if not world.is_inside(target_x, target_y):
            return

        cell = world.get_cell(target_x, target_y)

        # Consumir una criatura
        if cell.creature is not None:
            target_creature = cell.creature

            target_creature.take_damage(damage)

            creature.heal(heal)

            if target_creature.health <= 0:
                world.remove_creature(target_creature.x, target_creature.y)

            return

        # Consumir un objeto
        if cell.world_object is not None:
            cell.world_object.resource -= damage

            creature.heal(heal)

            return

        # Consumir terreno
        cell.terrain.resource -= damage
        creature.heal(heal)
