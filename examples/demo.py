"""Demo showcasing Qlementine-styled Qt widgets."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt6Qlementine import (
    ActionButton,
    AutoIconColor,
    ColorButton,
    ColorEditor,
    CommandLinkButton,
    Expander,
    Label,
    LineEdit,
    LoadingSpinner,
    NotificationBadge,
    PlainTextEdit,
    QlementineStyle,
    StatusBadgeWidget,
    Switch,
    TextRole,
)

ZOOM_STEP = 0.1


class Section(QGroupBox):
    """Group box that ignores minimum width so columns can shrink freely."""

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(title, parent)
        sp = self.sizePolicy()
        self.setSizePolicy(sp)
        self._layout = QVBoxLayout(self)

    def vbox(self) -> QVBoxLayout:
        return self._layout


class LabelsSection(Section):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Labels", parent)
        for text, role in [
            ("Headline 1", TextRole.H1),
            ("Headline 2", TextRole.H2),
            ("Headline 3", TextRole.H3),
            ("Headline 4", TextRole.H4),
            ("Headline 5", TextRole.H5),
            ("Default body text", TextRole.Default),
            ("Caption text", TextRole.Caption),
        ]:
            lbl = Label(self)
            lbl.setText(text)
            lbl.setRole(role)
            self.vbox().addWidget(lbl)


class ButtonsSection(Section):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Buttons", parent)

        btn = QPushButton("Default Button", self)
        btn.setDefault(True)
        btn_flat = QPushButton("Flat Button", self)
        btn_flat.setFlat(True)
        btn_menu = QPushButton("With Menu", self)
        menu = QMenu(btn_menu)
        for i in range(3):
            menu.addAction(QAction(f"Action {i + 1}", menu))
        btn_menu.setMenu(menu)

        row1 = QHBoxLayout()
        row1.addWidget(btn)
        row1.addWidget(btn_flat)
        row1.addWidget(btn_menu)
        self.vbox().addLayout(row1)

        action_btn = ActionButton(self)
        action_btn.setText("Action Button")
        cmd_btn = CommandLinkButton(self)
        cmd_btn.setText("Command Link")
        cmd_btn.setDescription("With a description line underneath")

        row2 = QHBoxLayout()
        row2.addWidget(action_btn)
        row2.addWidget(cmd_btn)
        self.vbox().addLayout(row2)


class InputsSection(Section):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Input Widgets", parent)

        line_edit = LineEdit(self)
        line_edit.setPlaceholderText("Type something here...")
        line_edit.setClearButtonEnabled(True)
        self.vbox().addWidget(line_edit)

        plain_text = PlainTextEdit(self)
        plain_text.setPlaceholderText("Multi-line text editor")
        plain_text.setFixedHeight(80)
        self.vbox().addWidget(plain_text)

        spin = QSpinBox(self)
        spin.setRange(0, 100)
        spin.setValue(42)
        spin.setSuffix(" units")
        combo = QComboBox(self)
        combo.setEditable(True)
        for i in range(5):
            combo.addItem(f"Option {i + 1}")

        row = QHBoxLayout()
        row.addWidget(spin)
        row.addWidget(combo)
        self.vbox().addLayout(row)


class TogglesAndChecks(Section):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Toggles & Checks", parent)

        sw = Switch(self)
        sw.setText("Switch toggle")
        sw.setChecked(True)
        sw_tri = Switch(self)
        sw_tri.setText("Tristate switch")
        sw_tri.setTristate(True)
        sw_tri.setCheckState(Qt.CheckState.PartiallyChecked)

        row = QHBoxLayout()
        row.addWidget(sw)
        row.addWidget(sw_tri)
        self.vbox().addLayout(row)

        checks = QHBoxLayout()
        for i, text in enumerate(["Check A", "Check B", "Check C"]):
            cb = QCheckBox(text, self)
            cb.setChecked(i % 2 == 0)
            checks.addWidget(cb)
        self.vbox().addLayout(checks)

        radios = QHBoxLayout()
        for i, text in enumerate(["Radio 1", "Radio 2", "Radio 3"]):
            rb = QRadioButton(text, self)
            rb.setChecked(i == 0)
            radios.addWidget(rb)
        self.vbox().addLayout(radios)


class SlidersAndProgress(Section):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Sliders & Progress", parent)

        progress = QProgressBar(self)
        progress.setRange(0, 100)
        progress.setValue(35)
        self.vbox().addWidget(progress)

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setRange(0, 100)
        slider.setValue(35)
        slider.valueChanged.connect(progress.setValue)
        self.vbox().addWidget(slider)

        dial = QDial(self)
        dial.setRange(0, 100)
        dial.setValue(50)
        dial.setNotchesVisible(True)
        dial.setFixedSize(64, 64)
        spinner = LoadingSpinner(self)
        spinner.setFixedSize(48, 48)

        row = QHBoxLayout()
        row.addWidget(dial)
        row.addWidget(spinner)
        row.addStretch()
        self.vbox().addLayout(row)


class QlementineWidgets(Section):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Qlementine Widgets", parent)

        expand_btn = QPushButton("Toggle Expander", self)
        self.vbox().addWidget(expand_btn)

        expander = Expander(self)
        inner = QWidget(self)
        inner_lay = QVBoxLayout(inner)
        inner_lay.setContentsMargins(0, 0, 0, 0)
        inner_lay.addWidget(Label("Hidden content revealed!", parent=inner))
        inner_line = LineEdit(inner)
        inner_line.setPlaceholderText("An input inside the expander")
        inner_lay.addWidget(inner_line)
        expander.setContent(inner)
        expand_btn.clicked.connect(expander.toggleExpanded)
        self.vbox().addWidget(expander)

        color_row = QHBoxLayout()
        color_row.addWidget(Label("Color:", parent=self))
        color_row.addWidget(ColorButton(self))
        color_row.addWidget(ColorEditor(self))
        color_row.addStretch()
        self.vbox().addLayout(color_row)

        badge_row = QHBoxLayout()
        badge_row.addWidget(Label("Status badge:", parent=self))
        badge_row.addWidget(StatusBadgeWidget(self))
        badge_row.addWidget(Label("Notification:", parent=self))
        notif = NotificationBadge(self)
        notif.setText("3")
        badge_row.addWidget(notif)
        badge_row.addStretch()
        self.vbox().addLayout(badge_row)


class SettingsForm(QScrollArea):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)

        form = QWidget()
        self.setWidget(form)
        layout = QVBoxLayout(form)

        title = Label(form)
        title.setText("Settings")
        title.setRole(TextRole.H2)
        layout.addWidget(title)

        general = Section("General", form)
        name_edit = LineEdit(general)
        name_edit.setPlaceholderText("Project name")
        general.vbox().addWidget(name_edit)
        desc_edit = PlainTextEdit(general)
        desc_edit.setPlaceholderText("Description")
        desc_edit.setFixedHeight(60)
        general.vbox().addWidget(desc_edit)
        layout.addWidget(general)

        appearance = Section("Appearance", form)
        dark_switch = Switch(appearance)
        dark_switch.setText("Dark mode")
        appearance.vbox().addWidget(dark_switch)
        anim_switch = Switch(appearance)
        anim_switch.setText("Enable animations")
        anim_switch.setChecked(True)
        appearance.vbox().addWidget(anim_switch)
        layout.addWidget(appearance)

        layout.addStretch()

        buttons = QHBoxLayout()
        buttons.addStretch()
        save_btn = QPushButton("Save", form)
        save_btn.setDefault(True)
        buttons.addWidget(save_btn)
        cancel_btn = QPushButton("Cancel", form)
        cancel_btn.setFlat(True)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)


class DemoWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyQt6-Qlementine Demo")

        tabs = QTabWidget(self)
        self.setCentralWidget(tabs)

        # --- Gallery tab (2-column) ---
        gallery = QWidget()
        columns = QHBoxLayout(gallery)
        left = QVBoxLayout()
        right = QVBoxLayout()
        columns.addLayout(left, 1)
        columns.addLayout(right, 1)

        left.addWidget(LabelsSection(gallery))
        left.addWidget(ButtonsSection(gallery))
        left.addWidget(InputsSection(gallery))
        right.addWidget(TogglesAndChecks(gallery))
        right.addWidget(SlidersAndProgress(gallery))
        right.addWidget(QlementineWidgets(gallery))
        left.addStretch()
        right.addStretch()

        tabs.addTab(gallery, "Widget Gallery")
        tabs.addTab(SettingsForm(self), "Form Example")

        self.resize(1000, 700)


def _setup_zoom_shortcuts(window: QMainWindow, style: QlementineStyle) -> None:
    """Wire up Ctrl+Shift+=/+/- zoom shortcuts."""

    def zoom_in() -> None:
        style.setScaleFactor(style.scaleFactor() + ZOOM_STEP)

    def zoom_out() -> None:
        style.setScaleFactor(style.scaleFactor() - ZOOM_STEP)

    def reset_zoom() -> None:
        style.setScaleFactor(1.0)

    mods = Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier
    QShortcut(QKeySequence(mods | Qt.Key.Key_Equal), window, zoom_in)  # type: ignore
    QShortcut(QKeySequence(mods | Qt.Key.Key_Plus), window, zoom_in)  # type: ignore
    QShortcut(QKeySequence(mods | Qt.Key.Key_Minus), window, zoom_out)  # type: ignore
    QShortcut(QKeySequence(mods | Qt.Key.Key_0), window, reset_zoom)  # type: ignore


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Qlementine Demo")

    window = DemoWindow()
    if "--unstyled" not in sys.argv:
        style = QlementineStyle(app)
        style.setAutoIconColor(AutoIconColor.TextColor)
        style.setAnimationsEnabled(True)
        app.setStyle(style)
        _setup_zoom_shortcuts(window, style)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
