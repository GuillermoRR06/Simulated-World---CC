from PySide6.QtCore import Qt, QRectF

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QImage,
)

from PySide6.QtWidgets import QWidget

from .world_view import WorldView


class MiniMap(QWidget):

    def __init__(self, world_view: WorldView):

        super().__init__()

        self.world_view = world_view

        self.setFixedHeight(110)

        self.setToolTip(
            "Pulsa para desplazar la cámara"
        )


    def _map_rect(self):

        world = self.world_view.world

        available_width = max(1, self.width() - 12)

        available_height = max(1, self.height() - 12)

        scale = min(
            available_width / world.width,
            available_height / world.height
        )

        width = world.width * scale

        height = world.height * scale

        return QRectF(
            (self.width() - width) / 2,
            (self.height() - height) / 2,
            width,
            height
        )

    def _cell_color(self, cell):

        if cell.creature is not None:

            faction = (
                cell.creature.species.faction.lower()
            )

            colors = {
                "eldia": "#7CB9E8",
                "marley": "#E0D4AE",
                "titans": "#E08060",
            }

            return QColor(
                colors.get(faction, "#D0A5E8")
            )

        if cell.world_object is not None:

            name = cell.world_object.name.lower()

            colors = {
                "wall": "#BFC2C5",
                "tree": "#294C32",
                "rock": "#777777",
            }

            return QColor(
                colors.get(name, "#8D8D8D")
            )

        name = cell.terrain.name.lower()

        colors = {
            "grass": "#718640",
            "forest": "#466B39",
            "water": "#548EB5",
            "sand": "#C8B27D",
        }

        return QColor(
            colors.get(name, "#8FAF7A")
        )

    def paintEvent(self, event):

        world = self.world_view.world

        painter = QPainter(self)

        painter.fillRect(
            self.rect(),
            QColor("#101D27")
        )

        area = self._map_rect()

        image = QImage(
            world.width,
            world.height,
            QImage.Format.Format_RGB32
        )

        for y, row in enumerate(world.grid):

            for x, cell in enumerate(row):

                image.setPixelColor(
                    x,
                    y,
                    self._cell_color(cell)
                )

        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform,
            False
        )

        painter.drawImage(
            area,
            image
        )

        self._draw_camera(
            painter,
            area
        )

        painter.end()

    def _draw_camera(self, painter, area):

        view = self.world_view

        world = view.world

        visible = view.mapToScene(
            view.viewport().rect()
        ).boundingRect()

        world_rect = QRectF(
            0,
            0,
            world.width * view.cell_size,
            world.height * view.cell_size
        )

        visible = visible.intersected(
            world_rect
        )

        if visible.isEmpty():
            return

        scale_x = (
            area.width() / world_rect.width()
        )

        scale_y = (
            area.height() / world_rect.height()
        )

        camera_rect = QRectF(
            area.x() + visible.x() * scale_x,
            area.y() + visible.y() * scale_y,
            visible.width() * scale_x,
            visible.height() * scale_y
        )

        pen = QPen(QColor("#FFE19A"))

        pen.setWidthF(1.5)

        painter.setPen(pen)

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawRect(camera_rect)

    def mousePressEvent(self, event):

        if event.button() != Qt.MouseButton.LeftButton:

            super().mousePressEvent(event)

            return

        area = self._map_rect()

        position = event.position()

        if not area.contains(position):
            return

        world = self.world_view.world

        relative_x = (
            (position.x() - area.x())
            / area.width()
        )

        relative_y = (
            (position.y() - area.y())
            / area.height()
        )

        scene_x = (
            relative_x
            * world.width
            * self.world_view.cell_size
        )

        scene_y = (
            relative_y
            * world.height
            * self.world_view.cell_size
        )

        self.world_view.centerOn(
            scene_x,
            scene_y
        )

        self.update()

        event.accept()