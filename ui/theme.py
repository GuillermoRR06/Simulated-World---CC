from pathlib import Path

from PySide6.QtGui import QColor, QPalette,QFontDatabase, QFont
from PySide6.QtWidgets import QApplication




def apply_theme(app: QApplication) -> None:
    """Aplica el tema de la interfaz después de crear QApplication."""


    fonts_dir = (
        Path(__file__).resolve().parent
        / "assets"
        / "fonts"
    )
    
    title_font_path = fonts_dir / "Cinzel-Bold.ttf"
    
    if title_font_path.exists():
        QFontDatabase.addApplicationFont(
            str(title_font_path)
        )
    
    app.setFont(
        QFont("Segoe UI", 10)
    )

    app.setStyle("Fusion")

    palette = QPalette()
    role = QPalette.ColorRole

    colors = {
        role.Window: "#101820",
        role.WindowText: "#EEE8D5",
        role.Base: "#101D27",
        role.AlternateBase: "#1C2B36",
        role.Text: "#EEE8D5",
        role.Button: "#283E4C",
        role.ButtonText: "#EEE8D5",
        role.Highlight: "#355D4A",
        role.HighlightedText: "#FFFFFF",
        role.ToolTipBase: "#263A47",
        role.ToolTipText: "#EEE8D5",
        role.Light: "#506572",
        role.Midlight: "#3B515F",
        role.Mid: "#243744",
        role.Dark: "#0C141B",
        role.Shadow: "#080E13",
    }

    for color_role, color in colors.items():
        palette.setColor(color_role, QColor(color))

    disabled = QPalette.ColorGroup.Disabled

    for color_role in (role.WindowText, role.Text, role.ButtonText):
        palette.setColor(disabled, color_role, QColor("#83939F"))

    palette.setColor(disabled, role.Highlight, QColor("#293B46"))
    palette.setColor(disabled, role.HighlightedText, QColor("#A9B8C0"))

    app.setPalette(palette)

    theme_path = (
        Path(__file__).resolve().parent / "styles" / "dark.qss"
    )

    app.setStyleSheet(theme_path.read_text(encoding="utf-8"))
