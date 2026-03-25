"""Widget utility functions."""

from __future__ import annotations

from qlementine._qt import QtCore, QtGui, QtWidgets

QWidget = QtWidgets.QWidget
QFrame = QtWidgets.QFrame
QSizePolicy = QtWidgets.QSizePolicy
QGuiApplication = QtGui.QGuiApplication
QWindow = QtGui.QWindow

__all__ = [
    "centerWidget",
    "clearFocus",
    "findFirstParentOfType",
    "getDpi",
    "getWindow",
    "makeHorizontalLine",
    "makeVerticalLine",
]


def makeHorizontalLine(
    parentWidget: QWidget, maxWidth: int = -1
) -> QWidget:
    """Create a horizontal line widget."""
    lineThickness = 1
    style = parentWidget.style() if parentWidget else None
    if style is not None and hasattr(style, "theme"):
        lineThickness = style.theme().borderWidth

    line = QFrame(parentWidget)
    line.setSizePolicy(
        QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
    )
    line.setFixedHeight(lineThickness)
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Plain)

    if maxWidth >= 0:
        line.setMaximumWidth(maxWidth)

    return line


def makeVerticalLine(
    parentWidget: QWidget, maxHeight: int = -1
) -> QWidget:
    """Create a vertical line widget."""
    lineThickness = 1
    style = parentWidget.style() if parentWidget else None
    if style is not None and hasattr(style, "theme"):
        lineThickness = style.theme().borderWidth

    line = QFrame(parentWidget)
    line.setSizePolicy(
        QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding
    )
    line.setFixedWidth(lineThickness)
    line.setFrameShape(QFrame.Shape.VLine)
    line.setFrameShadow(QFrame.Shadow.Plain)

    if maxHeight >= 0:
        line.setMaximumHeight(maxHeight)

    return line


def centerWidget(
    widget: QWidget, host: QWidget | None = None
) -> None:
    """Center *widget* inside *host* or on the screen."""
    if host is None:
        host = widget.parentWidget()

    if host is not None:
        hostRect = host.geometry()
        widget.move(hostRect.center() - widget.rect().center())
    else:
        screens = QGuiApplication.screens()
        if screens:
            screenGeometry = screens[0].geometry()
            x = (screenGeometry.width() - widget.width()) // 2
            y = (screenGeometry.height() - widget.height()) // 2
            widget.move(x, y)


def getDpi(widget: QWidget | None) -> float:
    """Get the logical DPI for the widget's screen."""
    if widget is not None:
        screen = widget.screen()
        if screen is not None:
            return screen.logicalDotsPerInch()
    return 72.0


def getWindow(widget: QWidget | None) -> QWindow | None:
    """Get the QWindow for the widget."""
    if widget is not None:
        window = widget.window()
        if window is not None:
            return window.windowHandle()
    return None


def clearFocus(widget: QWidget | None, recursive: bool) -> None:
    """Clear focus from *widget* and optionally its children."""
    if widget is None:
        return
    widget.clearFocus()
    if recursive:
        for child in widget.findChildren(QWidget):
            child.clearFocus()


def findFirstParentOfType(child: QWidget, cls: type) -> QWidget | None:
    """Walk up the parent chain and return the first ancestor of *cls*."""
    parent = child
    while parent is not None:
        parent = parent.parentWidget()
        if isinstance(parent, cls):
            return parent
    return None
