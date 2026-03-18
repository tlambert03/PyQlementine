"""Comprehensive demo of standard Qt widgets styled with Qlementine."""

from __future__ import annotations

import sys
from datetime import date, time

from PyQt6.QtCore import QDate, Qt, QTime
from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDialogButtonBox,
    QCommandLinkButton,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFileDialog,
    QFontComboBox,
    QFontDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QKeySequenceEdit,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QProgressDialog,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QTimeEdit,
    QToolBar,
    QToolBox,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt6Qlementine import AutoIconColor, QlementineStyle

# ---------------------------------------------------------------------------
# Tab 1: Widget Gallery (2-column)
# ---------------------------------------------------------------------------


class LabelsSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Labels && Display", parent)
        layout = QVBoxLayout(self)

        for text, size, bold in [
            ("Headline 1", 28, True),
            ("Headline 2", 22, True),
            ("Headline 3", 18, True),
            ("Headline 4", 14, True),
            ("Headline 5", 12, True),
            ("Default body text", 0, False),
            ("Caption text", -2, False),
        ]:
            lbl = QLabel(text, self)
            if size or bold:
                font = lbl.font()
                if size > 0:
                    font.setPointSize(size)
                elif size < 0:
                    font.setPointSize(font.pointSize() + size)
                font.setBold(bold)
                lbl.setFont(font)
            layout.addWidget(lbl)

        lcd = QLCDNumber(self)
        lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        lcd.display(42.5)
        lcd.setFixedHeight(40)
        layout.addWidget(lcd)


class ButtonsSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Buttons", parent)
        layout = QVBoxLayout(self)

        btn = QPushButton("Default", self)
        btn.setDefault(True)
        btn_flat = QPushButton("Flat", self)
        btn_flat.setFlat(True)
        btn_disabled = QPushButton("Disabled", self)
        btn_disabled.setEnabled(False)
        btn_menu = QPushButton("With Menu", self)
        menu = QMenu(btn_menu)
        for i in range(3):
            menu.addAction(QAction(f"Action {i + 1}", menu))
        btn_menu.setMenu(menu)

        row1 = QHBoxLayout()
        row1.addWidget(btn)
        row1.addWidget(btn_flat)
        row1.addWidget(btn_disabled)
        row1.addWidget(btn_menu)
        layout.addLayout(row1)

        tool_btn = QToolButton(self)
        tool_btn.setText("Tool")
        tool_btn.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        tool_menu = QMenu(tool_btn)
        tool_menu.addAction("Option A")
        tool_menu.addAction("Option B")
        tool_btn.setMenu(tool_menu)

        cmd_btn = QCommandLinkButton("Command Link", self)
        cmd_btn.setDescription("With a description line underneath")

        row2 = QHBoxLayout()
        row2.addWidget(tool_btn)
        row2.addWidget(cmd_btn)
        layout.addLayout(row2)


class TextInputsSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Text Inputs", parent)
        layout = QVBoxLayout(self)

        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText("QLineEdit — single line...")
        line_edit.setClearButtonEnabled(True)
        layout.addWidget(line_edit)

        line_pw = QLineEdit(self)
        line_pw.setPlaceholderText("Password field")
        line_pw.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(line_pw)

        plain_text = QPlainTextEdit(self)
        plain_text.setPlaceholderText("QPlainTextEdit — multi-line plain text")
        plain_text.setFixedHeight(60)
        layout.addWidget(plain_text)

        rich_text = QTextEdit(self)
        rich_text.setPlaceholderText("QTextEdit — rich text")
        rich_text.setFixedHeight(60)
        layout.addWidget(rich_text)


