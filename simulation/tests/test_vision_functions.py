from random import Random

from simulation.model.terrain import Terrain
from simulation.model.world_object import WorldObject
from simulation.model.species import Species
from simulation.model.creature import Creature
from simulation.model.world import World

from simulation.perceptions.perceptions import (
    PerceptionContext
)

from simulation.perceptions.vision_functions import (
    NONE,
    GROUND,
    OBJECT,
    ALLY,
    ENEMY,
    see,
    name,
)


# ============================================================
# MUNDO
# ============================================================

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


# ============================================================
# ESPECIES
# ============================================================

eldian = Species(
    "Eldian",
    "eldia",
    100,
    2,          # vision = 2
    100
)

scout = Species(
    "Scout",
    "eldia",
    100,
    2,
    100
)

marleyan = Species(
    "Marleyan",
    "marley",
    100,
    2,
    100
)


# ============================================================
# CRIATURAS
# ============================================================

observer = Creature(
    eldian
)

ally = Creature(
    scout
)

enemy = Creature(
    marleyan
)


world.place_creature(
    observer,
    2,
    2
)

world.place_creature(
    ally,
    3,
    2
)

world.place_creature(
    enemy,
    2,
    4
)


# ============================================================
# OBJETO
# ============================================================

rock = WorldObject(
    "Rock",
    "#",
    100
)

world.get_cell(
    1,
    1
).place_object(
    rock
)


# ============================================================
# CONTEXTO
# ============================================================

context = PerceptionContext(
    world=world,
    creature=observer,
    tick=0,
    rng=Random(42)
)


# ============================================================
# 1. CONSTANTES
# ============================================================

assert NONE == -1
assert GROUND == 0
assert OBJECT == 1
assert ALLY == 2
assert ENEMY == 3


# ============================================================
# 2. TERRENO
# ============================================================

assert see(
    context,
    3,
    3
) == GROUND

assert name(
    context,
    3,
    3
) == "Grass"


# ============================================================
# 3. OBJETO
# ============================================================

assert see(
    context,
    1,
    1
) == OBJECT

assert name(
    context,
    1,
    1
) == "Rock"


# ============================================================
# 4. ALIADO
# ============================================================

assert see(
    context,
    3,
    2
) == ALLY

assert name(
    context,
    3,
    2
) == "Scout"


# ============================================================
# 5. ENEMIGO
# ============================================================

assert see(
    context,
    2,
    4
) == ENEMY

assert name(
    context,
    2,
    4
) == "Marleyan"


# ============================================================
# 6. PROPIA CASILLA
# ============================================================

assert see(
    context,
    2,
    2
) == ALLY

assert name(
    context,
    2,
    2
) == "Eldian"


# ============================================================
# 7. FUERA DEL RADIO DE VISION
# ============================================================

# Desde (2,2) hasta (5,2):
# distancia = 3
# vision = 2

assert see(
    context,
    5,
    2
) == NONE

assert name(
    context,
    5,
    2
) == ""


# ============================================================
# 8. FUERA DEL MAPA PERO DENTRO DE VISION
# ============================================================

# El observador está en (2,2), así que (-1,2)
# estaría a distancia 3 y NO serviría.
#
# Para probar el borde creamos otro observador cerca del borde.

edge_observer = Creature(
    eldian
)

world.place_creature(
    edge_observer,
    0,
    6
)

edge_context = PerceptionContext(
    world=world,
    creature=edge_observer,
    tick=0,
    rng=Random(42)
)


# (-1,6) está fuera del mapa,
# pero a distancia 1.

assert see(
    edge_context,
    -1,
    6
) == OBJECT

assert name(
    edge_context,
    -1,
    6
) == ""


# ============================================================
# 9. FUERA DEL MAPA Y FUERA DE VISION
# ============================================================

assert see(
    edge_context,
    -5,
    6
) == NONE

assert name(
    edge_context,
    -5,
    6
) == ""


print("Vision functions tests passed")