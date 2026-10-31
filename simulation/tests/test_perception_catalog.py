from random import Random

from simulation.model.terrain import Terrain
from simulation.model.world_object import WorldObject
from simulation.model.species import Species
from simulation.model.creature import Creature
from simulation.model.world import World

from simulation.perceptions.perceptions import (
    PerceptionContext
)

from simulation.perceptions.catalog import (
    PerceptionCatalog
)

from simulation.perceptions.vision_functions import (
    OBJECT,
    ALLY,
)


grass = Terrain(
    "Grass",
    ".",
    100,
    2
)

world = World(
    7,
    7,
    grass
)


eldian = Species(
    "Eldian",
    "eldia",
    100,
    3,
    100
)

marleyan = Species(
    "Marleyan",
    "marley",
    100,
    3,
    100
)


observer = Creature(
    eldian
)

enemy = Creature(
    marleyan
)


world.place_creature(
    observer,
    3,
    3
)

world.place_creature(
    enemy,
    5,
    3
)


rock = WorldObject(
    "Rock",
    "#",
    100
)

world.get_cell(
    2,
    3
).place_object(
    rock
)


context = PerceptionContext(
    world=world,
    creature=observer,
    tick=7,
    rng=Random(42)
)


catalog = PerceptionCatalog()


# ============================================================
# PERCEPCIONES PROPIAS
# ============================================================

assert catalog.read(
    "health",
    context
) == 100

assert catalog.read(
    "age",
    context
) == 0

assert catalog.read(
    "species",
    context
) == "Eldian"

assert catalog.read(
    "faction",
    context
) == "eldia"

assert catalog.read(
    "x",
    context
) == 3

assert catalog.read(
    "y",
    context
) == 3


# ============================================================
# PERCEPCIONES DEL MUNDO
# ============================================================

assert catalog.read(
    "width",
    context
) == 7

assert catalog.read(
    "height",
    context
) == 7

assert catalog.read(
    "tick",
    context
) == 7

assert catalog.read(
    "total_enemies",
    context
) == 1


# ============================================================
# PERCEPCIONES CERCANAS
# ============================================================

assert catalog.read(
    "enemies_near",
    context
) == 1

assert catalog.read(
    "enemy_dist",
    context
) == 2

assert catalog.read(
    "enemy_dx",
    context
) == 1

assert catalog.read(
    "enemy_dy",
    context
) == 0


# ============================================================
# SEE
# ============================================================

assert catalog.call(
    "see",
    context,
    2,
    3
) == OBJECT


assert catalog.call(
    "see",
    context,
    3,
    3
) == ALLY


# ============================================================
# NAME
# ============================================================

assert catalog.call(
    "name",
    context,
    2,
    3
) == "Rock"


assert catalog.call(
    "name",
    context,
    5,
    3
) == "Marleyan"


# ============================================================
# ERRORES
# ============================================================

try:

    catalog.read(
        "banana",
        context
    )

    assert False

except KeyError:
    pass


try:

    catalog.call(
        "banana",
        context
    )

    assert False

except KeyError:
    pass


print("Perception catalog tests passed")