"""Geometry utility functions."""

from __future__ import annotations

import math

from qlementine._qt import QtCore

QPointF = QtCore.QPointF
QRectF = QtCore.QRectF
QSizeF = QtCore.QSizeF

__all__ = [
    "isPointInRoundedRect",
]


def isPointInRoundedRect(
    point: QPointF, rect: QRectF, cornerRadius: float
) -> bool:
    """Check if *point* is inside a rounded rectangle."""
    if not rect.contains(point):
        return False
    if cornerRadius <= 1.0:
        return True

    diameter = cornerRadius * 2.0
    rect_size = QSizeF(diameter, diameter)
    corners = [
        rect.topLeft(),
        rect.topRight() - QPointF(diameter, 0.0),
        rect.bottomLeft() - QPointF(diameter, diameter),
        rect.bottomRight() - QPointF(0.0, diameter),
    ]
    for corner in corners:
        corner_rect = QRectF(corner, rect_size)
        if corner_rect.contains(point):
            center = corner_rect.center()
            dist = math.hypot(
                point.x() - center.x(), point.y() - center.y()
            )
            return dist <= cornerRadius

    return True
