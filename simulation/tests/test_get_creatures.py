from simulation.model.terrain import Terrain
from simulation.model.species import Species
from simulation.model.creature import Creature
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
    80
)

world = World(
    5,
    4,
    grass
)

creature1 = Creature(species)
creature2 = Creature(species)
creature3 = Creature(species)

world.place_creature(creature1, 0, 0)
world.place_creature(creature2, 2, 1)
world.place_creature(creature3, 4, 3)


creatures = world.get_creatures()


assert len(creatures) == 3

assert creature1 in creatures
assert creature2 in creatures
assert creature3 in creatures


print("Get creatures tests passed")