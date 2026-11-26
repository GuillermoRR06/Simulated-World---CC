from simulation.model.map_definition import (
    MapDefinition
)

from simulation.loaders.resource_catalog import (
    ResourceCatalog
)


class MapLoader:

    def __init__(
        self,
        catalog: ResourceCatalog
    ):

        self.catalog = catalog


    def load(
        self,
        file_path: str
    ) -> MapDefinition:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            lines = [
                line.rstrip("\n")
                for line in file
            ]


        if not lines:
            raise ValueError(
                "Map file is empty"
            )


        name = lines[0].strip()

        if not name:
            raise ValueError(
                "Map name cannot be empty"
            )


        rows = lines[1:]

        if not rows:
            raise ValueError(
                "Map must contain at least one row"
            )


        expected_width = len(
            rows[0]
        )


        if expected_width == 0:
            raise ValueError(
                "Map rows cannot be empty"
            )


        for row_index, row in enumerate(
            rows,
            start=2
        ):

            if len(row) != expected_width:

                raise ValueError(
                    f"Invalid map row length "
                    f"at line {row_index}"
                )


            for char in row:

                terrain = (
                    self.catalog
                    .get_terrain_by_char(char)
                )

                world_object = (
                    self.catalog
                    .get_object_by_char(char)
                )


                if (
                    terrain is None
                    and world_object is None
                ):

                    raise ValueError(
                        f"Unknown map character "
                        f"'{char}' "
                        f"at line {row_index}"
                    )


        return MapDefinition(
            name=name,
            rows=rows
        )