class SpinnersAndCombos(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Spinners && Combos", parent)
        layout = QVBoxLayout(self)

        form = QFormLayout()

        spin = QSpinBox(self)
        spin.setRange(0, 100)
        spin.setValue(42)
        spin.setSuffix(" units")
        form.addRow("QSpinBox:", spin)

        dspin = QDoubleSpinBox(self)
        dspin.setRange(0.0, 1.0)
        dspin.setSingleStep(0.05)
        dspin.setValue(0.75)
        dspin.setDecimals(2)
        form.addRow("QDoubleSpinBox:", dspin)

        combo = QComboBox(self)
        combo.setEditable(True)
        for i in range(5):
            combo.addItem(f"Option {i + 1}")
        form.addRow("QComboBox:", combo)

        font_combo = QFontComboBox(self)
        form.addRow("QFontComboBox:", font_combo)

        layout.addLayout(form)


class TogglesAndChecks(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Toggles && Checks", parent)
        layout = QVBoxLayout(self)

        checks = QHBoxLayout()
        for i, text in enumerate(["Check A", "Check B", "Check C"]):
            cb = QCheckBox(text, self)
            cb.setChecked(i % 2 == 0)
            checks.addWidget(cb)
        tri = QCheckBox("Tristate", self)
        tri.setTristate(True)
        tri.setCheckState(Qt.CheckState.PartiallyChecked)
        checks.addWidget(tri)
        layout.addLayout(checks)

        radios = QHBoxLayout()
        for i, text in enumerate(["Radio 1", "Radio 2", "Radio 3"]):
            rb = QRadioButton(text, self)
            rb.setChecked(i == 0)
            radios.addWidget(rb)
        layout.addLayout(radios)


class SlidersAndProgress(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Sliders && Progress", parent)
        layout = QVBoxLayout(self)

        progress = QProgressBar(self)
        progress.setRange(0, 100)
        progress.setValue(35)
        layout.addWidget(progress)

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setRange(0, 100)
        slider.setValue(35)
        slider.valueChanged.connect(progress.setValue)
        layout.addWidget(slider)

        dial = QDial(self)
        dial.setRange(0, 100)
        dial.setValue(50)
        dial.setNotchesVisible(True)
        dial.setFixedSize(64, 64)

        row = QHBoxLayout()
        row.addWidget(dial)
        row.addStretch()
        layout.addLayout(row)


class DateTimeSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Date && Time", parent)
        layout = QVBoxLayout(self)

        form = QFormLayout()

        date_edit = QDateEdit(self)
        date_edit.setCalendarPopup(True)
        date_edit.setDate(
            QDate(date.today().year, date.today().month, date.today().day)
        )
        form.addRow("QDateEdit:", date_edit)

        time_edit = QTimeEdit(self)
        now = time(12, 30)
        time_edit.setTime(QTime(now.hour, now.minute))
        form.addRow("QTimeEdit:", time_edit)

        dt_edit = QDateTimeEdit(self)
        dt_edit.setCalendarPopup(True)
        form.addRow("QDateTimeEdit:", dt_edit)

        ks_edit = QKeySequenceEdit(self)
        form.addRow("QKeySequenceEdit:", ks_edit)

        layout.addLayout(form)


class WidgetGalleryTab(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        columns = QHBoxLayout(self)
        left = QVBoxLayout()
        right = QVBoxLayout()
        columns.addLayout(left, 1)
        columns.addLayout(right, 1)

        left.addWidget(LabelsSection(self))
        left.addWidget(ButtonsSection(self))
        left.addWidget(TextInputsSection(self))
        right.addWidget(TogglesAndChecks(self))
        right.addWidget(SpinnersAndCombos(self))
        right.addWidget(SlidersAndProgress(self))
        right.addWidget(DateTimeSection(self))
        left.addStretch()
        right.addStretch()


# ---------------------------------------------------------------------------
# Tab 2: Item Views
# ---------------------------------------------------------------------------


class ListWidgetSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("QListWidget", parent)
        layout = QVBoxLayout(self)

        lw = QListWidget(self)
        for i in range(8):
            lw.addItem(f"List item {i + 1}")
        lw.setFixedHeight(150)
        layout.addWidget(lw)


class TableWidgetSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("QTableWidget", parent)
        layout = QVBoxLayout(self)

        tw = QTableWidget(5, 3, self)
        tw.setHorizontalHeaderLabels(["Name", "Value", "Unit"])
        for r in range(5):
            tw.setItem(r, 0, QTableWidgetItem(f"Param {r + 1}"))
            tw.setItem(r, 1, QTableWidgetItem(str(r * 10 + 5)))
            tw.setItem(r, 2, QTableWidgetItem(["m", "kg", "s", "A", "K"][r]))
        tw.setFixedHeight(180)
        layout.addWidget(tw)


class TreeWidgetSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("QTreeWidget", parent)
        layout = QVBoxLayout(self)

        tree = QTreeWidget(self)
        tree.setHeaderLabels(["Name", "Type"])
        for group_name, children in [
            ("Animals", [("Cat", "Mammal"), ("Parrot", "Bird"), ("Frog", "Amphibian")]),
            (
                "Plants",
                [("Oak", "Tree"), ("Daisy", "Flower"), ("Fern", "Pteridophyte")],
            ),
        ]:
            group = QTreeWidgetItem([group_name])
            for name, kind in children:
                group.addChild(QTreeWidgetItem([name, kind]))
            tree.addTopLevelItem(group)
        tree.expandAll()
        tree.setFixedHeight(180)
        layout.addWidget(tree)


class ItemViewsTab(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        columns = QHBoxLayout(self)
        left = QVBoxLayout()
        right = QVBoxLayout()
        columns.addLayout(left, 1)
        columns.addLayout(right, 1)

        left.addWidget(ListWidgetSection(self))
        left.addWidget(TableWidgetSection(self))
        right.addWidget(TreeWidgetSection(self))
        left.addStretch()
        right.addStretch()


# ---------------------------------------------------------------------------
# Tab 3: Containers && Display
# ---------------------------------------------------------------------------


class SplitterSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("QSplitter", parent)
        layout = QVBoxLayout(self)

        splitter = QSplitter(Qt.Orientation.Horizontal, self)
        for name, shape in [
            ("NoFrame", QLabel.Shape.NoFrame),
            ("Box", QLabel.Shape.Box),
            ("Panel", QLabel.Shape.Panel),
            ("StyledPanel", QLabel.Shape.StyledPanel),
        ]:
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFrameShape(shape)
            splitter.addWidget(lbl)
        splitter.setFixedHeight(80)
        layout.addWidget(splitter)


class ToolBoxSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("QToolBox", parent)
        layout = QVBoxLayout(self)

        toolbox = QToolBox(self)
        for title, items in [
            ("Section A", ["Item 1", "Item 2"]),
            ("Section B", ["Item 3", "Item 4"]),
            ("Section C", ["Item 5", "Item 6"]),
        ]:
            page = QWidget()
            page_layout = QVBoxLayout(page)
            for item in items:
                page_layout.addWidget(QLabel(item, page))
            toolbox.addItem(page, title)
        toolbox.setFixedHeight(160)
        layout.addWidget(toolbox)


class StackedSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("QStackedWidget", parent)
        layout = QVBoxLayout(self)

        stack = QStackedWidget(self)
        for i in range(3):
            page = QLabel(f"Page {i + 1}", stack)
            page.setAlignment(Qt.AlignmentFlag.AlignCenter)
            page.setFrameShape(QLabel.Shape.StyledPanel)
            stack.addWidget(page)

        row = QHBoxLayout()
        for i in range(3):
            btn = QPushButton(f"Page {i + 1}", self)
            btn.clicked.connect(lambda checked, idx=i: stack.setCurrentIndex(idx))
            row.addWidget(btn)

        layout.addLayout(row)
        layout.addWidget(stack)


class CalendarSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("QCalendarWidget", parent)
        layout = QVBoxLayout(self)

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        layout.addWidget(cal)


class DialogsSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Dialogs", parent)
        layout = QVBoxLayout(self)

        self._result = QLabel("(dialog result appears here)", self)
        self._result.setFrameShape(QLabel.Shape.StyledPanel)
        self._result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._result.setWordWrap(True)

        for text, slot in [
            ("QColorDialog", self._color),
            ("QFontDialog", self._font),
            ("QFileDialog", self._file),
            ("QInputDialog", self._input),
            ("QMessageBox", self._message),
            ("QProgressDialog", self._progress),
        ]:
            btn = QPushButton(text, self)
            btn.clicked.connect(slot)
            layout.addWidget(btn)

        layout.addWidget(self._result)

    def _color(self) -> None:
        color = QColorDialog.getColor(parent=self)
        if color.isValid():
            self._result.setText(color.name())
            self._result.setStyleSheet(
                f"background-color: {color.name()}; padding: 4px;"
            )

    def _font(self) -> None:
        ok, font = QFontDialog.getFont(self.font(), self)
        if ok:
            self._result.setText(f"{font.family()}, {font.pointSize()}pt")
            self._result.setStyleSheet("")

    def _file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            self._result.setText(path)
            self._result.setStyleSheet("")

    def _input(self) -> None:
        text, ok = QInputDialog.getText(self, "Input", "Enter your name:")
        if ok and text:
            self._result.setText(f"Hello, {text}!")
            self._result.setStyleSheet("")

    def _message(self) -> None:
        result = QMessageBox.question(
            self,
            "Question",
            "Do you like this demo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        name = "Yes" if result == QMessageBox.StandardButton.Yes else "No"
        self._result.setText(f"You clicked: {name}")
        self._result.setStyleSheet("")

    def _progress(self) -> None:
        dlg = QProgressDialog("Working...", "Cancel", 0, 100, self)
        dlg.setWindowModality(Qt.WindowModality.WindowModal)
        dlg.setValue(100)


class DialogButtonBoxSection(QGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("QDialogButtonBox", parent)
        layout = QVBoxLayout(self)

        box1 = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply,
            self,
        )
        layout.addWidget(box1)

        box2 = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Discard
            | QDialogButtonBox.StandardButton.Reset
            | QDialogButtonBox.StandardButton.Help,
            self,
        )
        layout.addWidget(box2)

        box3 = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Yes
            | QDialogButtonBox.StandardButton.No
            | QDialogButtonBox.StandardButton.Abort
            | QDialogButtonBox.StandardButton.Retry,
            self,
        )
        layout.addWidget(box3)


class ContainersTab(QScrollArea):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)

        inner = QWidget()
        columns = QHBoxLayout(inner)
        left = QVBoxLayout()
        right = QVBoxLayout()
        columns.addLayout(left, 1)
        columns.addLayout(right, 1)

        left.addWidget(SplitterSection(inner))
        left.addWidget(ToolBoxSection(inner))
        left.addWidget(DialogButtonBoxSection(inner))
        right.addWidget(StackedSection(inner))
        right.addWidget(CalendarSection(inner))
        right.addWidget(DialogsSection(inner))
        left.addStretch()
        right.addStretch()

        self.setWidget(inner)


# ---------------------------------------------------------------------------
# Tab 4: Form Example
# ---------------------------------------------------------------------------


class SettingsForm(QScrollArea):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)

        form = QWidget()
        self.setWidget(form)
        layout = QVBoxLayout(form)

        title = QLabel("Settings", form)
        font = title.font()
        font.setPointSize(22)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)

        general = QGroupBox("General", form)
        general_layout = QVBoxLayout(general)
        name_edit = QLineEdit(general)
        name_edit.setPlaceholderText("Project name")
        general_layout.addWidget(name_edit)
        desc_edit = QPlainTextEdit(general)
        desc_edit.setPlaceholderText("Description")
        desc_edit.setFixedHeight(60)
        general_layout.addWidget(desc_edit)
        layout.addWidget(general)

        appearance = QGroupBox("Appearance", form)
        appearance_layout = QVBoxLayout(appearance)
        dark_cb = QCheckBox("Dark mode", appearance)
        appearance_layout.addWidget(dark_cb)
        anim_cb = QCheckBox("Enable animations", appearance)
        anim_cb.setChecked(True)
        appearance_layout.addWidget(anim_cb)
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


# ---------------------------------------------------------------------------
# Main Window
# ---------------------------------------------------------------------------


class DemoWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Qt Widget Gallery")

        # Menu bar
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&New")
        file_menu.addAction("&Open...")
        file_menu.addAction("&Save")
        file_menu.addSeparator()
        quit_action = file_menu.addAction("E&xit")
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(QApplication.quit)

        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction("&Undo")
        edit_menu.addAction("&Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cu&t")
        edit_menu.addAction("&Copy")
        edit_menu.addAction("&Paste")

        view_menu = menubar.addMenu("&View")
        view_menu.addAction("Zoom &In")
        view_menu.addAction("Zoom &Out")
        view_menu.addSeparator()
        toggle = view_menu.addAction("&Toolbar")
        toggle.setCheckable(True)
        toggle.setChecked(True)

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&About")
        help_menu.addAction("About &Qt")

        # Toolbar
        toolbar = QToolBar("Main", self)
        toolbar.addAction("New")
        toolbar.addAction("Open")
        toolbar.addSeparator()
        toolbar.addAction("Save")
        self.addToolBar(toolbar)
        toggle.toggled.connect(toolbar.setVisible)

        # Status bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")  # type: ignore[union-attr]

        # Tabs
        tabs = QTabWidget(self)
        self.setCentralWidget(tabs)
        tabs.addTab(WidgetGalleryTab(self), "Widget Gallery")
        tabs.addTab(ItemViewsTab(self), "Item Views")
        tabs.addTab(ContainersTab(self), "Containers && Display")
        tabs.addTab(SettingsForm(self), "Form Example")

        self.resize(1000, 750)


def _setup_zoom_shortcuts(
    window: QMainWindow, style: QlementineStyle, zoom_step: float = 0.1
) -> None:
    """Wire up Ctrl+Shift+=/+/- zoom shortcuts."""
    if not hasattr(style, "setScaleFactor"):  # future feature
        return

    def zoom_in() -> None:
        style.setScaleFactor(style.scaleFactor() + zoom_step)

    def zoom_out() -> None:
        style.setScaleFactor(style.scaleFactor() - zoom_step)

    def reset_zoom() -> None:
        style.setScaleFactor(1.0)

    mods = Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier
    QShortcut(QKeySequence(mods | Qt.Key.Key_Equal), window, zoom_in)  # type: ignore
    QShortcut(QKeySequence(mods | Qt.Key.Key_Plus), window, zoom_in)  # type: ignore
    QShortcut(QKeySequence(mods | Qt.Key.Key_Minus), window, zoom_out)  # type: ignore
    QShortcut(QKeySequence(mods | Qt.Key.Key_0), window, reset_zoom)  # type: ignore


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Qt Widget Gallery")
    parser.add_argument(
        "--style",
        choices=["native", "fusion", "qlementine"],
        default="native",
        help="widget style to use (default: qlementine)",
    )
    args, qt_args = parser.parse_known_args()

    app = QApplication([sys.argv[0], *qt_args])
    app.setApplicationDisplayName("Qt Widget Gallery")
    window = DemoWindow()

    if args.style == "fusion":
        app.setStyle("Fusion")
    elif args.style == "qlementine":
        qlem = QlementineStyle(app)
        qlem.setAutoIconColor(AutoIconColor.TextColor)
        qlem.setAnimationsEnabled(True)
        app.setStyle(qlem)
        _setup_zoom_shortcuts(window, qlem)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
