from simulation.actions.wait_action import WaitAction
from simulation.model.creature import Creature
from simulation.model.species import Species
from simulation.model.terrain import Terrain
from simulation.model.world import World
from simulation.simulator import Simulator


class TestSimulator(Simulator):

    def __init__(self, world, seed=None):
        super().__init__(world, seed)

        self.turns_executed = 0

    def _run_turn(self, creature):
        self.turns_executed += 1


grass = Terrain(
    "Grass",
    ".",
    100,
    2
)

species = Species(
    "TestCreature",
    "test",
    100,
    5,
    100
)

world = World(
    5,
    5,
    grass
)

creature = Creature(species)

world.place_creature(
    creature,
    2,
    2
)

simulator = TestSimulator(
    world,
    seed=42
)

wait = WaitAction()


# La criatura acaba de ejecutar wait(4).
wait.execute(
    world,
    creature,
    4
)

assert creature.wait_turns_remaining == 3


# -----------------------------
# Primer turno que se salta
# -----------------------------

simulator.advance_tick()

assert creature.wait_turns_remaining == 2
assert simulator.turns_executed == 0

assert creature.age == 1
assert creature.health == 99


# -----------------------------
# Segundo turno que se salta
# -----------------------------

simulator.advance_tick()

assert creature.wait_turns_remaining == 1
assert simulator.turns_executed == 0

assert creature.age == 2
assert creature.health == 98


# -----------------------------
# Tercer turno que se salta
# -----------------------------

simulator.advance_tick()

assert creature.wait_turns_remaining == 0
assert simulator.turns_executed == 0

assert creature.age == 3
assert creature.health == 97


# -----------------------------
# La criatura vuelve a actuar
# -----------------------------

simulator.advance_tick()

assert creature.wait_turns_remaining == 0
assert simulator.turns_executed == 1

assert creature.age == 4
assert creature.health == 96


print("Wait simulator tests passed")