from simulation.actions.reproduce_action import ReproduceAction
from simulation.model.creature import Creature
from simulation.model.species import Species
from simulation.model.terrain import Terrain
from simulation.model.world import World
from simulation.model.world_object import WorldObject


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
    6,
    6,
    grass
)

mother = Creature(species)

world.place_creature(
    mother,
    2,
    2
)

reproduce = ReproduceAction()


# --------------------------------
# 1. Reproducción correcta
# --------------------------------

child = reproduce.execute(
    world,
    mother,
    1,
    0,
    30
)

assert child is not None

assert mother.health == 70

assert child.health == 30
assert child.age == 0

assert child.x == 3
assert child.y == 2

assert child.species is mother.species

assert world.get_cell(
    3,
    2
).creature is child

assert len(
    world.get_creatures()
) == 2


# --------------------------------
# 2. Casilla ocupada por criatura
# --------------------------------

health_before = mother.health

failed_child = reproduce.execute(
    world,
    mother,
    1,
    0,
    20
)

assert failed_child is None
assert mother.health == health_before

assert world.get_cell(
    3,
    2
).creature is child


# --------------------------------
# 3. Casilla ocupada por objeto
# --------------------------------

rock = WorldObject(
    "Rock",
    "#",
    100
)

world.get_cell(
    1,
    2
).place_object(rock)

health_before = mother.health

failed_child = reproduce.execute(
    world,
    mother,
    -1,
    0,
    20
)

assert failed_child is None
assert mother.health == health_before

assert world.get_cell(
    1,
    2
).world_object is rock


# --------------------------------
# 4. Vida exactamente igual
# --------------------------------

mother.health = 30

failed_child = reproduce.execute(
    world,
    mother,
    0,
    1,
    30
)

assert failed_child is None
assert mother.health == 30

assert world.get_cell(
    2,
    3
).creature is None


# --------------------------------
# 5. Vida estrictamente mayor
# --------------------------------

mother.health = 31

child2 = reproduce.execute(
    world,
    mother,
    0,
    1,
    30
)

assert child2 is not None

assert mother.health == 1

assert child2.health == 30
assert child2.age == 0

assert child2.x == 2
assert child2.y == 3

assert child2.species is mother.species


# --------------------------------
# 6. Dirección (0,0)
# --------------------------------

mother2 = Creature(species)

world.place_creature(
    mother2,
    4,
    4
)

health_before = mother2.health

failed_child = reproduce.execute(
    world,
    mother2,
    0,
    0,
    20
)

assert failed_child is None
assert mother2.health == health_before

assert world.get_cell(
    4,
    4
).creature is mother2


# --------------------------------
# 7. Fuera del mapa
# --------------------------------

edge_mother = Creature(species)

world.place_creature(
    edge_mother,
    0,
    0
)

health_before = edge_mother.health

failed_child = reproduce.execute(
    world,
    edge_mother,
    -1,
    0,
    20
)

assert failed_child is None
assert edge_mother.health == health_before


print("ReproduceAction tests passed")