from simulation.model.species import Species


eldian = Species(
    "Eldian",
    "eldia",
    100,
    5,
    80
)

assert eldian.name == "Eldian"
assert eldian.faction == "eldia"
assert eldian.max_health == 100
assert eldian.vision == 5
assert eldian.lifespan == 80

try:
    invalid_species = Species(
        "Invalid",
        "test",
        -10,
        5,
        80
    )

    raise AssertionError(
        "Expected ValueError for invalid maximum health"
    )

except ValueError:
    pass

print("Species tests passed")