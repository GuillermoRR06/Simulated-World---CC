from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsTextItem,
)

from PySide6.QtGui import (
    QBrush,
    QPen,
    QColor,
)
from .asset_manager import AssetManager

from PySide6.QtCore import Qt, Signal

from simulation.model.world import World


class WorldView(QGraphicsView):

    selection_changed = Signal(object)
    cell_clicked = Signal(int, int)
    view_changed = Signal()

    def __init__(
        self,
        world: World,
        cell_size: int = 40
    ):
        super().__init__()

        self.world = world
        self.cell_size = cell_size

        self.selected_creature = None

        self.scene = QGraphicsScene()

        self.setScene(
            self.scene
        )

        self.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )

        self.assets = AssetManager()

        self.draw_world()

        self._min_zoom = 0.5
        
        self._max_zoom = 3.0
        
        self._pan_last_pos = None
        
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        
        self.setMouseTracking(True)


    def draw_world(self):
        self.scene.clear()

        self.scene.setSceneRect(
            0,
            0,
            self.world.width * self.cell_size,
            self.world.height * self.cell_size,
        )

        for y, row in enumerate(
            self.world.grid
        ):
            for x, cell in enumerate(row):
                self._draw_cell(
                    x,
                    y,
                    cell
                )
        self.view_changed.emit()

    def _draw_cell(self, x, y, cell):
        screen_x = x * self.cell_size
        screen_y = y * self.cell_size
        size = self.cell_size

        # Color de fondo, visible si no hay textura.
        background = self.scene.addRect(
            screen_x,
            screen_y,
            size,
            size,
            QPen(Qt.PenStyle.NoPen),
            QBrush(
                self._terrain_color(cell.terrain.name)
            ),
        )

        background.setZValue(-1)

        # Textura del terreno.
        self._draw_sprite(
            "terrain",
            cell.terrain.name,
            screen_x,
            screen_y,
            0,
        )

        # Objeto sobre el terreno.
        if cell.world_object is not None:
            world_object = cell.world_object

            drawn = self._draw_sprite(
                "object",
                world_object.name,
                screen_x,
                screen_y,
                1,
            )

            if not drawn:
                margin = 8

                item = self.scene.addRect(
                    screen_x + margin,
                    screen_y + margin,
                    size - 2 * margin,
                    size - 2 * margin,
                    QPen(QColor("#222222")),
                    QBrush(QColor("#666666")),
                )

                item.setZValue(1)

                self._draw_centered_text(
                    world_object.char,
                    screen_x,
                    screen_y,
                )

        # Criatura sobre el terreno.
        elif cell.creature is not None:
            creature = cell.creature

            drawn = self._draw_sprite(
                "creature",
                creature.species.name,
                screen_x,
                screen_y,
                1,
            )

            if not drawn:
                margin = 6

                item = self.scene.addEllipse(
                    screen_x + margin,
                    screen_y + margin,
                    size - 2 * margin,
                    size - 2 * margin,
                    QPen(QColor("#202020")),
                    QBrush(
                        self._faction_color(
                            creature.species.faction
                        )
                    ),
                )

                item.setZValue(1)

                self._draw_centered_text(
                    creature.species.name[:1].upper(),
                    screen_x,
                    screen_y,
                )

        # Selección encima de todas las imágenes.
        if (
            self.selected_creature is not None
            and cell.creature is self.selected_creature
        ):
            pen = QPen(Qt.GlobalColor.yellow)
            pen.setWidth(3)

            selection = self.scene.addRect(
                screen_x + 1.5,
                screen_y + 1.5,
                size - 3,
                size - 3,
                pen,
                QBrush(Qt.BrushStyle.NoBrush),
            )

            selection.setZValue(3)


    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:

            self._pan_last_pos = (
                event.position().toPoint()
            )

            self.viewport().setCursor(
                Qt.CursorShape.ClosedHandCursor
            )

            event.accept()
            return

        if event.button() != Qt.MouseButton.LeftButton:

            super().mousePressEvent(event)
            return

        scene_position = self.mapToScene(
            event.position().toPoint()
        )

        x = int(
            scene_position.x() // self.cell_size
        )

        y = int(
            scene_position.y() // self.cell_size
        )

        if not self.world.is_inside(x, y):
            return

        self.cell_clicked.emit(x, y)

        cell = self.world.get_cell(x, y)

        self.selected_creature = cell.creature

        self.selection_changed.emit(
            self.selected_creature
        )

        self.draw_world()

        event.accept()



    def _terrain_color(
    self,
    terrain_name: str
) -> QColor:

        name = terrain_name.lower()

        if name == "grass":
            return QColor("#8FAF7A")

        if name == "forest":
            return QColor("#557A46")

        if name == "water":
            return QColor("#6997B7")

        if name == "sand":
            return QColor("#C8B27D")

        return QColor("#A5A5A5")

    def _faction_color(
    self,
    faction: str
) -> QColor:

        name = faction.lower()

        if name == "eldia":
            return QColor("#4E8ABF")

        if name == "marley":
            return QColor("#B55555")

        if name in (
            "titan",
            "titans",
            "titanes"
        ):
            return QColor("#A66BB7")

        return QColor("#888888")

    def _draw_centered_text(
    self,
    value: str,
    screen_x: float,
    screen_y: float
):

        text = QGraphicsTextItem(
            value
        )

        text.setZValue(2)

        text.setDefaultTextColor(
            Qt.GlobalColor.white
        )

        text_rect = text.boundingRect()

        text_x = (
            screen_x
            + (
                self.cell_size
                - text_rect.width()
            ) / 2
        )

        text_y = (
            screen_y
            + (
                self.cell_size
                - text_rect.height()
            ) / 2
        )

        text.setPos(
            text_x,
            text_y
        )

        self.scene.addItem(
            text
        )
    def set_world(
    self,
    world: World
):

        self.world = world

        self.selected_creature = None

        self.draw_world()

        self.reset_view()

    def wheelEvent(self, event):

        delta = event.angleDelta().y()

        if delta == 0:
            super().wheelEvent(event)
            return

        current_zoom = self.transform().m11()

        factor = 1.2 ** (delta / 120)

        target_zoom = current_zoom * factor

        target_zoom = max(
            self._min_zoom,
            min(self._max_zoom, target_zoom)
        )

        real_factor = target_zoom / current_zoom

        self.scale(
            real_factor,
            real_factor
        )

        self.view_changed.emit()

        event.accept()

    def mouseMoveEvent(self, event):

        if self._pan_last_pos is None:

            super().mouseMoveEvent(event)
            return

        current_pos = event.position().toPoint()

        delta = current_pos - self._pan_last_pos

        horizontal = self.horizontalScrollBar()
        vertical = self.verticalScrollBar()

        horizontal.setValue(
            horizontal.value() - delta.x()
        )

        vertical.setValue(
            vertical.value() - delta.y()
        )

        self._pan_last_pos = current_pos

        event.accept()


    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:

            self._pan_last_pos = None

            self.viewport().unsetCursor()

            event.accept()
            return

        super().mouseReleaseEvent(event)

    def reset_view(self):

        self.resetTransform()

        self.centerOn(
            self.sceneRect().center()
        )
        self.view_changed.emit()

    def _draw_sprite(
        self,
        category: str,
        name: str,
        screen_x: float,
        screen_y: float,
        layer: int,
    ) -> bool:
        pixmap = self.assets.get(
            category,
            name,
            self.cell_size,
        )

        if pixmap is None:
            return False

        item = self.scene.addPixmap(pixmap)

        item.setTransformationMode(
            Qt.TransformationMode.FastTransformation
        )

        item.setPos(
            screen_x + (self.cell_size - pixmap.width()) / 2,
            screen_y + (self.cell_size - pixmap.height()) / 2,
        )

        item.setZValue(layer)

        return True

    def scrollContentsBy(self, dx, dy):

        super().scrollContentsBy(dx, dy)

        self.view_changed.emit()

    def resizeEvent(self, event):
    
        super().resizeEvent(event)
    
        self.view_changed.emit()