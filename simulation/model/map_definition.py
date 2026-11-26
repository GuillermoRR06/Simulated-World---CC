class MapDefinition:

    def __init__(
        self,
        name: str,
        rows: list[str]
    ):

        self.name = name
        self.rows = tuple(rows)


    @property
    def width(self) -> int:

        return len(
            self.rows[0]
        )


    @property
    def height(self) -> int:

        return len(
            self.rows
        )