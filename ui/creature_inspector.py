from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QProgressBar,
)

from simulation.model.creature import Creature

from .asset_manager import AssetManager


class CreatureInspector(QGroupBox):

    def __init__(self):
        super().__init__("Inspector")

        self.assets = AssetManager()

        self._build_ui()

        self.clear()


    def _build_ui(self):

        layout = QVBoxLayout(self)

        # Retrato

        self.portrait = QLabel()

        self.portrait.setObjectName(
            "creaturePortrait"
        )

        self.portrait.setFixedSize(112, 112)

        self.portrait.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.portrait,
            0,
            Qt.AlignmentFlag.AlignHCenter
        )

        # Nombre y faccion

        self.name_label = QLabel()

        self.name_label.setObjectName(
            "creatureName"
        )

        self.name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.name_label.setWordWrap(True)

        self.faction_label = QLabel()

        self.faction_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.faction_label.setWordWrap(True)

        layout.addWidget(self.name_label)
        layout.addWidget(self.faction_label)

        # Vida

        self.health_label = QLabel()

        self.health_bar = QProgressBar()

        self.health_bar.setObjectName(
            "healthBar"
        )

        self.health_bar.setRange(0, 100)
        self.health_bar.setTextVisible(False)

        self.health_reference = QLabel()
        self.health_reference.setWordWrap(True)

        layout.addWidget(self.health_label)
        layout.addWidget(self.health_bar)
        layout.addWidget(self.health_reference)

        # Edad

        self.age_label = QLabel()

        self.age_bar = QProgressBar()

        self.age_bar.setObjectName(
            "ageBar"
        )

        self.age_bar.setRange(0, 100)
        self.age_bar.setTextVisible(False)

        layout.addWidget(self.age_label)
        layout.addWidget(self.age_bar)

        # Informacion adicional

        details = QFormLayout()

        self.position_label = QLabel()
        self.vision_label = QLabel()
        self.lifespan_label = QLabel()

        details.addRow(
            "Posición:",
            self.position_label
        )

        details.addRow(
            "Visión:",
            self.vision_label
        )

        details.addRow(
            "Longevidad:",
            self.lifespan_label
        )

        layout.addLayout(details)

        layout.addStretch()

    def show_creature(self, creature: Creature):

        species = creature.species

        # Retrato

        pixmap = self.assets.get(
            "creature",
            species.name,
            104
        )

        if pixmap is not None:

            self.portrait.setPixmap(pixmap)

        else:

            self.portrait.setText(
                species.name[:1].upper()
            )

        # Nombre y faccion

        self.name_label.setText(
            species.name
        )

        self.faction_label.setText(
            f"Facción: {species.faction}"
        )

        # Vida

        self.health_label.setText(
            f"Vida: {creature.health} PV"
        )

        self.health_reference.setText(
            f"Vida inicial: {species.initial_health}"
        )

        health_percentage = (
            creature.health * 100
            // max(1, species.initial_health)
        )

        self.health_bar.setValue(
            max(0, min(100, health_percentage))
        )

        # Edad

        self.age_label.setText(
            f"Edad: {creature.age} / {species.lifespan}"
        )

        age_percentage = (
            creature.age * 100
            // species.lifespan
        )

        self.age_bar.setValue(
            max(0, min(100, age_percentage))
        )

        # Informacion adicional

        self.position_label.setText(
            f"({creature.x}, {creature.y})"
        )

        self.vision_label.setText(
            str(species.vision)
        )

        self.lifespan_label.setText(
            f"{species.lifespan} ticks"
        )

    def clear(self):

        self.portrait.clear()
        self.portrait.setText("Sin selección")

        self.name_label.setText("Sin criatura")
        self.faction_label.setText("Facción: -")

        self.health_label.setText("Vida: -")
        self.health_reference.setText("Vida inicial: -")
        self.health_bar.setValue(0)

        self.age_label.setText("Edad: -")
        self.age_bar.setValue(0)

        self.position_label.setText("-")
        self.vision_label.setText("-")
        self.lifespan_label.setText("-")