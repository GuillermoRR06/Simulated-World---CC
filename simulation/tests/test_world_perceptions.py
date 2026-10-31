from random import Random

from simulation.model.terrain import Terrain
from simulation.model.species import Species
from simulation.model.creature import Creature
from simulation.model.world import World

from simulation.perceptions.perceptions import (
    PerceptionContext
)

from simulation.perceptions.world_perceptions import (
    WidthPerception,
    HeightPerception,
    TickPerception,
    TotalCreaturesPerception,
    TotalAlliesPerception,
    TotalEnemiesPerception,
    RandomPerception,
)


# --------------------------------
# Mundo
# --------------------------------

grass = Terrain(
    "Grass",
    ".",
    100,
    2
)

world = World(
    6,
    4,
    grass
)


# --------------------------------
# Especies
# --------------------------------

eldian = Species(
    "Eldian",
    "eldia",
    100,
    1,
    100
)

scout = Species(
    "Scout",
    "eldia",
    100,
    1,
    100
)

marleyan = Species(
    "Marleyan",
    "marley",
    100,
    1,
    100
)


# --------------------------------
# Criaturas
# --------------------------------

observer = Creature(eldian)

ally1 = Creature(eldian)
ally2 = Creature(scout)

enemy = Creature(marleyan)


world.place_creature(
    observer,
    2,
    2
)

world.place_creature(
    ally1,
    0,
    0
)

world.place_creature(
    ally2,
    5,
    3
)

world.place_creature(
    enemy,
    4,
    2
)


# --------------------------------
# Contexto
# --------------------------------

context = PerceptionContext(
    world=world,
    creature=observer,
    tick=12,
    rng=Random(42)
)


# --------------------------------
# Tamaño del mundo
# --------------------------------

assert WidthPerception().read(
    context
) == 6

assert HeightPerception().read(
    context
) == 4


# --------------------------------
# Tick
# --------------------------------

assert TickPerception().read(
    context
) == 12


# --------------------------------
# Totales
# --------------------------------

assert TotalCreaturesPerception().read(
    context
) == 3

assert TotalAlliesPerception().read(
    context
) == 2

assert TotalEnemiesPerception().read(
    context
) == 1


# --------------------------------
# El estado se consulta de verdad
# --------------------------------

world.remove_creature(
    ally2.x,
    ally2.y
)

assert TotalCreaturesPerception().read(
    context
) == 2

assert TotalAlliesPerception().read(
    context
) == 1

assert TotalEnemiesPerception().read(
    context
) == 1


# --------------------------------
# Random está entre 0 y 99
# --------------------------------

random_perception = RandomPerception()

values = [
    random_perception.read(context)
    for _ in range(10)
]

assert all(
    0 <= value <= 99
    for value in values
)


# --------------------------------
# Misma semilla =
# misma secuencia
# --------------------------------

context1 = PerceptionContext(
    world=world,
    creature=observer,
    tick=12,
    rng=Random(123)
)

context2 = PerceptionContext(
    world=world,
    creature=observer,
    tick=12,
    rng=Random(123)
)

sequence1 = [
    random_perception.read(context1)
    for _ in range(5)
]

sequence2 = [
    random_perception.read(context2)
    for _ in range(5)
]

assert sequence1 == sequence2


print("World perceptions tests passed")