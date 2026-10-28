from .action import Action
from ..model.world import World
from ..model.creature import Creature


class AttackAction(Action):

    def execute(self, world: World, creature: Creature, dx: int, dy: int, damage: int):
        self._validate_direction(dx,dy)

        if creature.x is None or creature.y is None:
            raise ValueError(
                "Creature is not placed in the world"
            )

        # Caso especial:
        # (0, 0) significa atacar el terreno
        # debajo de la propia criatura.
        if dx == 0 and dy == 0:
            cell = world.get_cell(creature.x, creature.y)

            cell.terrain.resource -= damage
            return

        target_x = creature.x + dx
        target_y = creature.y + dy

        # Fuera del mundo:
        # la acción simplemente no hace nada.
        if not world.is_inside(target_x, target_y):
            return

        cell = world.get_cell(target_x, target_y)

        # Atacar criatura
        if cell.creature is not None:
            target_creature = cell.creature

            target_creature.take_damage(damage)

            if target_creature.health <= 0:
                world.remove_creature(
                    target_creature.x,
                    target_creature.y
                )

            return

        # Atacar objeto
        if cell.world_object is not None:
            cell.world_object.resource -= damage
            return

        # Si no hay criatura ni objeto,
        # atacamos el terreno.
        cell.terrain.resource -= damage
