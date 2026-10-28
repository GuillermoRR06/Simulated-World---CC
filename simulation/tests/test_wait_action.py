from simulation.actions.wait_action import WaitAction
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

wait = WaitAction()


# wait(4)
wait.execute(
    world,
    creature,
    4
)

assert creature.wait_turns_remaining == 3


# wait(1)
wait.execute(
    world,
    creature,
    1
)

assert creature.wait_turns_remaining == 0


# wait(0) cuenta como wait(1)
wait.execute(
    world,
    creature,
    0
)

assert creature.wait_turns_remaining == 0


# wait negativo también cuenta como wait(1)
wait.execute(
    world,
    creature,
    -10
)

assert creature.wait_turns_remaining == 0


print("WaitAction tests passed")