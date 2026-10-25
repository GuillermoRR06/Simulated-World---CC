from simulation.model.terrain import Terrain
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


# --------------------------------
# Criatura que morirá por health
# --------------------------------

weak_species = Species(
    "WeakCreature",
    "test",
    1,      # health inicial
    5,      # vision
    100     # lifespan
)

weak_creature = Creature(weak_species)


# --------------------------------
# Criatura que morirá por edad
# --------------------------------

old_species = Species(
    "OldCreature",
    "test",
    100,    # health inicial
    5,      # vision
    1       # lifespan
)

old_creature = Creature(old_species)


# --------------------------------
# Mundo
# --------------------------------

world = World(
    5,
    5,
    grass
)

world.place_creature(
    weak_creature,
    1,
    1
)

world.place_creature(
    old_creature,
    3,
    3
)


simulator = Simulator(
    world,
    seed=42
)


# Ejecutamos un tick
simulator.advance_tick()


# --------------------------------
# Muerte por health
# --------------------------------

assert weak_creature.health == 0
assert weak_creature.age == 1

assert weak_creature.x is None
assert weak_creature.y is None

assert world.get_cell(
    1,
    1
).creature is None


# --------------------------------
# Muerte por lifespan
# --------------------------------

assert old_creature.health == 99
assert old_creature.age == 1

assert old_creature.x is None
assert old_creature.y is None

assert world.get_cell(
    3,
    3
).creature is None


# No debe quedar ninguna criatura
assert len(world.get_creatures()) == 0


print("Death rules tests passed")