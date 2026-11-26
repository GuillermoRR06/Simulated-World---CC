from simulation.loaders.application_loader import ApplicationLoader


loader = ApplicationLoader()

loader.load()


# Test 1: cargar terrenos

grass = loader.catalog.get_terrain_by_char(".")

assert grass is not None
assert grass.name == "Grass"


# Test 2: cargar objetos

rock = loader.catalog.get_object_by_char("#")

assert rock is not None
assert rock.name == "Rock"


# Test 3: cargar mapas

assert len(loader.maps) > 0

assert any(
    map_definition.name == "Plain with rocks"
    for map_definition in loader.maps
)


# Mostrar mapas disponibles

print("Available maps:")

for map_definition in loader.maps:

    print(
        map_definition.name,
        map_definition.width,
        map_definition.height
    )


# Mostrar errores de carga

print("\nLoading errors:")

for error in loader.errors:

    print(error)


print("\nApplication loader tests passed")