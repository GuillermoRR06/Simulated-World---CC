from simulation.model.terrain import Terrain


class TerrainLoader:

    def load(self, file_path: str) -> Terrain:

        data = {}

        with open(file_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                parts = line.split(maxsplit=1)

                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid line {line_number}: {line}"
                    )

                key, value = parts

                data[key] = value

        required = {
            "terrain",
            "char",
            "resource_max",
            "regen",
        }

        missing = required - data.keys()

        if missing:
            raise ValueError(
                f"Missing terrain fields: {missing}"
            )

        char = data["char"]

        if len(char) != 1:
            raise ValueError(
                "Terrain char must contain exactly one character"
            )

        return Terrain(
            name=data["terrain"],
            char=char,
            resource_max=int(
                data["resource_max"]
            ),
            regen=int(
                data["regen"]
            ),
        )