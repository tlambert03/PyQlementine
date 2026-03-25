"""Badge utility functions."""

from __future__ import annotations

from qlementine._qt import QtCore, QtGui
from qlementine._enums import StatusBadge, StatusBadgeSize

QColor = QtGui.QColor
QPainter = QtGui.QPainter
QPainterPath = QtGui.QPainterPath
QPen = QtGui.QPen
QPoint = QtCore.QPoint
QPointF = QtCore.QPointF
QRect = QtCore.QRect
QRectF = QtCore.QRectF
QSize = QtCore.QSize
QMarginsF = QtCore.QMarginsF
Qt = QtCore.Qt

__all__ = [
    "drawStatusBadge",
    "getStatusBadgeColors",
    "getStatusBadgeSizes",
]


def getStatusBadgeColors(
    statusBadge: StatusBadge, theme: object
) -> tuple[QColor, QColor]:
    """Get (background, foreground) colors for a status badge."""
    fg = getattr(theme, "statusColorForeground", QColor(255, 255, 255))
    if statusBadge == StatusBadge.Error:
        bg = getattr(theme, "statusColorError", QColor(255, 0, 0))
    elif statusBadge == StatusBadge.Success:
        bg = getattr(theme, "statusColorSuccess", QColor(0, 200, 0))
    elif statusBadge == StatusBadge.Warning:
        bg = getattr(theme, "statusColorWarning", QColor(255, 200, 0))
    else:
        bg = getattr(theme, "statusColorInfo", QColor(0, 120, 212))
    return (bg, fg)


def getStatusBadgeSizes(
    statusBadgeSize: StatusBadgeSize, theme: object
) -> tuple[QSize, QSize]:
    """Get (badge size, icon size) for a status badge."""
    if statusBadgeSize == StatusBadgeSize.Small:
        h = getattr(theme, "controlHeightSmall", 20)
        return (QSize(h, h), QSize(10, 10))
    h = getattr(theme, "controlHeightMedium", 28)
    iconSize = getattr(theme, "iconSize", QSize(16, 16))
    return (QSize(h, h), iconSize)


