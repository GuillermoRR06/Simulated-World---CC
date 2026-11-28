from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class AssetManager:
    def __init__(self):
        self.assets_dir = (
            Path(__file__).resolve().parents[1] / "assets"
        )

        self._files = {
            ("terrain", "grass"): "terrains/grass.png",
            ("object", "rock"): "objects/rock.png",
            ("creature", "eldian"): "creatures/eldian.png",
            ("object", "wall"): "objects/wall.png",
            ("object", "tree"): "objects/tree.png",
            ("creature", "marleyan"): "creatures/marleyan.png",
            ("creature", "puretitan"): "creatures/pure_titan.png",
            ("object", "house"): "objects/house.png",
        }

        self._cache: dict[tuple[str, int], QPixmap | None] = {}

    def get(
        self,
        category: str,
        name: str,
        size: int,
    ) -> QPixmap | None:
        if size <= 0:
            raise ValueError("Image size must be positive")

        relative_path = self._files.get(
            (category, name.lower())
        )

        if relative_path is None:
            return None

        key = (relative_path, size)

        if key in self._cache:
            return self._cache[key]

        path = self.assets_dir / relative_path
        pixmap = QPixmap(str(path))

        if pixmap.isNull():
            print(f"[Assets] No se pudo cargar: {path}")
            self._cache[key] = None
            return None

        pixmap = pixmap.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )

        self._cache[key] = pixmap
        return pixmap
