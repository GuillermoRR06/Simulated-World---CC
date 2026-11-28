from PySide6.QtCore import Signal, QSize, Qt

from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSpinBox,
    QAbstractItemView,
    QListWidget,
    QListWidgetItem,
    QSizePolicy
)

from simulation.model.map_definition import MapDefinition
from simulation.model.species import Species

from .asset_manager import AssetManager

class PreparationPanel(QGroupBox):

    map_requested = Signal(object, int)


    def __init__(
        self,
        available_maps: list[MapDefinition],
        available_species: list[Species]
    ):
        super().__init__("Preparación")

        self.assets = AssetManager()

        self._build_ui(
            available_maps,
            available_species
        )
        self.species_list.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )


    def _build_ui(
        self,
        available_maps: list[MapDefinition],
        available_species: list[Species]
    ):
        layout = QFormLayout(self)

        self._build_species_list(
            available_species)


        layout.addRow(
            QLabel("Unidades:")
        )
        layout.addRow(
            self.species_list
        )


        self.map_combo = QComboBox()

        for map_definition in available_maps:
            self.map_combo.addItem(
                map_definition.name,
                map_definition,
            )

        self.dimensions_label = QLabel()

        self.seed_input = QSpinBox()
        self.seed_input.setRange(
            -999999999,
            999999999
        )
        self.seed_input.setValue(42)

        self.seed_input.setKeyboardTracking(False)


        layout.addRow(
            "Mapa:",
            self.map_combo
        )

        layout.addRow(
            "Dimensiones:",
            self.dimensions_label
        )

        layout.addRow(
            "Semilla:",
            self.seed_input
        )



        self.mode_combo = QComboBox()

        self.mode_combo.addItem(
            "Inspeccionar",
            "inspect"
        )

        self.mode_combo.addItem(
            "Colocar",
            "place"
        )

        self.mode_combo.addItem(
            "Eliminar",
            "remove"
        )


        layout.addRow(
            "Modo:",
            self.mode_combo
        )
        self.map_combo.currentIndexChanged.connect(
            self._update_dimensions
        )

        self.map_combo.currentIndexChanged.connect(
            self._request_map
        )

        self.seed_input.valueChanged.connect(
            self._request_map
        )

        self._update_dimensions()



    def _update_dimensions(
        self,
        index: int = -1
    ):
        map_definition = self.map_combo.currentData()

        if map_definition is None:

            self.dimensions_label.setText(
                "Sin mapas disponibles"
            )

            return

        self.dimensions_label.setText(
            f"{map_definition.width} x "
            f"{map_definition.height}"
        )

    def _request_map(self, *_args):
        map_definition = (
            self.map_combo.currentData()
        )

        if map_definition is None:
            return

        self.map_requested.emit(
            map_definition,
            self.seed_input.value(),
        )

    def selected_species(self) -> Species | None:
        selected = self.species_list.selectedItems()

        if not selected:
            return None

        item = selected[0]

        return item.data(
            Qt.ItemDataRole.UserRole
        )

    def selected_mode(self) -> str:
    
        return self.mode_combo.currentData()


    def _build_species_list(
        self,
        available_species: list[Species],
    ):
        self.species_list = QListWidget()

        self.species_list.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.species_list.setIconSize(QSize(40, 40))
        self.species_list.setSpacing(3)
        self.species_list.setMinimumHeight(180)

        for species in available_species:
            item = QListWidgetItem(species.name)

            item.setData(
                Qt.ItemDataRole.UserRole,
                species,
            )

            item.setSizeHint(QSize(0, 52))

            pixmap = self.assets.get(
                "creature",
                species.name,
                40,
            )

            if pixmap is not None:
                item.setIcon(QIcon(pixmap))

            self.species_list.addItem(item)

        if self.species_list.count() > 0:
            self.species_list.setCurrentRow(0)