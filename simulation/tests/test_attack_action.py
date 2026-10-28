from simulation.actions.attack_action import AttackAction
from simulation.model.creature import Creature
from simulation.model.species import Species
from simulation.model.terrain import Terrain
from simulation.model.world import World
from simulation.model.world_object import WorldObject


# -----------------------------
# Preparación del mundo
# -----------------------------

grass = Terrain(
    "Grass",
    ".",
    100,
    2
)

attacker_species = Species(
    "Attacker",
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
    5,
    5,
    grass
)

attacker = Creature(attacker_species)
enemy = Creature(enemy_species)
weak_enemy = Creature(weak_enemy_species)

world.place_creature(attacker, 2, 2)
world.place_creature(enemy, 3, 2)
world.place_creature(weak_enemy, 3, 3)

rock = WorldObject(
    "Rock",
    "#",
    100
)

world.get_cell(1, 2).place_object(rock)

attack = AttackAction()

# -----------------------------
# 1. Atacar una criatura
# -----------------------------

attack.execute(
    world,
    attacker,
    1,
    0,
    30
)

assert enemy.health == 70

assert world.get_cell(
    3,
    2
).creature is enemy

# -----------------------------
# 2. Muerte inmediata
# -----------------------------

attack.execute(
    world,
    attacker,
    1,
    1,
    25
)

assert weak_enemy.health <= 0

assert weak_enemy.x is None
assert weak_enemy.y is None

assert world.get_cell(
    3,
    3
).creature is None

# -----------------------------
# 3. Atacar un objeto
# -----------------------------

attack.execute(
    world,
    attacker,
    -1,
    0,
    40
)

assert rock.resource == 60

assert world.get_cell(
    1,
    2
).world_object is rock

# -----------------------------
# 4. Atacar terreno
# -----------------------------

attack.execute(
    world,
    attacker,
    0,
    -1,
    20
)

assert world.get_cell(
    2,
    1
).terrain.resource == 80

# -----------------------------
# 5. attack(0, 0, damage)
# -----------------------------

health_before = attacker.health

attack.execute(
    world,
    attacker,
    0,
    0,
    15
)

assert attacker.health == health_before

assert world.get_cell(
    2,
    2
).terrain.resource == 85

# -----------------------------
# 6. Atacar fuera del mapa
# -----------------------------

edge_attacker = Creature(
    attacker_species
)

world.place_creature(
    edge_attacker,
    0,
    0
)

attack.execute(
    world,
    edge_attacker,
    -1,
    0,
    50
)

assert edge_attacker.health == 100

assert world.get_cell(
    0,
    0
).creature is edge_attacker

print("AttackAction tests passed")