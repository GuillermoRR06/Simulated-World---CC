from simulation.model.world_object import WorldObject


class ObjectLoader:

    def load(self, file_path: str) -> WorldObject:

        data = {}

        with open(file_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                parts = line.split(
                    maxsplit=1
                )

                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid line {line_number}: {line}"
                    )

                key, value = parts

                data[key] = value

        required = {
            "object",
            "char",
            "resource_max",
        }

        missing = required - data.keys()

        if missing:
            raise ValueError(
                f"Missing object fields: {missing}"
            )

        char = data["char"]

        if len(char) != 1:
            raise ValueError(
                "Object char must contain exactly one character"
            )

        return WorldObject(
            name=data["object"],
            char=char,
            resource_max=int(
                data["resource_max"]
            ),
        )