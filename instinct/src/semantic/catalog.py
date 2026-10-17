class Catalog:
    def __init__(self):
        self.actions: dict[str, int] = {}
        self.functions: dict[str, int] = {}
        self.perceptions: set[str] = set()
        self.constants: dict[str, int | str] = {}

    # Seccion para registrar nuevas acciones/funciones/percepciones/constantes
    def Register_Action(self, name: str, arity: int):
        if name in self.actions or name in self.functions:
            raise ValueError(f"Ya existe una accion o funcion llamada '{name}'")
        self.actions[name] = arity

    def Register_Function(self, name: str, arity: int):
        if name in self.actions or name in self.functions:
            raise ValueError(f"Ya existe una accion o funcion llamada '{name}'")
        self.functions[name] = arity

    def Register_Perception(self, name: str):
        if name in self.perceptions or name in self.constants:
            raise ValueError(f"Ya existe una percepcion o constante llamada '{name}'")
        self.perceptions.add(name)

    def Register_Constant(self, name: str, value: int | str):
        if name in self.perceptions or name in self.constants:
            raise ValueError(f"Ya existe una percepcion o constante llamada '{name}'")
        self.constants[name] = value

    # Acceder a las acciones/funciones/percepciones/constantes
    def action_arity(self, name: str) -> int | None:
        return self.actions.get(name)

    def function_arity(self, name: str) -> int | None:
        return self.functions.get(name)

    def is_perception(self, name: str) -> bool:
        return name in self.perceptions

    def is_constant(self, name: str) -> bool:
        return name in self.constants

    def constant_value(self, name: str) -> int | str:
        return self.constants[name]

# Acciones/Funciones/Percepciones/Constantes definidas en la base del lenguaje
BASE_ACTIONS = {
    "wait": 1, "move": 3, "attack": 3, "consume": 4,
    "reproduce": 3, "roar": 1, "say": 1,
}

BASE_FUNCTIONS = {"see": 2, "name": 2}

BASE_CONSTANTS = {"NONE": -1, "GROUND": 0, "OBJECT": 1, "ALLY": 2, "ENEMY": 3}

BASE_PERCEPTIONS = (
    "health", "age", "lifespan", "vision", "species", "faction",
    "x", "y", "terrain_here", "reserve_here",

    "width", "height", "tick",
    "total_creatures", "total_allies", "total_enemies", "random",

    "allies_near", "enemies_near", "objects_near",
    "enemy_dist", "enemy_dx", "enemy_dy",
    "ally_dist", "ally_dx", "ally_dy",
    "object_dist", "object_dx", "object_dy",
    "roars_near", "last_roar",
)

def default_catalog() -> Catalog:
    catalog = Catalog()
    for name, arity in BASE_ACTIONS.items():
        catalog.register_action(name, arity)
    for name, arity in BASE_FUNCTIONS.items():
        catalog.register_function(name, arity)
    for name, value in BASE_CONSTANTS.items():
        catalog.register_constant(name, value)
    for name in BASE_PERCEPTIONS:
        catalog.register_perception(name)
    return catalog