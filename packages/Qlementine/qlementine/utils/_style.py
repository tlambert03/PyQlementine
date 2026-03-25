"""Style utility functions."""

from __future__ import annotations

from qlementine._qt import QtCore, QtWidgets

QWidget = QtWidgets.QWidget
Qt = QtCore.Qt

__all__ = [
    "getHPaddings",
    "getTabCount",
    "getTabIndex",
    "shouldHaveBoldFont",
    "shouldHaveExternalFocusFrame",
    "shouldHaveHoverEvents",
    "shouldHaveMouseTracking",
    "shouldHaveTabFocus",
    "shouldNotBeVerticallyCompressed",
    "shouldNotHaveWheelEvents",
]


def shouldHaveHoverEvents(w: QWidget) -> bool:
    """Whether the widget should receive hover events."""
    return isinstance(
        w,
        (
            QtWidgets.QAbstractButton,
            QtWidgets.QComboBox,
            QtWidgets.QMenuBar,
            QtWidgets.QScrollBar,
            QtWidgets.QSplitterHandle,
            QtWidgets.QTabBar,
            QtWidgets.QAbstractSlider,
            QtWidgets.QLineEdit,
            QtWidgets.QAbstractSpinBox,
            QtWidgets.QAbstractItemView,
            QtWidgets.QGroupBox,
        ),
    ) or w.inherits("QDockSeparator") or w.inherits(
        "QDockWidgetSeparator"
    )


def shouldHaveMouseTracking(w: QWidget) -> bool:
    """Whether the widget should have mouse tracking."""
    return isinstance(w, QtWidgets.QAbstractItemView)


def shouldHaveBoldFont(w: QWidget) -> bool:
    """Whether the widget text should be bold."""
    return isinstance(
        w, (QtWidgets.QPushButton, QtWidgets.QToolButton)
    )


def shouldHaveExternalFocusFrame(w: QWidget) -> bool:
    """Whether the widget should have an external focus frame."""
    # QPlainTextEdit (before QAbstractScrollArea)
    if isinstance(w, QtWidgets.QPlainTextEdit):
        return (
            w.focusPolicy() != Qt.FocusPolicy.NoFocus
            and w.frameShape() == QtWidgets.QFrame.Shape.StyledPanel
            and w.frameShadow() != QtWidgets.QFrame.Shadow.Plain
        )
    # QTextEdit (before QAbstractScrollArea)
    if isinstance(w, QtWidgets.QTextEdit):
        return (
            w.focusPolicy() != Qt.FocusPolicy.NoFocus
            and w.frameShape() == QtWidgets.QFrame.Shape.StyledPanel
            and w.frameShadow() != QtWidgets.QFrame.Shadow.Plain
        )
    # Other QAbstractScrollArea
    if isinstance(w, QtWidgets.QAbstractScrollArea):
        return False
    # QLineEdit
    if isinstance(w, QtWidgets.QLineEdit):
        return w.focusPolicy() != Qt.FocusPolicy.NoFocus and (
            w.hasFrame()
            or isinstance(w.parentWidget(), QtWidgets.QComboBox)
        )
    # General case
    return (
        (
            isinstance(w, QtWidgets.QAbstractButton)
            and not isinstance(
                w.parentWidget(), QtWidgets.QTabBar
            )
        )
        or isinstance(w, QtWidgets.QComboBox)
        or isinstance(w, QtWidgets.QLineEdit)
        or (
            not isinstance(w, QtWidgets.QScrollBar)
            and isinstance(w, QtWidgets.QAbstractSlider)
        )
        or isinstance(w, QtWidgets.QGroupBox)
    )


def shouldHaveTabFocus(w: QWidget) -> bool:
    """Whether the widget should be focusable with Tab."""
    return (
        w is not None
        and w.focusPolicy()
        in (Qt.FocusPolicy.StrongFocus, Qt.FocusPolicy.ClickFocus)
        and isinstance(
            w,
            (QtWidgets.QAbstractButton, QtWidgets.QGroupBox),
        )
    )


def shouldNotBeVerticallyCompressed(w: QWidget) -> bool:
    """Whether the widget should not be vertically compressed."""
    return isinstance(
        w,
        (
            QtWidgets.QAbstractButton,
            QtWidgets.QComboBox,
            QtWidgets.QLineEdit,
            QtWidgets.QAbstractSpinBox,
        ),
    )


def shouldNotHaveWheelEvents(w: QWidget) -> bool:
    """Whether the widget should not receive wheel events."""
    return (
        not isinstance(w, QtWidgets.QScrollBar)
        and isinstance(w, QtWidgets.QAbstractSlider)
    ) or isinstance(w, QtWidgets.QAbstractSpinBox)


def getHPaddings(
    hasIcon: bool, hasText: bool, hasIndicator: bool, padding: int
) -> tuple[int, int]:
    """Get horizontal paddings (left, right) based on content."""
    if hasText:
        if not hasIcon and hasIndicator:
            return (padding * 2, padding)
        elif hasIcon and not hasIndicator:
            return (padding, padding * 2)
        elif hasIcon and hasIndicator:
            return (padding, padding)
        else:
            return (padding * 2, padding * 2)
    return (padding, padding)


def getTabIndex(
    optTab: QtWidgets.QStyleOptionTab, parentWidget: QWidget | None
) -> int:
    """Get the tab index from QStyleOptionTab or QTabBar."""
    if hasattr(optTab, "tabIndex"):
        return optTab.tabIndex
    if isinstance(parentWidget, QtWidgets.QTabBar):
        return parentWidget.tabAt(optTab.rect.topLeft())
    return -1


def getTabCount(parentWidget: QWidget | None) -> int:
    """Get the tab count from a QTabBar."""
    if isinstance(parentWidget, QtWidgets.QTabBar):
        return parentWidget.count()
    return -1
