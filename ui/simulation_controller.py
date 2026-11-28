from enum import Enum, auto

from PySide6.QtCore import QObject, QTimer, Signal

from simulation.simulator import Simulator
from simulation.loaders.map_factory import MapFactory

from simulation.model.map_definition import (
    MapDefinition
)

from simulation.model.creature import Creature
from simulation.model.species import Species

class SimulationState(Enum):
    PREPARATION = auto()
    RUNNING = auto()
    PAUSED = auto()


class SimulationController(QObject):

    state_changed = Signal(object)
    tick_changed = Signal(int)
    world_changed = Signal(object)
    log_message = Signal(str)

    def __init__(
        self,
        simulator: Simulator,
        map_factory: MapFactory,
        initial_map: MapDefinition,
        seed: int = 42
    ):
        super().__init__()

        self.simulator = simulator
        self.map_factory = map_factory
        self._active_map = initial_map
        self._active_seed = seed

        self.state = SimulationState.PREPARATION

        self.timer = QTimer()
        self.timer.setInterval(500)

        self.timer.timeout.connect(
            self._advance_tick
        )

    def start(self):

        if self.state == SimulationState.RUNNING:
            return

        self.state = SimulationState.RUNNING

        self.timer.start()

        self.report_event(
            "Simulación iniciada"
        )

        self.state_changed.emit(
            self.state
        )


    def pause(self):

        if self.state != SimulationState.RUNNING:
            return

        self.timer.stop()

        self.state = SimulationState.PAUSED

        self.report_event(
            "Simulación pausada"
        )

        self.state_changed.emit(
            self.state
        )

    def step(self):

        if self.state == SimulationState.RUNNING:
            return

        if self.state == SimulationState.PREPARATION:
            self.state = SimulationState.PAUSED

            self.state_changed.emit(
                self.state
            )

        self._advance_tick()

    def _advance_tick(self):

        self.simulator.advance_tick()

        self.tick_changed.emit(
            self.simulator.current_tick
        )

    def load_map(
        self,
        map_definition: MapDefinition,
        seed: int
    ):
        if self.state != SimulationState.PREPARATION:
            return

        self._rebuild_world(
            map_definition,
            seed
        )

        self.report_event(
            f"Mapa cargado: {map_definition.name}"
        )


    def place_creature(
        self,
        species: Species,
        x: int,
        y: int
    ) -> Creature:

        if self.state != SimulationState.PREPARATION:

            raise ValueError(
                "Cannot place creatures during simulation"
            )

        creature = Creature(species)

        self.simulator.world.place_creature(
            creature,
            x,
            y
        )

        self.report_event(
            f"{species.name} colocado en ({x}, {y})"
        )

        return creature


    def remove_creature(
        self,
        x: int,
        y: int
    ) -> Creature | None:
    
        if self.state != SimulationState.PREPARATION:
        
            raise ValueError(
                "Cannot remove creatures during simulation"
            )
    
        creature = self.simulator.world.remove_creature(
            x,
            y
        )
    
        if creature is not None:
        
            self.report_event(
                f"{creature.species.name} eliminado "
                f"de ({x}, {y})"
            )
    
        return creature


    def _rebuild_world(
        self,
        map_definition: MapDefinition,
        seed: int
    ):
        world = self.map_factory.create_world(
            map_definition
        )

        simulator = Simulator(
            world,
            seed=seed
        )

        self.timer.stop()

        self.simulator = simulator

        self._active_map = map_definition
        self._active_seed = seed

        self.state = SimulationState.PREPARATION

        self.world_changed.emit(world)

        self.tick_changed.emit(
            self.simulator.current_tick
        )

        self.state_changed.emit(
            self.state
        )

    def reset(self):

        self._rebuild_world(
            self._active_map,
            self._active_seed
        )

        self.report_event(
            "Simulación reiniciada"
        )

    def set_speed(
        self,
        ticks_per_second: int
    ):
        if ticks_per_second <= 0:
            raise ValueError(
                "Speed must be positive"
            )

        interval = max(
            1,
            round(1000 / ticks_per_second)
        )

        self.timer.setInterval(
            interval
        )
        self.report_event(
            f"Velocidad: {ticks_per_second} ticks/s"
        )

    def report_event(self, message: str):

        tick = self.simulator.current_tick

        self.log_message.emit(
            f"[Tick {tick:04d}] {message}"
        )