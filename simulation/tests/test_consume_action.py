from simulation.actions.consume_action import ConsumeAction
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

consumer_species = Species(
    "Consumer",
    "faction_a",
    100,
    5,
    100
)

enemy_species = Species(
    "Enemy",
    "faction_b",
    100,
    5,
    100
)

weak_enemy_species = Species(
    "WeakEnemy",
    "faction_b",
    20,
    5,
    100
)

world = World(
    6,
    6,
    grass
)

consumer = Creature(
    consumer_species
)

enemy = Creature(
    enemy_species
)

weak_enemy = Creature(
    weak_enemy_species
)

world.place_creature(
    consumer,
    2,
    2
)

world.place_creature(
    enemy,
    3,
    2
)

world.place_creature(
    weak_enemy,
    3,
    3
)

rock = WorldObject(
    "Rock",
    "#",
    100
)

world.get_cell(
    1,
    2
).place_object(rock)

consume = ConsumeAction()


# 1. Consumir criatura

consumer.health = 50

consume.execute(
    world,
    consumer,
    1,
    0,
    30,
    15
)

assert enemy.health == 70
assert consumer.health == 65
assert world.get_cell(3, 2).creature is enemy


# 2. Consumir y matar criatura

health_before = consumer.health

consume.execute(
    world,
    consumer,
    1,
    1,
    25,
    10
)

assert weak_enemy.health <= 0
assert consumer.health == health_before + 10

assert weak_enemy.x is None
assert weak_enemy.y is None

assert world.get_cell(
    3,
    3
).creature is None


# 3. Consumir objeto

health_before = consumer.health

consume.execute(
    world,
    consumer,
    -1,
    0,
    40,
    20
)

assert rock.resource == 60
assert consumer.health == health_before + 20

assert world.get_cell(
    1,
    2
).world_object is rock


# 4. Consumir terreno

health_before = consumer.health

consume.execute(
    world,
    consumer,
    0,
    -1,
    25,
    10
)

assert world.get_cell(
    2,
    1
).terrain.resource == 75

assert consumer.health == health_before + 10


# 5. Consumir terreno debajo

health_before = consumer.health

consume.execute(
    world,
    consumer,
    0,
    0,
    30,
    15
)

assert world.get_cell(
    2,
    2
).terrain.resource == 70

assert consumer.health == health_before + 15


# 6. Fuera del mapa

edge_consumer = Creature(
    consumer_species
)

world.place_creature(
    edge_consumer,
    0,
    0
)

edge_consumer.health = 40

consume.execute(
    world,
    edge_consumer,
    -1,
    0,
    50,
    30
)

assert edge_consumer.health == 40
assert world.get_cell(0, 0).creature is edge_consumer


# 7. No existe health máximo

consumer.health = 95

consume.execute(
    world,
    consumer,
    0,
    0,
    0,
    20
)

assert consumer.health == 115


print("ConsumeAction tests passed")