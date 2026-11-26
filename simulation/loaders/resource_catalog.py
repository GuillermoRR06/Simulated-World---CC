from simulation.model.terrain import Terrain
from simulation.model.world_object import WorldObject


class ResourceCatalog:

    def __init__(self):

        self._terrains_by_char = {}
        self._objects_by_char = {}

        self._terrains_by_name = {}
        self._objects_by_name = {}

        self._first_terrain = None


    def add_terrain(self, terrain: Terrain):

        self._validate_char_available(terrain.char)

        if terrain.name in self._terrains_by_name:
            raise ValueError(
                f"Terrain name already loaded: {terrain.name}"
            )

        self._terrains_by_char[
            terrain.char
        ] = terrain

        self._terrains_by_name[
            terrain.name
        ] = terrain

        if self._first_terrain is None:
            self._first_terrain = terrain


    def add_object(
        self,
        world_object: WorldObject
    ):

        self._validate_char_available(
            world_object.char
        )

        if world_object.name in self._objects_by_name:
            raise ValueError(
                f"Object name already loaded: {world_object.name}"
            )

        self._objects_by_char[
            world_object.char
        ] = world_object

        self._objects_by_name[
            world_object.name
        ] = world_object


    def get_terrain_by_char(
        self,
        char: str
    ):

        return self._terrains_by_char.get(
            char
        )


    def get_object_by_char(
        self,
        char: str
    ):

        return self._objects_by_char.get(
            char
        )


    @property
    def first_terrain(self):

        if self._first_terrain is None:
            raise ValueError(
                "No terrain has been loaded"
            )

        return self._first_terrain


    def _validate_char_available(
        self,
        char: str
    ):

        if (
            char in self._terrains_by_char
            or char in self._objects_by_char
        ):
            raise ValueError(
                f"Character already in use: {char}"
            )