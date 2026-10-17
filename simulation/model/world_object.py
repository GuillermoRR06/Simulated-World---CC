class WorldObject:
    def __init__(self, name:str, char:str, resource_max:int):
        self.name = name
        self.char = char
        self.resource_max = resource_max
        self.resource = resource_max