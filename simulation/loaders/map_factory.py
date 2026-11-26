from simulation.model.world import World
from simulation.model.map_definition import MapDefinition
from simulation.loaders.resource_catalog import ResourceCatalog


class MapFactory:

    def __init__(self, catalog: ResourceCatalog):

        self.catalog = catalog


    def create_world(
        self,
        map_definition: MapDefinition
    ) -> World:

        world = World(
            map_definition.width,
            map_definition.height,
            self.catalog.first_terrain
        )

        for y, row in enumerate(map_definition.rows):

            for x, char in enumerate(row):

                cell = world.get_cell(x, y)

                terrain = self.catalog.get_terrain_by_char(char)

                if terrain is not None:

                    cell.terrain = terrain.new_instance()

                    continue

                world_object = self.catalog.get_object_by_char(char)

                if world_object is not None:

                    cell.terrain = (
                        self.catalog.first_terrain.new_instance()
                    )

                    cell.world_object = world_object.new_instance()

                    continue

                raise ValueError(
                    f"Unknown map character '{char}' "
                    f"at line {y + 2}"
                )

        return world