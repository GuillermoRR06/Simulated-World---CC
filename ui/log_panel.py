from PySide6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QPlainTextEdit,
    QPushButton
)


class LogPanel(QGroupBox):

    def __init__(self):

        super().__init__("Registro de eventos")

        layout = QVBoxLayout(self)

        self.log_output = QPlainTextEdit()

        self.log_output.setReadOnly(True)

        self.log_output.setMaximumBlockCount(1000)

        self.log_output.setMaximumHeight(150)

        self.clear_button = QPushButton(
            "Limpiar registro"
        )

        layout.addWidget(self.log_output)

        layout.addWidget(self.clear_button)

        self.clear_button.clicked.connect(
            self.log_output.clear
        )


    def append_message(self, message: str):

        self.log_output.appendPlainText(message)