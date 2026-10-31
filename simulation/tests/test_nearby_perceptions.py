from random import Random

from simulation.model.terrain import Terrain
from simulation.model.species import Species
from simulation.model.creature import Creature
from simulation.model.world import World

from simulation.perceptions.perceptions import (
    PerceptionContext
)

from simulation.perceptions.nearby_perceptions import (
    _visible_roars,
    RoarsNearPerception,
    LastRoarPerception,
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
    9,
    9,
    grass
)


# ============================================================
# ESPECIES
# ============================================================

observer_species = Species(
    "Observer",
    "eldia",
    100,
    3,      # vision = 3
    100
)

marleyan = Species(
    "Marleyan",
    "marley",
    100,
    3,
    100
)


# ============================================================
# CRIATURAS
# ============================================================

observer = Creature(
    observer_species
)

near_creature = Creature(
    marleyan
)

another_near_creature = Creature(
    marleyan
)

far_creature = Creature(
    marleyan
)


world.place_creature(
    observer,
    4,
    4
)

world.place_creature(
    near_creature,
    5,
    4
)

world.place_creature(
    another_near_creature,
    2,
    4
)

world.place_creature(
    far_creature,
    8,
    8
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
# 1. AL PRINCIPIO NO HAY RUGIDOS
# ============================================================

assert RoarsNearPerception().read(
    context
) == 0

assert LastRoarPerception().read(
    context
) == ""


# ============================================================
# 2. GENERAR RUGIDOS EN EL TICK ACTUAL
# ============================================================

world.emit_roar(
    near_creature,
    "First roar"
)

world.emit_roar(
    another_near_creature,
    "Second roar"
)

world.emit_roar(
    far_creature,
    "Far roar"
)


# Todavía están en current_roars.
# Las percepciones NO deben escucharlos todavía.

assert len(
    world.current_roars
) == 3

assert RoarsNearPerception().read(
    context
) == 0

assert LastRoarPerception().read(
    context
) == ""


# ============================================================
# 3. CAMBIAR DE TICK
# ============================================================

world.rotate_roars()


assert len(
    world.current_roars
) == 0

assert len(
    world.previous_roars
) == 3


# ============================================================
# 4. SOLO LOS RUGIDOS VISIBLES
# ============================================================

visible = _visible_roars(
    context
)

# near_creature:
# (5,4) respecto a (4,4)
# distancia = 1
#
# another_near_creature:
# (2,4) respecto a (4,4)
# distancia = 2
#
# far_creature:
# (8,8) respecto a (4,4)
# distancia = 4
#
# vision = 3
#
# Por tanto solo se escuchan los dos primeros.

assert len(visible) == 2


# ============================================================
# 5. ROARS_NEAR
# ============================================================

assert RoarsNearPerception().read(
    context
) == 2


# ============================================================
# 6. LAST_ROAR
# ============================================================

assert LastRoarPerception().read(
    context
) == "Second roar"


print("Roar perceptions tests passed")