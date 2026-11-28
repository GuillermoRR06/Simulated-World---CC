from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QComboBox,
    QGridLayout,

)
from PySide6.QtCore import Qt

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
from .creature_inspector import CreatureInspector

from simulation.model.creature import Creature
from .minimap import MiniMap

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

        main_layout = QGridLayout(
            central_widget
        )

        main_layout.setSpacing(8)

        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 4)
        main_layout.setColumnStretch(2, 1)

        main_layout.setRowStretch(1, 1)

        # --------------------------------
        # Información
        # --------------------------------

        top_layout = QHBoxLayout()
        
        self.state_label = QLabel(
            "Estado: PREPARATION"
        )
        self.state_label.setObjectName(
            "stateLabel"
        )
        
        self.title_label = QLabel(
            "INSTINCT"
        )
        self.title_label.setObjectName(
            "gameTitleLabel"
        )
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        
        self.tick_label = QLabel(
            "Tick: 0"
        )
        self.tick_label.setObjectName(
            "tickLabel"
        )
        self.tick_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )
        
        top_layout.addWidget(
            self.state_label,
            1
        )
        
        top_layout.addWidget(
            self.title_label,
            2
        )
        
        top_layout.addWidget(
            self.tick_label,
            1
        )
        
        main_layout.addLayout(
            top_layout,
            0, 0, 1, 3
        )
        # --------------------------------
        # Panel de preparación
        # --------------------------------

        self.preparation_panel = PreparationPanel(
            self.available_maps,
            self.available_species
        )

        main_layout.addWidget(
            self.preparation_panel,
            1, 0
        )

        # --------------------------------
        # Mapa principal
        # --------------------------------

        self.world_view = WorldView(
            self.controller.simulator.world
        )

        main_layout.addWidget(
            self.world_view,
            1, 1
        )

        # --------------------------------
        # Inspector
        # --------------------------------

        self.creature_inspector = CreatureInspector()

        main_layout.addWidget(
            self.creature_inspector,
            1, 2
        )

        # --------------------------------
        # Minimapa
        # --------------------------------

        self.minimap = MiniMap(
            self.world_view
        )

        minimap_panel = QGroupBox("Minimapa")

        minimap_layout = QVBoxLayout(
            minimap_panel
        )

        minimap_layout.addWidget(
            self.minimap
        )

        main_layout.addWidget(
            minimap_panel,
            3, 0
        )


        # --------------------------------
        # Controles
        # --------------------------------

        controls_layout = QHBoxLayout()


        self.start_button = QPushButton(
            "Start"
        )
        self.start_button.setObjectName("startButton")

        self.pause_button = QPushButton(
            "Pause"
        )

        self.step_button = QPushButton(
            "Step"
        )

        self.reset_button = QPushButton(
            "Reset"
        )
        self.reset_button.setObjectName("resetButton")

        self.center_button = QPushButton(
            "Centrar cámara"
        )

        controls_layout.addWidget(
            self.center_button
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
            controls_layout,
            2, 0, 1, 3
        )
        self.log_panel = LogPanel()
        
        main_layout.addWidget(
            self.log_panel,
            3, 1, 1, 2
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

        self.center_button.clicked.connect(
            self.world_view.reset_view
        )

        self.world_view.view_changed.connect(
            self.minimap.update
        )

    def _update_tick(self, tick: int):
    
        self.tick_label.setText(
            f"Tick: {tick}"
        )
    
        creature = self.selected_creature
    
        if creature is not None:
        
            if creature.x is None or creature.y is None:
            
                self.selected_creature = None
    
                self.world_view.selected_creature = None
    
                self._clear_creature_info()
    
            else:
            
                self._show_creature_info(
                    creature
                )
    
        self.world_view.draw_world()

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
        creature: Creature
    ):
    
        self.selected_creature = creature
    
        self.creature_inspector.show_creature(
            creature
        )

    def _selection_changed(self, creature):
    
        self.selected_creature = creature
    
        if creature is None:
        
            self._clear_creature_info()
    
        else:
        
            self._show_creature_info(creature)
    
    def _clear_creature_info(self):
    
        self.creature_inspector.clear()


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