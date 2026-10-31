from random import Random

from simulation.model.terrain import Terrain
from simulation.model.species import Species
from simulation.model.creature import Creature
from simulation.model.world import World

from simulation.perceptions.perceptions import PerceptionContext

from simulation.perceptions.self_perceptions import (
    HealthPerception,
    AgePerception,
    LifespanPerception,
    VisionPerception,
    SpeciesPerception,
    FactionPerception,
    XPerception,
    YPerception,
    TerrainHerePerception,
    ReserveHerePerception,
)


# --------------------------------
# Preparar el mundo
# --------------------------------

grass = Terrain(
    "Grass",
    ".",
    100,
    2
)

world = World(
    5,
    5,
    grass
)


# --------------------------------
# Crear una especie
# --------------------------------

eldian = Species(
    "Eldian",
    "eldia",
    100,
    4,
    200
)


# --------------------------------
# Crear criatura
# --------------------------------

creature = Creature(
    eldian
)

world.place_creature(
    creature,
    2,
    3
)


# Cambiamos algunos valores para
# que el test sea más interesante.

creature.health = 73
creature.age = 15


# --------------------------------
# Crear el contexto
# --------------------------------

rng = Random(42)

context = PerceptionContext(
    world=world,
    creature=creature,
    tick=10,
    rng=rng
)


# --------------------------------
# Percepciones de la criatura
# --------------------------------

assert HealthPerception().read(context) == 73

assert AgePerception().read(context) == 15

assert LifespanPerception().read(context) == 200

assert VisionPerception().read(context) == 4

assert SpeciesPerception().read(context) == "Eldian"

assert FactionPerception().read(context) == "eldia"

assert XPerception().read(context) == 2

assert YPerception().read(context) == 3


# --------------------------------
# Percepciones del terreno actual
# --------------------------------

assert TerrainHerePerception().read(context) == "Grass"

assert ReserveHerePerception().read(context) == 100


# --------------------------------
# Comprobar que la percepción
# lee el estado ACTUAL
# --------------------------------

creature.health = 45

assert HealthPerception().read(context) == 45


# Modificamos la reserva del terreno

cell = world.get_cell(
    creature.x,
    creature.y
)

cell.terrain.resource = 60

assert ReserveHerePerception().read(context) == 60


print("Self perceptions tests passed")