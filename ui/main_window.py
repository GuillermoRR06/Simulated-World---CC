from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QComboBox

)

from .simulation_controller import (
    SimulationController,
    SimulationState,
)
from .world_view import WorldView
from .preparation_panel import PreparationPanel

from simulation.model.map_definition import (
    MapDefinition
)

from simulation.model.species import Species

from .log_panel import LogPanel

class MainWindow(QMainWindow):

    def __init__(
        self,
        controller: SimulationController,
        available_maps: list[MapDefinition],
        available_species: list[Species]
    ):
        super().__init__()
    
        self.controller = controller
    
        self.available_maps = list(
            available_maps
        )

        self.available_species = list(
            available_species
        )
    
        self.setWindowTitle(
            "Attack on Instinct"
        )
    
        self.resize(1000, 700)
    
        self.selected_creature = None
    
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )


        # --------------------------------
        # Información
        # --------------------------------

        self.state_label = QLabel(
            "Estado: PREPARATION"
        )

        self.tick_label = QLabel(
            "Tick: 0"
        )

        main_layout.addWidget(
            self.state_label
        )

        main_layout.addWidget(
            self.tick_label
        )


        content_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.preparation_panel = PreparationPanel(
            self.available_maps,
            self.available_species
        )

        left_layout.addWidget(
            self.preparation_panel
        )

        left_layout.addStretch()

        content_layout.addLayout(
            left_layout,
            1
        )

        self.world_view = WorldView(
            self.controller.simulator.world
        )

        content_layout.addWidget(
            self.world_view,
            4
        )

        self.info_panel = QGroupBox(
    "Creature information"
)

        info_layout = QVBoxLayout(
            self.info_panel
        )


        self.species_label = QLabel(
            "Species: -"
        )

        self.faction_label = QLabel(
            "Faction: -"
        )

        self.health_label = QLabel(
            "Health: -"
        )

        self.age_label = QLabel(
            "Age: -"
        )

        self.position_label = QLabel(
            "Position: -"
        )

        self.vision_label = QLabel(
            "Vision: -"
        )

        self.lifespan_label = QLabel(
            "Lifespan: -"
        )

        info_layout.addWidget(
    self.species_label
)

        info_layout.addWidget(
            self.faction_label
        )

        info_layout.addWidget(
            self.health_label
        )

        info_layout.addWidget(
            self.age_label
        )

        info_layout.addWidget(
            self.position_label
        )

        info_layout.addWidget(
            self.vision_label
        )

        info_layout.addWidget(
            self.lifespan_label
        )

        content_layout.addWidget(
    self.info_panel,
    1
)

        main_layout.addLayout(
            content_layout
        )

        # --------------------------------
        # Controles
        # --------------------------------

        controls_layout = QHBoxLayout()


        self.start_button = QPushButton(
            "Start"
        )

        self.pause_button = QPushButton(
            "Pause"
        )

        self.step_button = QPushButton(
            "Step"
        )

        self.reset_button = QPushButton(
            "Reset"
        )


        controls_layout.addWidget(
            self.start_button
        )

        controls_layout.addWidget(
            self.pause_button
        )

        controls_layout.addWidget(
            self.step_button
        )


        main_layout.addLayout(
            controls_layout
        )

        self.log_panel = LogPanel()

        main_layout.addWidget(
            self.log_panel
        )


        controls_layout.addWidget(
            self.reset_button
        )
        self.speed_combo = QComboBox()

        self.speed_combo.addItem(
            "Lenta (2 ticks/s)",
            2
        )

        self.speed_combo.addItem(
            "Normal (10 ticks/s)",
            10
        )

        self.speed_combo.addItem(
            "Rápida (30 ticks/s)",
            30
        )

        controls_layout.addWidget(
            QLabel("Velocidad:")
        )

        controls_layout.addWidget(
            self.speed_combo
        )




    def _connect_signals(self):

        self.world_view.cell_clicked.connect(
            self._cell_clicked
        )


        self.start_button.clicked.connect(
            self.controller.start
        )

        self.pause_button.clicked.connect(
            self.controller.pause
        )

        self.step_button.clicked.connect(
            self.controller.step
        )


        self.controller.tick_changed.connect(
            self._update_tick
        )

        self.controller.state_changed.connect(
            self._update_state
        )

        self.world_view.selection_changed.connect(
            self._selection_changed
        )
        self.preparation_panel.map_requested.connect(
            self.controller.load_map
        )
        self.controller.world_changed.connect(
            self._world_changed
        )
        self.reset_button.clicked.connect(
            self.controller.reset
        )

        self.speed_combo.currentIndexChanged.connect(
            self._change_speed
        )

        self.controller.log_message.connect(
            self.log_panel.append_message
        )

    def _update_tick(
        self,
        tick: int
    ):

        self.tick_label.setText(
            f"Tick: {tick}"
        )

        self.world_view.draw_world()

        if self.selected_creature is not None:

            self._show_creature_info(
                self.selected_creature
            )

    def _update_state(
        self,
        state: SimulationState
    ):

        self.state_label.setText(
            f"Estado: {state.name}"
        )

        self.preparation_panel.setEnabled(
    state == SimulationState.PREPARATION
)

    def _show_creature_info(
    self,
    creature
):
        self.selected_creature = creature

        self.species_label.setText(
            f"Species: {creature.species.name}"
        )

        self.faction_label.setText(
            f"Faction: {creature.species.faction}"
        )

        self.health_label.setText(
            f"Health: {creature.health}"
        )

        self.age_label.setText(
            f"Age: {creature.age}"
        )

        self.position_label.setText(
            f"Position: ({creature.x}, {creature.y})"
        )

        self.vision_label.setText(
            f"Vision: {creature.species.vision}"
        )

        self.lifespan_label.setText(
            f"Lifespan: {creature.species.lifespan}"
        )

    def _selection_changed(self,creature):

        self.selected_creature = creature
        if creature is None:
            self._clear_creature_info()
            return
        self._show_creature_info(
            creature
        )

    def _clear_creature_info(self):

        self.species_label.setText(
            "Species: -"
        )

        self.faction_label.setText(
            "Faction: -"
        )

        self.health_label.setText(
            "Health: -"
        )

        self.age_label.setText(
            "Age: -"
        )

        self.position_label.setText(
            "Position: -"
        )

        self.vision_label.setText(
            "Vision: -"
        )

        self.lifespan_label.setText(
            "Lifespan: -"
        )

    def _world_changed(
    self,
    world
):

        self.selected_creature = None

        self._clear_creature_info()

        self.world_view.set_world(
            world
        )

    def _cell_clicked(self, x: int, y: int):

        if self.controller.state != SimulationState.PREPARATION:
            return

        mode = self.preparation_panel.selected_mode()

        try:

            if mode == "place":

                species = (
                    self.preparation_panel.selected_species()
                )

                if species is None:
                    return

                creature = self.controller.place_creature(
                    species,
                    x,
                    y
                )

                self.statusBar().showMessage(
                    f"{creature.species.name} colocado "
                    f"en ({x}, {y})",
                    3000
                )

            elif mode == "remove":

                creature = self.controller.remove_creature(
                    x,
                    y
                )

                if creature is not None:

                    self.statusBar().showMessage(
                        "Criatura eliminada",
                        3000
                    )

        except (ValueError, IndexError) as error:
        
            self.statusBar().showMessage(
                str(error),
                4000
            )
        
            self.controller.report_event(
                f"ERROR: {error}"
            )

    def _change_speed(
        self,
        index: int
    ):
        speed = self.speed_combo.currentData()

        if speed is not None:

            self.controller.set_speed(
                speed
            )