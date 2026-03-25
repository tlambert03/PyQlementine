"""Font utility functions."""

from __future__ import annotations

from qlementine._qt import QtCore, QtGui

QFontMetrics = QtGui.QFontMetrics
Qt = QtCore.Qt

__all__ = [
    "pixelSizeToPointSize",
    "pointSizeToPixelSize",
    "textWidth",
]

_STANDARD_DPI = 72.0


def pointSizeToPixelSize(pointSize: float, dpi: float) -> float:
    """Convert a point size to pixel size given *dpi*."""
    return pointSize / _STANDARD_DPI * dpi


def pixelSizeToPointSize(pixelSize: float, dpi: float) -> float:
    """Convert a pixel size to point size given *dpi*."""
    return pixelSize * _STANDARD_DPI / dpi if dpi != 0 else 0.0


def textWidth(fontMetrics: QFontMetrics, text: str) -> int:
    """Return the width of *text* using *fontMetrics*."""
    from qlementine._qt import QtCore

    return fontMetrics.boundingRect(
        QtCore.QRect(), Qt.AlignmentFlag.AlignCenter, text, 0
    ).width()
