from simulation.model.terrain import Terrain
from simulation.model.world_object import WorldObject
from simulation.model.species import Species
from simulation.model.creature import Creature
from simulation.model.world import World
from simulation.simulator import Simulator


grass = Terrain(
    "Grass",
    ".",
    100,
    2
)

species = Species(
    "TestCreature",
    "test",
    10,
    5,
    10
)

world = World(
    4,
    3,
    grass
)

creature = Creature(species)

world.place_creature(
    creature,
    1,
    1
)

# Reducimos el terreno para poder comprobar
# que realmente se regenera.
world.get_cell(
    0,
    0
).terrain.resource = 50


rock = WorldObject(
    "Rock",
    "#",
    100
)

world.get_cell(
    3,
    2
).place_object(rock)

# Simulamos un objeto completamente agotado.
rock.resource = 0


simulator = Simulator(
    world,
    seed=42
)

simulator.advance_tick()


assert simulator.current_tick == 1

assert creature.health == 9
assert creature.age == 1

assert (
    world.get_cell(
        0,
        0
    ).terrain.resource
    == 52
)

assert (
    world.get_cell(
        3,
        2
    ).world_object
    is None
)


print("Simulator tick tests passed")