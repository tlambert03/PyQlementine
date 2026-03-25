"""Icon utility functions."""

from __future__ import annotations

from qlementine._qt import QtCore, QtGui

QColor = QtGui.QColor
QIcon = QtGui.QIcon
QPainter = QtGui.QPainter
QPixmap = QtGui.QPixmap
QSize = QtCore.QSize
Qt = QtCore.Qt

__all__ = [
    "IconTheme",
    "makeIconFromSvg",
]


class IconTheme:
    """Color scheme for icon states."""

    __slots__ = ("normal", "disabled", "checkedNormal", "checkedDisabled")

    def __init__(
        self,
        normal: QColor,
        disabled: QColor | None = None,
        checkedNormal: QColor | None = None,
        checkedDisabled: QColor | None = None,
    ) -> None:
        self.normal = normal
        self.disabled = disabled if disabled is not None else normal
        self.checkedNormal = (
            checkedNormal if checkedNormal is not None else normal
        )
        self.checkedDisabled = (
            checkedDisabled
            if checkedDisabled is not None
            else self.disabled
        )

    def color(self, mode: QIcon.Mode, state: QIcon.State) -> QColor:
        """Return the color for the given icon mode and state."""
        if mode == QIcon.Mode.Disabled:
            if state == QIcon.State.On:
                return self.checkedDisabled
            return self.disabled
        if state == QIcon.State.On:
            return self.checkedNormal
        return self.normal


def makeIconFromSvg(
    svgPath: str,
    size_or_theme: QSize | IconTheme,
    size: QSize | None = None,
) -> QIcon:
    """Make a QIcon from an SVG file, optionally colorized."""
    try:
        from PySide6.QtSvg import QSvgRenderer
    except ImportError:
        from PyQt6.QtSvg import QSvgRenderer  # type: ignore

    if isinstance(size_or_theme, IconTheme):
        iconTheme = size_or_theme
        actual_size = size if size is not None else QSize(16, 16)
        return _makeIconFromSvgWithTheme(
            svgPath, iconTheme, actual_size, QSvgRenderer
        )

    actual_size = size_or_theme
    if not svgPath or actual_size.isEmpty():
        return QIcon()

    icon = QIcon()
    renderer = QSvgRenderer(svgPath)
    renderer.setAspectRatioMode(
        Qt.AspectRatioMode.KeepAspectRatio
    )

    for pxRatio in (1.0, 2.0):
        pixmap = QPixmap(actual_size * pxRatio)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing, True
        )
        renderer.render(painter, pixmap.rect())
        painter.end()
        pixmap.setDevicePixelRatio(pxRatio)

        for iconMode in (
            QIcon.Mode.Normal,
            QIcon.Mode.Disabled,
            QIcon.Mode.Active,
            QIcon.Mode.Selected,
        ):
            for iconState in (QIcon.State.On, QIcon.State.Off):
                icon.addPixmap(pixmap, iconMode, iconState)

    return icon


def _makeIconFromSvgWithTheme(
    svgPath: str,
    iconTheme: IconTheme,
    size: QSize,
    QSvgRenderer: type,
) -> QIcon:
    """Make a colorized QIcon from SVG + IconTheme."""
    from qlementine.utils._image import getColorizedPixmap

    if not svgPath or size.isEmpty():
        return QIcon()

    icon = QIcon()
    renderer = QSvgRenderer(svgPath)
    renderer.setAspectRatioMode(
        Qt.AspectRatioMode.KeepAspectRatio
    )

    for pxRatio in (1, 2):
        pixmap = QPixmap(size * pxRatio)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing, True
        )
        renderer.render(painter, pixmap.rect())
        painter.end()
        pixmap.setDevicePixelRatio(float(pxRatio))

        for iconMode in (
            QIcon.Mode.Normal,
            QIcon.Mode.Disabled,
            QIcon.Mode.Active,
            QIcon.Mode.Selected,
        ):
            for iconState in (QIcon.State.On, QIcon.State.Off):
                fgColor = iconTheme.color(iconMode, iconState)
                coloredPixmap = getColorizedPixmap(
                    pixmap, fgColor
                )
                icon.addPixmap(
                    coloredPixmap, iconMode, iconState
                )

    return icon
