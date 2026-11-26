from pathlib import Path

from simulation.loaders.terrain_loader import TerrainLoader
from simulation.loaders.object_loader import ObjectLoader
from simulation.loaders.map_loader import MapLoader
from simulation.loaders.resource_catalog import ResourceCatalog
from simulation.model.map_definition import MapDefinition


class ApplicationLoader:

    def __init__(self, root_path: str = "."):

        self.root_path = Path(root_path)

        self.catalog = ResourceCatalog()

        self.maps: list[MapDefinition] = []

        self.errors: list[str] = []


    def load(self) -> None:

        self.catalog = ResourceCatalog()
        self.maps.clear()
        self.errors.clear()

        self._load_directory(
            "terrains",
            ".te",
            TerrainLoader().load,
            self.catalog.add_terrain
        )

        self._load_directory(
            "objects",
            ".ob",
            ObjectLoader().load,
            self.catalog.add_object
        )

        self._load_directory(
            "maps",
            ".map",
            MapLoader(self.catalog).load,
            self.maps.append
        )


    def _load_directory(
        self,
        directory,
        extension,
        load_file,
        register
    ):

        folder = self.root_path / directory

        if not folder.is_dir():

            self.errors.append(
                f"Directory not found: {folder}"
            )

            return

        for file_path in sorted(folder.glob(f"*{extension}")):

            if not file_path.is_file():
                continue

            try:

                resource = load_file(str(file_path))

                register(resource)

            except (ValueError, OSError) as error:

                self.errors.append(
                    f"{file_path}: {error}"
                )