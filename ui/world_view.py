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

from PySide6.QtCore import Qt, Signal

from simulation.model.world import World


class WorldView(QGraphicsView):

    selection_changed = Signal(object)
    cell_clicked = Signal(int, int)

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

        self.draw_world()

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

    def _draw_cell(
        self,
        x,
        y,
        cell
    ):

        screen_x = x * self.cell_size
        screen_y = y * self.cell_size


        # ==========================================
        # TERRENO
        # ==========================================

        rect = QGraphicsRectItem(
            screen_x,
            screen_y,
            self.cell_size,
            self.cell_size
        )

        terrain_color = self._terrain_color(
            cell.terrain.name
        )

        rect.setBrush(
            QBrush(terrain_color)
        )


        # ==========================================
        # SELECCIÓN
        # ==========================================

        if (
            self.selected_creature is not None
            and cell.creature is self.selected_creature
        ):

            selection_pen = QPen(
                Qt.GlobalColor.yellow
            )

            selection_pen.setWidth(3)

            rect.setPen(
                selection_pen
            )

        else:

            rect.setPen(
                QPen(
                    QColor("#303030")
                )
            )


        self.scene.addItem(
            rect
        )


        # ==========================================
        # OBJETO
        # ==========================================

        if cell.world_object is not None:

            margin = 8

            object_item = self.scene.addRect(
                screen_x + margin,
                screen_y + margin,
                self.cell_size - 2 * margin,
                self.cell_size - 2 * margin,
            )

            object_item.setBrush(
                QBrush(
                    QColor("#666666")
                )
            )

            object_item.setPen(
                QPen(
                    QColor("#222222")
                )
            )

            char = cell.world_object.char

            self._draw_centered_text(
                char,
                screen_x,
                screen_y
            )

            return


        # ==========================================
        # CRIATURA
        # ==========================================

        if cell.creature is not None:

            creature = cell.creature

            margin = 6

            creature_item = self.scene.addEllipse(
                screen_x + margin,
                screen_y + margin,
                self.cell_size - 2 * margin,
                self.cell_size - 2 * margin,
            )

            creature_item.setBrush(
                QBrush(
                    self._faction_color(
                        creature.species.faction
                    )
                )
            )

            creature_item.setPen(
                QPen(
                    QColor("#202020")
                )
            )


            # Primera letra del nombre de la especie.
            char = creature.species.name[0].upper()

            self._draw_centered_text(
                char,
                screen_x,
                screen_y
            )

    def mousePressEvent(self, event):

        scene_position = self.mapToScene(
            event.position().toPoint()
        )

        x = int(
            scene_position.x()
            // self.cell_size
        )

        y = int(
            scene_position.y()
            // self.cell_size
        )

        if not self.world.is_inside(x, y):
            return

        if event.button() == Qt.MouseButton.LeftButton:

            self.cell_clicked.emit(x, y)

        cell = self.world.get_cell(x, y)

        self.selected_creature = cell.creature

        self.selection_changed.emit(
            self.selected_creature
        )

        self.draw_world()


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