"""Layout utility functions."""

from __future__ import annotations

from qlementine._qt import QtCore, QtWidgets

QMargins = QtCore.QMargins
QWidget = QtWidgets.QWidget
QLayout = QtWidgets.QLayout
QStyle = QtWidgets.QStyle

__all__ = [
    "clearLayout",
    "getFormLayoutProps",
    "getHLayoutProps",
    "getLayoutHSpacing",
    "getLayoutMargins",
    "getLayoutVSpacing",
    "getVLayoutProps",
]


def getLayoutMargins(widget: QWidget | None) -> QMargins:
    """Retrieve the widget's QStyle margins."""
    style = widget.style() if widget else None
    if style is not None:
        left = style.pixelMetric(QStyle.PixelMetric.PM_LayoutLeftMargin)
        top = style.pixelMetric(QStyle.PixelMetric.PM_LayoutTopMargin)
        right = style.pixelMetric(
            QStyle.PixelMetric.PM_LayoutRightMargin
        )
        bottom = style.pixelMetric(
            QStyle.PixelMetric.PM_LayoutBottomMargin
        )
        return QMargins(left, top, right, bottom)
    return QMargins(0, 0, 0, 0)


def getLayoutHSpacing(widget: QWidget | None) -> int:
    """Retrieve the widget's QStyle horizontal spacing."""
    style = widget.style() if widget else None
    if style is not None:
        return style.pixelMetric(
            QStyle.PixelMetric.PM_LayoutHorizontalSpacing
        )
    return 0


def getLayoutVSpacing(widget: QWidget | None) -> int:
    """Retrieve the widget's QStyle vertical spacing."""
    style = widget.style() if widget else None
    if style is not None:
        return style.pixelMetric(
            QStyle.PixelMetric.PM_LayoutVerticalSpacing
        )
    return 0


def getVLayoutProps(
    widget: QWidget | None,
) -> tuple[int, QMargins]:
    """Retrieve vertical spacing and margins."""
    return (getLayoutVSpacing(widget), getLayoutMargins(widget))


def getHLayoutProps(
    widget: QWidget | None,
) -> tuple[int, QMargins]:
    """Retrieve horizontal spacing and margins."""
    return (getLayoutHSpacing(widget), getLayoutMargins(widget))


def getFormLayoutProps(
    widget: QWidget | None,
) -> tuple[int, int, QMargins]:
    """Retrieve vertical/horizontal spacings and margins."""
    return (
        getLayoutVSpacing(widget),
        getLayoutHSpacing(widget),
        getLayoutMargins(widget),
    )


def clearLayout(layout: QLayout) -> None:
    """Remove and delete all elements in the layout."""
    while layout.count() > 0:
        item = layout.takeAt(0)
        if item is None:
            break
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()
        elif item.layout() is not None:
            clearLayout(item.layout())
