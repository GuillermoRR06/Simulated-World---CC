import random

from .model.world import World
from .model.creature import Creature


class Simulator:
    def __init__(self, world: World, seed: int | None = None):
        self.world = world
        self.current_tick = 0
        self.rng = random.Random(seed)

    def advance_tick(self):
        self.world.rotate_roars()
        turn_order = self.world.get_creatures()

        self.rng.shuffle(turn_order)

        for creature in turn_order:
            if not creature.is_alive():
                continue

            if creature.x is None or creature.y is None:
                continue

            if creature.wait_turns_remaining > 0:
                creature.wait_turns_remaining -= 1
                continue

            self._run_turn(creature)

        self._apply_end_of_tick_rules()

        self.current_tick += 1

    def _run_turn(self, creature: Creature):
        pass

    def _apply_end_of_tick_rules(self):
        creatures = self.world.get_creatures()

        # Fase 1: todas envejecen y pierden vida
        for creature in creatures:
            creature.age += 1
            creature.health -= 1

        # Fase 2: eliminar las que murieron
        for creature in creatures:
            if (
                creature.health <= 0
                or creature.age >= creature.species.lifespan
            ):
                self.world.remove_creature(
                    creature.x,
                    creature.y
                )

        # Fase 3 y 4: terreno y objetos
        for row in self.world.grid:
            for cell in row:
                cell.terrain.regenerate()

                if (
                    cell.world_object is not None
                    and cell.world_object.resource <= 0
                ):
                    cell.remove_object()