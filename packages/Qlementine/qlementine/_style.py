"""QlementineStyle - pure-Python QCommonStyle subclass."""

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from qlementine._qt import QtCore, QtGui, QtWidgets, Signal
from qlementine._enums import AutoIconColor, Status
from qlementine._style_colors import QlementineStyleColorsMixin
from qlementine._style_drawing import QlementineStyleDrawingMixin
from qlementine._style_metrics import QlementineStyleMetricsMixin

if TYPE_CHECKING:
    from qlementine._theme import Theme

QApplication = QtWidgets.QApplication
QCommonStyle = QtWidgets.QCommonStyle
QColor = QtGui.QColor
QIcon = QtGui.QIcon
QPalette = QtGui.QPalette
QPixmap = QtGui.QPixmap
QSize = QtCore.QSize

__all__ = ["QlementineStyle", "appStyle"]

_AUTO_ICON_COLOR_PROP = b"_qlementine_autoIconColor"


class QlementineStyle(
    QlementineStyleDrawingMixin,
    QlementineStyleMetricsMixin,
    QlementineStyleColorsMixin,
    QCommonStyle,
):
    """Pure-Python port of oclero::qlementine::QlementineStyle."""

    # -- Signals -------------------------------------------------------

    themeChanged = Signal()
    animationsEnabledChanged = Signal()

    # -- Extended enums (nested) ---------------------------------------

    class StandardPixmapExt(IntEnum):
        SP_Check = 0
        SP_Calendar = 1

    class ControlElementExt(IntEnum):
        CE_CommandButtonLabel = 0
        CE_CommandButton = 1

    class ContentsTypeExt(IntEnum):
        CT_CommandButton = 0

    class PixelMetricExt(IntEnum):
        PM_MediumIconSize = 0

    class PrimitiveElementExt(IntEnum):
        PE_CommandButtonPanel = 0
        PE_CommandButtonLabel = 1

    # -- Constructor ---------------------------------------------------

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__()
        from qlementine._theme import Theme

        self._theme: Theme = Theme()
        self._animations_enabled: bool = True
        self._auto_icon_color: AutoIconColor = AutoIconColor.None_
        self._icon_path_getter = None

    # -- Theme ---------------------------------------------------------

    def theme(self) -> Theme:
        return self._theme

    def setTheme(self, theme: Theme) -> None:
        self._theme = theme
        self.themeChanged.emit()

    def setThemeJsonPath(self, path: str) -> None:
        from qlementine._theme import Theme

        self._theme = Theme.fromJsonPath(path)
        self.themeChanged.emit()

    # -- Animations ----------------------------------------------------

    def animationsEnabled(self) -> bool:
        return self._animations_enabled

    def setAnimationsEnabled(self, enabled: bool) -> None:
        if self._animations_enabled != enabled:
            self._animations_enabled = enabled
            self.animationsEnabledChanged.emit()

    # -- AutoIconColor (instance level) --------------------------------

    def autoIconColor(self, widget: object = None) -> AutoIconColor:
        if widget is not None and hasattr(widget, "property"):
            val = widget.property(_AUTO_ICON_COLOR_PROP)
            if isinstance(val, int):
                return AutoIconColor(val)
            if isinstance(val, AutoIconColor):
                return val
            return self._auto_icon_color
        return self._auto_icon_color

    def setAutoIconColor(self, *args: object) -> None:
        if len(args) == 2:
            widget, aic = args
            if hasattr(widget, "setProperty"):
                widget.setProperty(
                    _AUTO_ICON_COLOR_PROP, int(aic)
                )
                return
        if len(args) == 1:
            self._auto_icon_color = AutoIconColor(int(args[0]))

    # -- Icon helpers --------------------------------------------------

    def setIconPathGetter(self, func: object) -> None:
        self._icon_path_getter = func

    def getColorizedPixmap(
        self,
        input: QPixmap,
        auto_icon_color: AutoIconColor,
        fg_color: QColor,
        text_color: QColor,
    ) -> QPixmap:
        return QPixmap(input)

    def makeThemedIcon(
        self,
        svg_path: str,
        size: QSize | None = None,
        role: object = None,
    ) -> QIcon:
        if size is None:
            size = QSize(16, 16)
        return QIcon(svg_path)

    def makeThemedIconFromName(
        self,
        name: str,
        size: QSize | None = None,
        role: object = None,
    ) -> QIcon:
        if size is None:
            size = QSize(16, 16)
        if self._icon_path_getter is not None:
            path = self._icon_path_getter(name)
            if path:
                return QIcon(path)
        return QIcon()

    # -- Widget status -------------------------------------------------

    def widgetStatus(self, widget: object) -> Status:
        return Status.Default

    # -- Repaint -------------------------------------------------------

    def triggerCompleteRepaint(self) -> None:
        app = QApplication.instance()
        if app is not None:
            style = app.style()
            if style is not None and hasattr(style, "polish"):
                style.polish(app)

    # -- Extended QStyle methods (stubs) -------------------------------

    def standardIconExt(
        self,
        sp: StandardPixmapExt,
        opt: object = None,
        w: object = None,
    ) -> QIcon:
        return QIcon()

    def drawPrimitiveExt(
        self,
        pe: PrimitiveElementExt,
        opt: object = None,
        p: object = None,
        w: object = None,
    ) -> None:
        pass

    def drawControlExt(
        self,
        ce: ControlElementExt,
        opt: object = None,
        p: object = None,
        w: object = None,
    ) -> None:
        pass

    def sizeFromContentsExt(
        self,
        ct: ContentsTypeExt,
        opt: object = None,
        s: QSize | None = None,
        w: object = None,
    ) -> QSize:
        if s is not None:
            return QSize(s)
        return QSize(-1, -1)

    def pixelMetricExt(
        self,
        m: PixelMetricExt,
        opt: object = None,
        w: object = None,
    ) -> int:
        if m == self.PixelMetricExt.PM_MediumIconSize:
            return self._theme.iconSizeMedium.width()
        return 0


def appStyle() -> QlementineStyle | None:
    """Return the application style if it is a QlementineStyle."""
    app = QApplication.instance()
    if app is not None:
        style = app.style()
        if isinstance(style, QlementineStyle):
            return style
    return None
