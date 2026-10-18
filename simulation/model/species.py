class Species:
    def __init__(
        self,
        name: str,
        faction: str,
        initial_health: int,
        vision: int,
        lifespan: int
    ):
        if initial_health <= 0:
            raise ValueError("Initial health must be positive")

        if vision < 1:
            raise ValueError("Vision must be at least 1")

        if lifespan <= 0:
            raise ValueError("Lifespan must be positive")

        self.name = name
        self.faction = faction
        self.initial_health = initial_health
        self.vision = vision
        self.lifespan = lifespan