from simulation.loaders.object_loader import ObjectLoader


loader = ObjectLoader()

rock = loader.load(
    "objects/rock.ob"
)


assert rock.name == "Rock"

assert rock.char == "#"

assert rock.resource_max == 100

assert rock.resource == 100


print(
    "Object loader tests passed"
)