def _drawStatusBadgeIcon(
    p: QPainter,
    rect: QRect,
    statusBadge: StatusBadge,
    size: StatusBadgeSize,
    color: QColor,
    lineThickness: float,
) -> None:
    """Draw the icon shape for a status badge."""
    from qlementine.utils._primitive import drawRoundedTriangle

    w = rect.width()
    h = rect.width()
    x = rect.x()
    y = rect.y()

    if statusBadge == StatusBadge.Success:
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(
            QPen(
                color,
                lineThickness,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )
        halfLT = lineThickness * 0.5
        ellipseRect = QRectF(rect).marginsRemoved(
            QMarginsF(halfLT, halfLT, halfLT, halfLT)
        )
        p.drawEllipse(ellipseRect)

        if size == StatusBadgeSize.Small:
            s = 10.0
            path = QPainterPath()
            path.moveTo(QPointF((3.0 / s) * w + x, (5.0 / s) * h + y))
            path.lineTo(QPointF((4.5 / s) * w + x, (6.5 / s) * h + y))
            path.lineTo(QPointF((7.0 / s) * w + x, (4.0 / s) * h + y))
            p.drawPath(path)
        else:
            s = 16.0
            path = QPainterPath()
            path.moveTo(QPointF((5.0 / s) * w + x, (8.5 / s) * h + y))
            path.lineTo(QPointF((7.0 / s) * w + x, (10.5 / s) * h + y))
            path.lineTo(QPointF((11.0 / s) * w + x, (6.5 / s) * h + y))
            p.drawPath(path)

    elif statusBadge == StatusBadge.Info:
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(
            QPen(
                color,
                lineThickness,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )
        halfLT = lineThickness * 0.5
        ellipseRect = QRectF(rect).marginsRemoved(
            QMarginsF(halfLT, halfLT, halfLT, halfLT)
        )
        p.drawEllipse(ellipseRect)

        if size == StatusBadgeSize.Small:
            s = 10.0
            p.drawLine(
                QPointF((5.0 / s) * w + x, (5.0 / s) * h + y),
                QPointF((5.0 / s) * w + x, (7.0 / s) * h + y),
            )
            ellipseCenter = QPointF(
                (5.0 / s) * w + x, (3.0 / s) * h + y
            )
            ellipseRadius = (1.1 * lineThickness / s) * w
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(color)
            p.drawEllipse(ellipseCenter, ellipseRadius, ellipseRadius)
        else:
            s = 16.0
            path = QPainterPath()
            path.moveTo(QPointF((6.75 / s) * w + x, (7.0 / s) * h + y))
            path.lineTo(QPointF((8.0 / s) * w + x, (7.0 / s) * h + y))
            path.lineTo(QPointF((8.0 / s) * w + x, (12.0 / s) * h + y))
            p.drawPath(path)
            p.drawLine(
                QPointF((6.75 / s) * w + x, (12.0 / s) * h + y),
                QPointF((9.25 / s) * w + x, (12.0 / s) * h + y),
            )
            ellipseCenter = QPointF(
                (8.0 / s) * w + x, (4.0 / s) * h + y
            )
            ellipseRadius = (1.1 * lineThickness / s) * w
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(color)
            p.drawEllipse(ellipseCenter, ellipseRadius, ellipseRadius)

    elif statusBadge == StatusBadge.Warning:
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(
            QPen(
                color,
                lineThickness,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )

        if size == StatusBadgeSize.Small:
            s = 10.0
            triangleMargin = (1.0 / s) * w
            triangleDeltaY = (1.5 / s) * h
            triangleRadius = (1.0 / s) * h
            triangleRect = (
                QRectF(rect)
                .marginsAdded(
                    QMarginsF(
                        triangleMargin,
                        triangleMargin,
                        triangleMargin,
                        triangleMargin,
                    )
                )
                .translated(QPointF(0.0, triangleDeltaY))
            )
            drawRoundedTriangle(p, triangleRect, triangleRadius)
            p.drawLine(
                QPointF((5.0 / s) * w + x, (2.5 / s) * h + y),
                QPointF((5.0 / s) * w + x, (6.5 / s) * h + y),
            )
            ellipseCenter = QPointF(
                (5.0 / s) * w + x, (9.0 / s) * h + y
            )
            ellipseRadius = (1.1 * lineThickness / s) * w
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(color)
            p.drawEllipse(ellipseCenter, ellipseRadius, ellipseRadius)
        else:
            s = 16.0
            triangleMargin = (1.0 / s) * w
            triangleDeltaY = (2.5 / s) * h
            triangleRadius = (2.0 / s) * h
            triangleRect = (
                QRectF(rect)
                .marginsAdded(
                    QMarginsF(
                        triangleMargin,
                        triangleMargin,
                        triangleMargin,
                        triangleMargin,
                    )
                )
                .translated(QPointF(0.0, triangleDeltaY))
            )
            drawRoundedTriangle(p, triangleRect, triangleRadius)
            p.drawLine(
                QPointF((8.0 / s) * w + x, (5.5 / s) * h + y),
                QPointF((8.0 / s) * w + x, (9.5 / s) * h + y),
            )
            ellipseCenter = QPointF(
                (8.0 / s) * w + x, (12.0 / s) * h + y
            )
            ellipseRadius = (1.1 * lineThickness / s) * w
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(color)
            p.drawEllipse(ellipseCenter, ellipseRadius, ellipseRadius)

    elif statusBadge == StatusBadge.Error:
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(
            QPen(
                color,
                lineThickness,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )

        if size == StatusBadgeSize.Small:
            s = 10.0
            path = QPainterPath()
            coords = [
                (3.0, 0.5), (7.0, 0.5), (9.5, 3.0), (9.5, 7.0),
                (7.0, 9.5), (3.0, 9.5), (0.5, 7.0), (0.5, 3.0),
            ]
            for i, (cx, cy) in enumerate(coords):
                pt = QPointF((cx / s) * w + x, (cy / s) * h + y)
                if i == 0:
                    path.moveTo(pt)
                else:
                    path.lineTo(pt)
            path.closeSubpath()
            p.drawPath(path)
            p.drawLine(
                QPointF((3.5 / s) * w + x, (3.5 / s) * h + y),
                QPointF((6.5 / s) * w + x, (6.5 / s) * h + y),
            )
            p.drawLine(
                QPointF((3.5 / s) * w + x, (6.5 / s) * h + y),
                QPointF((6.5 / s) * w + x, (3.5 / s) * h + y),
            )
        else:
            s = 16.0
            path = QPainterPath()
            coords = [
                (4.5, 0.5), (11.5, 0.5), (15.5, 4.5), (15.5, 11.5),
                (11.5, 15.5), (4.5, 15.5), (0.5, 11.5), (0.5, 4.5),
            ]
            for i, (cx, cy) in enumerate(coords):
                pt = QPointF((cx / s) * w + x, (cy / s) * h + y)
                if i == 0:
                    path.moveTo(pt)
                else:
                    path.lineTo(pt)
            path.closeSubpath()
            p.drawPath(path)
            p.drawLine(
                QPointF((5.5 / s) * w + x, (5.5 / s) * h + y),
                QPointF((10.5 / s) * w + x, (10.5 / s) * h + y),
            )
            p.drawLine(
                QPointF((10.5 / s) * w + x, (5.5 / s) * h + y),
                QPointF((5.5 / s) * w + x, (10.5 / s) * h + y),
            )


def drawStatusBadge(
    p: QPainter,
    rect: QRect,
    statusBadge: StatusBadge,
    size: StatusBadgeSize,
    theme: object,
) -> None:
    """Draw a status badge (background + icon)."""
    bgColor, fgColor = getStatusBadgeColors(statusBadge, theme)
    badgeSize, iconSize = getStatusBadgeSizes(size, theme)

    badgeRect = QRect(
        QPoint(
            rect.x() + (rect.width() - badgeSize.width()) // 2,
            rect.y() + (rect.height() - badgeSize.height()) // 2,
        ),
        badgeSize,
    )
    iconRect = QRect(
        QPoint(
            rect.x() + (rect.width() - iconSize.width()) // 2,
            rect.y() + (rect.height() - iconSize.height()) // 2,
        ),
        iconSize,
    )
    radius = badgeRect.height() / 4.0

    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(bgColor)
    p.drawRoundedRect(badgeRect, radius, radius)

    lineThickness = 1.0001
    _drawStatusBadgeIcon(
        p, iconRect, statusBadge, size, fgColor, lineThickness
    )
