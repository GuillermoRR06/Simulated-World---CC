import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)

from simulation.loaders.application_loader import (
    ApplicationLoader,
)
from simulation.loaders.map_factory import (
    MapFactory,
)
from simulation.simulator import Simulator

from .main_window import MainWindow
from .simulation_controller import (
    SimulationController,
)

from simulation.model.species import Species


def main() -> int:
    app = QApplication(sys.argv)

    root_path = (
        Path(__file__).resolve().parents[1]
    )

    loader = ApplicationLoader(
        str(root_path)
    )

    loader.load()

    if not loader.maps:
        details = "\n".join(loader.errors)

        QMessageBox.critical(
            None,
            "No hay mapas disponibles",
            "Revisa los archivos de terrains, "
            "objects y maps.\n\n" + details,
        )

        return 1

    map_factory = MapFactory(
        loader.catalog
    )

    try:
        world = map_factory.create_world(
            loader.maps[0]
        )

    except ValueError as error:
        details = "\n".join(
            loader.errors + [str(error)]
        )

        QMessageBox.critical(
            None,
            "No se pudo crear el mundo",
            details,
        )

        return 1

    simulator = Simulator(
        world,
        seed=42
    )

    controller = SimulationController(
        simulator,
        map_factory,
        loader.maps[0],
        seed=42
    )

    available_species = [
        Species("Eldian", "eldia", 100, 4, 200),
        Species("Marleyan", "marley", 100, 4, 200),
        Species("PureTitan", "titans", 200, 5, 300)
    ]


    window = MainWindow(
        controller,
        loader.maps,
        available_species
    )

    controller.report_event(
        f"Mapas disponibles: {len(loader.maps)}"
    )
    
    controller.report_event(
        f"Mapa inicial: {loader.maps[0].name}"
    )
    
    for error in loader.errors:
    
        controller.report_event(
            f"ERROR DE CARGA: {error}"
        )


    window.show()

    if loader.errors:
        QMessageBox.warning(
            window,
            "Algunos archivos no se pudieron cargar",
            "\n".join(loader.errors),
        )

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())