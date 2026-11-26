from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSpinBox,
)

from simulation.model.map_definition import MapDefinition
from simulation.model.species import Species


class PreparationPanel(QGroupBox):

    map_requested = Signal(object, int)


    def __init__(
        self,
        available_maps: list[MapDefinition],
        available_species: list[Species]
    ):
        super().__init__("Preparación")

        self._build_ui(
            available_maps,
            available_species
        )


    def _build_ui(
        self,
        available_maps: list[MapDefinition],
        available_species: list[Species]
    ):
        layout = QFormLayout(self)

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

        self.load_button = QPushButton(
            "Cargar mapa"
        )

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

        layout.addRow(self.load_button)

        self.species_combo = QComboBox()

        for species in available_species:
        
            self.species_combo.addItem(
                species.name,
                species
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
            "Especie:",
            self.species_combo
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

        self.load_button.clicked.connect(
            self._request_map
        )

        self._update_dimensions()

    def _update_dimensions(
        self,
        index: int = -1
    ):
        map_definition = (
            self.map_combo.currentData()
        )

        if map_definition is None:
            self.dimensions_label.setText(
                "Sin mapas disponibles"
            )

            self.load_button.setEnabled(False)
            return

        self.dimensions_label.setText(
            f"{map_definition.width} x "
            f"{map_definition.height}"
        )

        self.load_button.setEnabled(True)

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

    def selected_species(self):
    
        return self.species_combo.currentData()

    def selected_mode(self) -> str:
    
        return self.mode_combo.currentData()