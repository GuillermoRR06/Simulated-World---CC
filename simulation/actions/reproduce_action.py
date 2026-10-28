from .action import Action
from ..model.world import World
from ..model.creature import Creature


class ReproduceAction(Action):

    def execute(self, world: World, creature: Creature, dx: int, dy: int, health: int):
        self._validate_direction(dx, dy)

        if creature.x is None or creature.y is None:
            raise ValueError(
                "Creature is not placed in the world"
            )

        # La cría debe nacer en una casilla adyacente.
        if dx == 0 and dy == 0:
            return

        target_x = creature.x + dx
        target_y = creature.y + dy

        # Fuera del mapa: reproducción fallida.
        if not world.is_inside(target_x, target_y):
            return

        target_cell = world.get_cell(target_x, target_y)

        # Tiene que haber solamente terreno.
        if target_cell.is_occupied():
            return

        # La madre debe tener MÁS vida que
        # la cantidad que entregará a la cría.
        if creature.health <= health:
            return

        child = Creature(creature.species)

        child.health = health

        creature.health -= health

        world.place_creature(child, target_x,target_y)

        return child