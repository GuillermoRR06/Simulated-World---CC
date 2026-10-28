from simulation.actions.say_action import SayAction
from simulation.actions.move_action import MoveAction

from simulation.model.creature import Creature
from simulation.model.species import Species
from simulation.model.terrain import Terrain
from simulation.model.world import World


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

say = SayAction()
move = MoveAction()


# -----------------------------
# Say no consume turno
# -----------------------------

assert say.consumes_turn is False


# -----------------------------
# Las demás acciones sí
# -----------------------------

assert move.consumes_turn is True


# -----------------------------
# Say con texto
# -----------------------------

message = say.execute(
    world,
    creature,
    "Hello world"
)

assert message == "Hello world"


# -----------------------------
# Say con número
# -----------------------------

message = say.execute(
    world,
    creature,
    42
)

assert message == "42"


print("SayAction tests passed")