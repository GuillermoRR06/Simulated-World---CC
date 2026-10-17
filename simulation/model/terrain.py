# Resource no entra como parámetro porque el terreno empieza con la reserva llena
class Terrain:
    def __init__(self, name: str, char: str, resource_max: int, regen: int):
        self.name = name
        self.char = char
        self.resource_max = resource_max
        self.regen = regen
        self.resource = resource_max

    def regenerate(self):
        self.resource = min(
            self.resource + self.regen,
            self.resource_max
        )

    def new_instance(self):
        return Terrain(
            self.name,
            self.char,
            self.resource_max,
            self.regen
        )