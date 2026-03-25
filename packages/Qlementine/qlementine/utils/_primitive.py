"""Primitive drawing utility functions."""

from __future__ import annotations

import math

from qlementine._qt import QtCore, QtGui, QtWidgets
from qlementine._enums import CheckState, MouseState
from qlementine._radiuses import RadiusesF

QColor = QtGui.QColor
QIcon = QtGui.QIcon
QImage = QtGui.QImage
QPainter = QtGui.QPainter
QPainterPath = QtGui.QPainterPath
QPen = QtGui.QPen
QPixmap = QtGui.QPixmap
QBrush = QtGui.QBrush
QKeySequence = QtGui.QKeySequence
QFontMetrics = QtGui.QFontMetrics
QPixmapCache = QtGui.QPixmapCache
QTextLayout = QtGui.QTextLayout

QPoint = QtCore.QPoint
QPointF = QtCore.QPointF
QRect = QtCore.QRect
QRectF = QtCore.QRectF
QSize = QtCore.QSize
QSizeF = QtCore.QSizeF
QMarginsF = QtCore.QMarginsF
QMargins = QtCore.QMargins
Qt = QtCore.Qt

QStyle = QtWidgets.QStyle
QWidget = QtWidgets.QWidget
QApplication = QtWidgets.QApplication

QLEMENTINE_PI = 3.14159265358979323846
_PI_4 = QLEMENTINE_PI / 4.0

__all__ = [
    "QLEMENTINE_PI",
    "displayedShortcutString",
    "drawArrowDown",
    "drawArrowLeft",
    "drawArrowRight",
    "drawArrowUp",
    "drawCalendarIndicator",
    "drawCheckBoxIndicator",
    "drawCheckButton",
    "drawCheckerboard",
    "drawCloseIndicator",
    "drawColorMark",
    "drawComboBoxIndicator",
    "drawDebugRect",
    "drawElidedMultiLineText",
    "drawEllipseBorder",
    "drawGripIndicator",
    "drawIcon",
    "drawMenuSeparator",
    "drawPartiallyCheckedCheckBoxIndicator",
    "drawProgressBarValueRect",
    "drawRadioButton",
    "drawRadioButtonIndicator",
    "drawRectBorder",
    "drawRoundedRect",
    "drawRoundedRectBorder",
    "drawRoundedTriangle",
    "drawShortcut",
    "drawTab",
    "drawTabShadow",
    "drawTreeViewIndicator",
    "getMenuIndicatorPath",
    "getMultipleRadiusesRectPath",
    "getPixelRatio",
    "getTabPath",
    "getTickInterval",
    "makeArrowLeftPixmap",
    "makeArrowRightPixmap",
    "makeCheckPixmap",
    "makeMessageBoxCriticalPixmap",
    "makeMessageBoxInformationPixmap",
    "makeMessageBoxQuestionPixmap",
    "makeMessageBoxWarningPixmap",
    "drawDial",
    "drawDialTickMarks",
    "drawSliderTickMarks",
    "drawSpinBoxArrowIndicator",
    "drawSubMenuIndicator",
    "getMenuLabelAndShortcut",
    "getPixmap",
    "removeTrailingWhitespaces",
    "shortcutSizeHint",
]


# -- helpers --


def _getLength(x: float, y: float) -> float:
    return math.sqrt(x * x + y * y)


def _getColinearVector(
    point: QPointF, partLength: float, vx: float, vy: float
) -> QPointF:
    vLen = _getLength(vx, vy)
    factor = partLength / vLen if vLen != 0 else 0
    return QPointF(point.x() - vx * factor, point.y() - vy * factor)


def _getAngleRadius(
    p1: QPointF, angular: QPointF, p2: QPointF, radius: float
) -> dict:
    v1x = angular.x() - p1.x()
    v1y = angular.y() - p1.y()
    v2x = angular.x() - p2.x()
    v2y = angular.y() - p2.y()

    vectorsAngle = math.atan2(v1y, v1x) - math.atan2(v2y, v2x)
    tan = math.tan(vectorsAngle / 2.0)
    segment = radius / tan if tan != 0 else 0

    length1 = _getLength(v1x, v1y)
    length2 = _getLength(v2x, v2y)
    length = min(length1, length2)
    if abs(segment) > length:
        segment = length
        radius = length * tan

    startPoint = _getColinearVector(angular, segment, v1x, v1y)
    endPoint = _getColinearVector(angular, segment, v2x, v2y)

    dx = angular.x() * 2.0 - startPoint.x() - endPoint.x()
    dy = angular.y() * 2.0 - startPoint.y() - endPoint.y()
    d = _getLength(segment, radius)
    circleCenter = _getColinearVector(angular, d, dx, dy)

    startAngle = -math.atan2(
        startPoint.y() - circleCenter.y(),
        startPoint.x() - circleCenter.x(),
    )
    endAngle = -math.atan2(
        endPoint.y() - circleCenter.y(),
        endPoint.x() - circleCenter.x(),
    )

    sweepAngle = endAngle - startAngle
    if sweepAngle > 0.0:
        startAngle = 2 * QLEMENTINE_PI + startAngle
        sweepAngle = endAngle - startAngle

    pointOnCircle = _getColinearVector(
        circleCenter,
        radius,
        circleCenter.x() - angular.x(),
        circleCenter.y() - angular.y(),
    )
    translationX = 2 * int(angular.x() - pointOnCircle.x())
    translationY = 2 * int(angular.y() - pointOnCircle.y())

    rad2deg = 180.0 / QLEMENTINE_PI
    return {
        "radius": radius,
        "startAngle": startAngle * rad2deg,
        "sweepAngle": sweepAngle * rad2deg,
        "centerPoint": circleCenter,
        "startPoint": startPoint,
        "endPoint": endPoint,
        "translation": QPointF(translationX, translationY),
    }


# -- public functions --


def getPixelRatio(w: QWidget | None) -> float:
    """Get the device pixel ratio for the widget."""
    window = w.window().windowHandle() if w and w.window() else None
    return window.devicePixelRatio() if window else 1.0


def drawEllipseBorder(
    p: QPainter,
    rect: QRectF,
    color: QColor,
    borderWidth: float,
) -> None:
    """Draw an antialiased pixel-perfect ellipse border."""
    halfBW = borderWidth / 2.0
    borderRect = rect.marginsRemoved(
        QMarginsF(halfBW, halfBW, halfBW, halfBW)
    )
    p.setPen(QPen(color, borderWidth, Qt.PenStyle.SolidLine))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawEllipse(borderRect)


def getMultipleRadiusesRectPath(
    rect: QRectF, radiuses: RadiusesF
) -> QPainterPath:
    """Generate a QPainterPath for a rounded rect with per-corner radii."""
    path = QPainterPath()
    w = float(rect.width())
    h = float(rect.height())
    x = float(rect.x())
    y = float(rect.y())

    half = max(w / 2.0, h / 2.0)
    tl = min(half, max(0.0, radiuses.topLeft * 2))
    tr = min(half, max(0.0, radiuses.topRight * 2))
    br = min(half, max(0.0, radiuses.bottomRight * 2))
    bl = min(half, max(0.0, radiuses.bottomLeft * 2))

    path.moveTo(x, y + tl)
    if tl > 0:
        path.arcTo(x, y, tl, tl, 180.0, -90.0)

    if tr > 0:
        path.lineTo(x + w - tr, y)
        path.arcTo(x + w - tr, y, tr, tr, 90.0, -90.0)
    else:
        path.lineTo(x + w, y)

    if br > 0:
        path.lineTo(x + w, y + h - br)
        path.arcTo(x + w - br, y + h - br, br, br, 0.0, -90.0)
    else:
        path.lineTo(x + w, y + h)

    if bl > 0:
        path.lineTo(x + bl, y + h)
        path.arcTo(x, y + h - bl, bl, bl, 270.0, -90.0)
    else:
        path.lineTo(x, y + h)

    path.closeSubpath()
    return path


def drawRoundedRect(
    p: QPainter,
    rect: QRectF | QRect,
    brush: QBrush,
    radius_or_radiuses: float | RadiusesF = 0.0,
) -> None:
    """Draw an antialiased rounded rectangle."""
    if isinstance(rect, QRect):
        rect = QRectF(rect)

    if isinstance(radius_or_radiuses, RadiusesF):
        radiuses = radius_or_radiuses
        if radiuses.hasSameRadius():
            drawRoundedRect(p, rect, brush, radiuses.topLeft)
        else:
            path = getMultipleRadiusesRectPath(rect, radiuses)
            p.setRenderHint(
                QPainter.RenderHint.Antialiasing, True
            )
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(brush)
            p.drawPath(path)
        return

    radius = float(radius_or_radiuses)
    if radius < 0.1:
        p.fillRect(rect, brush)
    else:
        p.setRenderHint(
            QPainter.RenderHint.Antialiasing, True
        )
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(brush)
        p.drawRoundedRect(rect, radius, radius)


def drawRoundedRectBorder(
    p: QPainter,
    rect: QRectF | QRect,
    color: QColor,
    borderWidth: float,
    radius_or_radiuses: float | RadiusesF = 0.0,
) -> None:
    """Draw an antialiased pixel-perfect rounded rect border."""
    if isinstance(rect, QRect):
        rect = QRectF(rect)

    if borderWidth <= 0:
        return

    if isinstance(radius_or_radiuses, RadiusesF):
        radiuses = radius_or_radiuses
        if radiuses.hasSameRadius():
            drawRoundedRectBorder(
                p, rect, color, borderWidth, radiuses.topLeft
            )
        else:
            p.setRenderHint(
                QPainter.RenderHint.Antialiasing, True
            )
            p.setPen(
                QPen(
                    color,
                    borderWidth,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.SquareCap,
                    Qt.PenJoinStyle.MiterJoin,
                )
            )
            p.setBrush(Qt.BrushStyle.NoBrush)
            halfBW = borderWidth / 2.0
            borderRect = rect.marginsRemoved(
                QMarginsF(halfBW, halfBW, halfBW, halfBW)
            )
            borderRadiuses = RadiusesF(
                max(0, radiuses.topLeft - halfBW),
                max(0, radiuses.topRight - halfBW),
                max(0, radiuses.bottomRight - halfBW),
                max(0, radiuses.bottomLeft - halfBW),
            )
            if all(
                r < 0.1
                for r in (
                    borderRadiuses.topLeft,
                    borderRadiuses.topRight,
                    borderRadiuses.bottomRight,
                    borderRadiuses.bottomLeft,
                )
            ):
                p.drawRect(borderRect)
            else:
                path = getMultipleRadiusesRectPath(
                    borderRect, borderRadiuses
                )
                p.drawPath(path)
        return

    radius = float(radius_or_radiuses)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(
        QPen(
            color,
            borderWidth,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
    )
    p.setBrush(Qt.BrushStyle.NoBrush)
    halfBW = borderWidth / 2.0
    borderRect = rect.marginsRemoved(
        QMarginsF(halfBW, halfBW, halfBW, halfBW)
    )
    borderRadius = radius - halfBW
    if borderRadius < 0.1:
        p.drawRect(borderRect)
    else:
        p.drawRoundedRect(borderRect, borderRadius, borderRadius)


def drawRectBorder(
    p: QPainter,
    rect: QRectF | QRect,
    color: QColor,
    borderWidth: float,
) -> None:
    """Draw a pixel-perfect rect border."""
    if isinstance(rect, QRect):
        rect = QRectF(rect)
    if borderWidth <= 0:
        return
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(
        QPen(
            color,
            borderWidth,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.SquareCap,
            Qt.PenJoinStyle.BevelJoin,
        )
    )
    p.setBrush(Qt.BrushStyle.NoBrush)
    halfBW = borderWidth / 2.0
    borderRect = rect.marginsRemoved(
        QMarginsF(halfBW, halfBW, halfBW, halfBW)
    )
    p.drawRect(borderRect)


def drawRoundedTriangle(
    p: QPainter, rect: QRectF, radius: float = 0.0
) -> None:
    """Draw an antialiased rounded triangle."""
    w = rect.width()
    h = rect.height()
    x = rect.x()
    y = rect.y()

    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    pt1 = QPointF(x + w / 2.0, y)
    pt2 = QPointF(x + w, y + h)
    pt3 = QPointF(x, y + h)

    a1 = _getAngleRadius(pt3, pt1, pt2, radius)
    a2 = _getAngleRadius(pt1, pt2, pt3, radius)
    a3 = _getAngleRadius(pt2, pt3, pt1, radius)

    diameter = radius * 2.0
    path = QPainterPath()
    path.moveTo(a1["startPoint"])
    path.arcTo(
        QRectF(
            a1["centerPoint"].x() - radius,
            a1["centerPoint"].y() - radius,
            diameter,
            diameter,
        ),
        a1["startAngle"],
        a1["sweepAngle"],
    )
    path.lineTo(a2["startPoint"])
    path.arcTo(
        QRectF(
            a2["centerPoint"].x() - radius,
            a2["centerPoint"].y() - radius,
            diameter,
            diameter,
        ),
        a2["startAngle"],
        a2["sweepAngle"],
    )
    path.lineTo(a3["startPoint"])
    path.arcTo(
        QRectF(
            a3["centerPoint"].x() - radius,
            a3["centerPoint"].y() - radius,
            diameter,
            diameter,
        ),
        a3["startAngle"],
        a3["sweepAngle"],
    )
    path.lineTo(a1["startPoint"])
    path.closeSubpath()

    tr_x = (
        a1["translation"].x()
        + a2["translation"].x()
        + a3["translation"].x()
    )
    tr_y = (
        a1["translation"].y()
        + a2["translation"].y()
        + a3["translation"].y()
    )

    p.translate(tr_x, tr_y)
    p.drawPath(path)
    p.translate(-tr_x, -tr_y)


def drawCheckerboard(
    p: QPainter,
    rect: QRectF,
    darkColor: QColor,
    lightColor: QColor,
    cellWidth: float,
) -> None:
    """Draw a checkerboard pattern."""
    hCells = int(rect.width() / cellWidth)
    vCells = int(rect.height() / cellWidth)

    p.setPen(Qt.PenStyle.NoPen)
    for i in range(hCells):
        for j in range(vCells):
            c = darkColor if (i + j) % 2 == 0 else lightColor
            cx = rect.x() + i * cellWidth
            cy = rect.y() + j * cellWidth
            cw = max(1.0, hCells - i) * cellWidth
            ch = max(1.0, vCells - j) * cellWidth
            p.setBrush(c)
            p.drawRect(QRectF(cx, cy, cw, ch))


def drawProgressBarValueRect(
    p: QPainter,
    rect: QRect,
    color: QColor,
    min_: float,
    max_: float,
    value: float,
    radius: float = 0.0,
    inverted: bool = False,
) -> None:
    """Draw the value portion of a progress bar."""
    ratio = (value - min_) / (max_ - min_) if max_ != min_ else 0
    w = int(rect.width() * ratio)
    x = rect.x() + rect.width() - w if inverted else rect.x()
    valueRect = QRect(x, rect.y(), w, rect.height())

    clipPath = QPainterPath()
    clipPath.addRoundedRect(QRectF(rect), radius, radius)
    p.save()
    p.setClipPath(clipPath)
    p.fillRect(valueRect, color)
    p.restore()


def drawColorMark(
    p: QPainter,
    rect: QRect,
    color: QColor,
    borderColor: QColor,
    borderWidth: int = 1,
) -> None:
    """Draw a color mark (circle with optional border)."""
    diam = rect.height()
    markRect = QRect(
        (rect.width() - diam) // 2, 0, diam, diam
    )
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    if color.alphaF() < 1.0:
        darkCell = QColor(220, 220, 220)
        lightCell = QColor(255, 255, 255)
        clipPath = QPainterPath()
        clipPath.addEllipse(QRectF(markRect))
        p.save()
        p.setClipPath(clipPath)
        drawCheckerboard(p, QRectF(markRect), darkCell, lightCell, 8)
        p.restore()

    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(color)
    p.drawEllipse(markRect)

    borderWidth = max(1, borderWidth)
    drawEllipseBorder(
        p, QRectF(markRect), borderColor, borderWidth * 1.5
    )


def drawDebugRect(rect: QRect, p: QPainter) -> None:
    """Draw a semi-transparent red debug rectangle."""
    p.fillRect(rect, QColor(255, 0, 0, 32))


def getMenuIndicatorPath(rect: QRect) -> QPainterPath:
    """Get the path for a menu arrow indicator."""
    w = rect.width()
    h = rect.width()
    x = rect.x()
    y = rect.y()
    s = 16.0

    path = QPainterPath()
    path.moveTo(QPointF((3.5 / s) * w + x, (6.5 / s) * h + y))
    path.lineTo(QPointF((8.0 / s) * w + x, (11.0 / s) * h + y))
    path.lineTo(QPointF((12.5 / s) * w + x, (6.5 / s) * h + y))
    return path


def drawComboBoxIndicator(rect: QRect, p: QPainter) -> None:
    """Draw the combobox double arrow."""
    w = rect.width()
    h = rect.width()
    x = rect.x()
    y = rect.y()
    s = 16.0

    path1 = QPainterPath()
    path1.moveTo(QPointF((5.5 / s) * w + x, (5.5 / s) * h + y))
    path1.lineTo(QPointF((8.0 / s) * w + x, (3.0 / s) * h + y))
    path1.lineTo(QPointF((10.5 / s) * w + x, (5.5 / s) * h + y))
    p.drawPath(path1)

    path2 = QPainterPath()
    path2.moveTo(QPointF((5.5 / s) * w + x, (10.5 / s) * h + y))
    path2.lineTo(QPointF((8.0 / s) * w + x, (13.0 / s) * h + y))
    path2.lineTo(QPointF((10.5 / s) * w + x, (10.5 / s) * h + y))
    p.drawPath(path2)


def drawCheckBoxIndicator(
    rect: QRect, p: QPainter, progress: float = 1.0
) -> None:
    """Draw a checkbox check mark indicator."""
    w = rect.width()
    h = rect.width()
    x = rect.x()
    y = rect.y()
    s = 16.0

    p1 = QPointF((4.5 / s) * w + x, (8.5 / s) * h + y)
    p2 = QPointF((7.0 / s) * w + x, (11.0 / s) * h + y)
    p3 = QPointF((11.5 / s) * w + x, (5.5 / s) * h + y)

    path = QPainterPath()
    path.moveTo(p1)
    path.lineTo(p2)
    path.lineTo(p3)

    if 1.0 - progress > 0.01:
        lastPoint = path.pointAtPercent(progress)
        trimmed = QPainterPath()
        trimmed.moveTo(p1)
        if progress < 0.5:
            trimmed.lineTo(lastPoint)
        else:
            trimmed.lineTo(p2)
            trimmed.lineTo(lastPoint)
        path = trimmed

    p.drawPath(path)


def drawPartiallyCheckedCheckBoxIndicator(
    rect: QRect, p: QPainter, progress: float = 1.0
) -> None:
    """Draw a partially-checked checkbox indicator (dash)."""
    w = rect.width()
    h = rect.width()
    x = rect.x()
    y = rect.y()
    s = 16.0

    p1 = QPointF((4.0 / s) * w + x, (8.0 / s) * h + y)
    p2 = QPointF((12.0 / s) * w + x, (8.0 / s) * h + y)

    path = QPainterPath()
    path.moveTo(p1)
    path.lineTo(p2)

    if 1.0 - progress > 0.01:
        lastPoint = path.pointAtPercent(progress)
        trimmed = QPainterPath()
        trimmed.moveTo(p1)
        trimmed.lineTo(lastPoint)
        path = trimmed

    p.drawPath(path)


def drawRadioButtonIndicator(
    rect: QRect, p: QPainter, progress: float = 1.0
) -> None:
    """Draw a radio button indicator (circle)."""
    ratio = 8.0 / 16.0
    iw = rect.width() * ratio * progress
    ih = rect.height() * ratio * progress
    ellipseRect = QRectF(
        rect.x() + (rect.width() - iw) / 2.0,
        rect.y() + (rect.height() - ih) / 2.0,
        iw,
        ih,
    )
    p.drawEllipse(ellipseRect)


def _drawArrow(
    rect: QRect,
    p: QPainter,
    coords: list[tuple[float, float]],
) -> None:
    w = rect.width()
    h = rect.width()
    x = rect.x()
    y = rect.y()
    s = 16.0
    path = QPainterPath()
    for i, (cx, cy) in enumerate(coords):
        pt = QPointF((cx / s) * w + x, (cy / s) * h + y)
        if i == 0:
            path.moveTo(pt)
        else:
            path.lineTo(pt)
    p.drawPath(path)


def drawArrowRight(rect: QRect, p: QPainter) -> None:
    """Draw a right-pointing arrow."""
    _drawArrow(rect, p, [(6.5, 4.5), (10.0, 8.0), (6.5, 11.5)])


def drawArrowLeft(rect: QRect, p: QPainter) -> None:
    """Draw a left-pointing arrow."""
    _drawArrow(rect, p, [(9.5, 4.5), (6.0, 8.0), (9.5, 11.5)])


def drawArrowDown(rect: QRect, p: QPainter) -> None:
    """Draw a downward-pointing arrow."""
    _drawArrow(rect, p, [(4.5, 6.5), (8.0, 10.0), (11.5, 6.5)])


def drawArrowUp(rect: QRect, p: QPainter) -> None:
    """Draw an upward-pointing arrow."""
    _drawArrow(rect, p, [(4.5, 10.0), (8.0, 6.5), (11.5, 10.0)])


def drawCloseIndicator(rect: QRect, p: QPainter) -> None:
    """Draw a close (X) indicator."""
    w = rect.width()
    h = rect.width()
    x = rect.x()
    y = rect.y()
    s = 16.0

    p.drawLine(
        QPointF((4.0 / s) * w + x, (4.0 / s) * h + y),
        QPointF((12.0 / s) * w + x, (12.0 / s) * h + y),
    )
    p.drawLine(
        QPointF((12.0 / s) * w + x, (4.0 / s) * h + y),
        QPointF((4.0 / s) * w + x, (12.0 / s) * h + y),
    )


def drawTreeViewIndicator(
    rect: QRect, p: QPainter, opened: bool
) -> None:
    """Draw a treeview expand/collapse indicator."""
    if opened:
        drawArrowDown(rect, p)
    else:
        drawArrowRight(rect, p)


def drawCalendarIndicator(
    rect: QRect, p: QPainter, color: QColor
) -> None:
    """Draw a calendar indicator."""
    defaultSize = 16.0
    defaultPenWidth = 1.01
    defaultRadius = 2.5
    defaultDayRadius = 0.5
    sizeRatio = rect.width() / defaultSize
    penWidth = sizeRatio * defaultPenWidth
    radius = sizeRatio * defaultRadius
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(
        QPen(
            color,
            penWidth,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
    )
    drawRoundedRectBorder(
        p,
        QRectF(
            rect.x() + sizeRatio * 1.0,
            rect.y() + sizeRatio * 1.0,
            sizeRatio * 14,
            sizeRatio * 14,
        ),
        Qt.GlobalColor.black,
        penWidth,
        radius,
    )
    p.drawLine(
        sizeRatio * QPointF(1.5, 5.5),
        sizeRatio * QPointF(14.5, 5.5),
    )
    p.drawLine(
        sizeRatio * QPointF(4.5, 0.5),
        sizeRatio * QPointF(4.5, 2.5),
    )
    p.drawLine(
        sizeRatio * QPointF(11.5, 0.5),
        sizeRatio * QPointF(11.5, 2.5),
    )

    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(color)
    dayBlockSize = sizeRatio * QSizeF(2.0, 2.0)
    for dx, dy in [
        (4.0, 7.0),
        (7.0, 7.0),
        (10.0, 7.0),
        (4.0, 10.0),
        (7.0, 10.0),
    ]:
        p.drawRoundedRect(
            QRectF(
                rect.topLeft() + sizeRatio * QPointF(dx, dy),
                dayBlockSize,
            ),
            defaultDayRadius,
            defaultDayRadius,
        )


def drawGripIndicator(
    rect: QRect,
    p: QPainter,
    color: QColor,
    orientation: Qt.Orientation,
) -> None:
    """Draw a grip indicator for drag & drop."""
    defaultSize = 16.0
    defaultBulletDiam = 2.0

    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(color)

    wR = rect.width() / defaultSize
    hR = rect.height() / defaultSize
    bulletSize = QSize(
        int(defaultBulletDiam * wR), int(defaultBulletDiam * hR)
    )

    if orientation == Qt.Orientation.Vertical:
        positions = [
            (5, 3), (5, 7), (5, 11), (9, 3), (9, 7), (9, 11)
        ]
    else:
        positions = [
            (3, 5), (7, 5), (11, 5), (3, 9), (7, 9), (11, 9)
        ]

    tl = rect.topLeft()
    for bx, by in positions:
        p.drawEllipse(
            QRect(
                tl + QPoint(int(bx * wR), int(by * hR)),
                bulletSize,
            )
        )


def getTickInterval(
    tickInterval: int,
    singleStep: int,
    pageStep: int,
    min_: int,
    max_: int,
    sliderLength: int,
) -> int:
    """Get tick interval for a slider."""
    if tickInterval <= 0:
        tickInterval = singleStep
        posInterval = QStyle.sliderPositionFromValue(
            min_, max_, tickInterval, sliderLength
        )
        posZero = QStyle.sliderPositionFromValue(
            min_, max_, 0, sliderLength
        )
        if posInterval - posZero < 3:
            tickInterval = pageStep
    if tickInterval <= 0:
        tickInterval = 1
    return tickInterval


def getTabPath(
    rect: QRect, radiuses: RadiusesF
) -> QPainterPath:
    """Get the path for a rounded tab."""
    path = QPainterPath()
    w = float(rect.width())
    h = float(rect.height())
    x = float(rect.x())
    y = float(rect.y())

    half = min(w / 2.0, h / 2.0)
    tl = min(half, max(0.0, radiuses.topLeft * 2))
    tr = min(half, max(0.0, radiuses.topRight * 2))
    br = min(half, max(0.0, radiuses.bottomRight * 2))
    bl = min(half, max(0.0, radiuses.bottomLeft * 2))

    path.moveTo(x, y + tl)
    if tl > 0:
        path.arcTo(x, y, tl, tl, 180.0, -90.0)

    if tr > 0:
        path.lineTo(x + w - tr, y)
        path.arcTo(x + w - tr, y, tr, tr, 90.0, -90.0)
    else:
        path.lineTo(x + w, y)

    if br > 0:
        path.lineTo(x + w, y + h - br)
        path.arcTo(x + w, y + h - br, br, br, 180.0, 90.0)
    else:
        path.lineTo(x + w, y + h)

    if bl > 0:
        path.lineTo(x - bl, y + h)
        path.arcTo(x - bl, y + h - bl, bl, bl, 270.0, 90.0)
    else:
        path.lineTo(x, y + h)

    path.closeSubpath()
    return path


def drawTab(
    p: QPainter,
    rect: QRect,
    radiuses: RadiusesF,
    bgColor: QColor,
    drawShadow_: bool = False,
    shadowColor: QColor | None = None,
) -> None:
    """Draw a rounded tab."""
    if drawShadow_:
        drawTabShadow(
            p,
            rect,
            radiuses,
            shadowColor
            if shadowColor is not None
            else QColor(Qt.GlobalColor.black),
        )
    path = getTabPath(rect, radiuses)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(bgColor)
    p.drawPath(path)


def drawTabShadow(
    p: QPainter,
    rect: QRect,
    radiuses: RadiusesF,
    color: QColor,
) -> None:
    """Draw the shadow of a rounded tab."""
    from qlementine.utils._image import getDropShadowPixmap

    path = getTabPath(rect, radiuses)
    pathRect = path.boundingRect().toAlignedRect()
    pathPixmap = QPixmap(pathRect.size())
    pathPixmap.fill(Qt.GlobalColor.transparent)
    pp = QPainter(pathPixmap)
    pp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    pp.setPen(Qt.PenStyle.NoPen)
    pp.setBrush(Qt.GlobalColor.black)
    pp.drawPath(path.translated(-pathRect.x(), -pathRect.y()))
    pp.end()

    blurRadius = 4.0
    shadowX = 0
    shadowY = blurRadius / 2.0
    shadowPixmap = getDropShadowPixmap(
        pathPixmap, blurRadius, color
    )

    deltaX = (
        (shadowPixmap.width() - pathRect.width()) / 2 + shadowX
    )
    deltaY = (
        (shadowPixmap.height() - pathRect.height()) / 2
        + shadowY
        - blurRadius
    )
    shadowRect = QRect(
        QPoint(
            int(pathRect.x() - deltaX),
            int(pathRect.y() - deltaY),
        ),
        shadowPixmap.size(),
    )

    modeBackup = p.compositionMode()
    p.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_Multiply
    )
    p.drawPixmap(shadowRect, shadowPixmap)
    p.setCompositionMode(modeBackup)


def drawRadioButton(
    p: QPainter,
    rect: QRect,
    bgColor: QColor,
    borderColor: QColor,
    fgColor: QColor,
    borderWidth: float,
    progress: float,
) -> None:
    """Draw a radio button with background, border, and indicator."""
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(bgColor)
    if borderWidth > 0.1:
        hw = borderWidth / 2.0
        ellipseRect = QRectF(rect).marginsRemoved(
            QMarginsF(hw, hw, hw, hw)
        )
    else:
        ellipseRect = QRectF(rect)
    p.drawEllipse(ellipseRect)

    if borderWidth > 0.1:
        drawEllipseBorder(p, QRectF(rect), borderColor, borderWidth)

    if progress > 0.01:
        p.setBrush(fgColor)
        p.setPen(Qt.PenStyle.NoPen)
        drawRadioButtonIndicator(rect, p, progress)


def drawCheckButton(
    p: QPainter,
    rect: QRect,
    radius: float,
    bgColor: QColor,
    borderColor: QColor,
    fgColor: QColor,
    borderWidth: float,
    progress: float,
    checkState: CheckState,
) -> None:
    """Draw a check button with background, border, and indicator."""
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    if radius < 1:
        p.fillRect(rect, bgColor)
    else:
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(bgColor)
        if borderWidth > 0.1:
            hw = borderWidth / 2.0
            buttonRect = QRectF(rect).marginsRemoved(
                QMarginsF(hw, hw, hw, hw)
            )
        else:
            buttonRect = QRectF(rect)
        p.drawRoundedRect(buttonRect, radius, radius)

    if borderWidth > 0.1:
        drawRoundedRectBorder(
            p, rect, borderColor, borderWidth, radius
        )

    if progress > 0.01:
        checkThickness = 2.0
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(
            QPen(
                fgColor,
                checkThickness,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )
        if checkState == CheckState.Checked:
            drawCheckBoxIndicator(rect, p, progress)
        elif checkState == CheckState.Indeterminate:
            drawPartiallyCheckedCheckBoxIndicator(
                rect, p, progress
            )


def drawMenuSeparator(
    p: QPainter,
    rect: QRect,
    color: QColor,
    thickness: int,
) -> None:
    """Draw a menu separator."""
    x = rect.x()
    w = rect.width()
    h = max(1, thickness)
    y = rect.y() + (rect.height() - h) // 2
    p.fillRect(QRect(x, y, w, h), color)


def removeTrailingWhitespaces(text: str) -> str:
    """Remove trailing whitespace from *text*."""
    return text.rstrip()


def displayedShortcutString(shortcut: QKeySequence) -> str:
    """Get display text for a keyboard shortcut."""
    s = shortcut.toString(QKeySequence.SequenceFormat.NativeText)
    try:
        tr = QApplication.translate
        s = s.replace(tr("QShortcut", "Left"), "\u2190")
        s = s.replace(tr("QShortcut", "Right"), "\u2192")
        s = s.replace(tr("QShortcut", "Up"), "\u2191")
        s = s.replace(tr("QShortcut", "Down"), "\u2193")
    except Exception:
        pass
    return s


def shortcutSizeHint(shortcut: QKeySequence, theme: object) -> QSize:
    """Get the necessary size to display the shortcut."""
    shortcutStr = displayedShortcutString(shortcut)
    if not shortcutStr:
        return QSize(0, 0)

    radius = 3.0
    borderW = 1
    font = getattr(theme, "fontRegular", QtGui.QFont())
    fm = QFontMetrics(font)
    parts = [
        p for p in shortcutStr.split("+") if p
    ]
    spacing_val = getattr(theme, "spacing", 8)
    spacing = spacing_val // 2
    paddingV = spacing_val // 4
    paddingH = spacing_val // 2
    padding = QMargins(paddingH, paddingV, paddingH, paddingV)
    bgMargins = QMargins(
        borderW, borderW, borderW, int(borderW * radius)
    )
    minimumTextW = fm.capHeight() + 2 * borderW

    from qlementine.utils._font import textWidth

    w = 0
    h = fm.height() + paddingV * 2 + bgMargins.top() + bgMargins.bottom()

    for part in parts:
        tw = max(minimumTextW, textWidth(fm, part))
        textRect = QRect(0, 0, tw, fm.height())
        fgRect = textRect.marginsAdded(padding)
        bgRect = fgRect.marginsAdded(bgMargins)
        w += bgRect.width()

    if parts:
        w += (len(parts) - 1) * spacing

    return QSize(w, h)


def drawShortcut(
    p: QPainter,
    shortcut: QKeySequence,
    rect: QRect,
    theme: object,
    enabled: bool,
    alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft
    | Qt.AlignmentFlag.AlignVCenter,
) -> None:
    """Draw a keyboard shortcut."""
    shortcutStr = displayedShortcutString(shortcut)
    if not shortcutStr:
        return

    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    radius = 3.0
    borderW = 1
    font = getattr(theme, "fontRegular", QtGui.QFont())
    fm = QFontMetrics(font)
    parts = [s for s in shortcutStr.split("+") if s]
    spacing_val = getattr(theme, "spacing", 8)
    spacing = spacing_val // 2
    paddingV = spacing_val // 4
    paddingH = spacing_val // 2
    padding = QMargins(paddingH, paddingV, paddingH, paddingV)
    bgMargins = QMargins(
        borderW, borderW, borderW, int(borderW * radius)
    )
    minimumTextW = fm.capHeight() + 2 * borderW

    from qlementine.utils._font import textWidth

    x = 0
    for part in parts:
        tw = max(minimumTextW, textWidth(fm, part))
        textRect = QRect(0, 0, tw, fm.height())
        fgRect = textRect.marginsAdded(padding)
        bgRect = fgRect.marginsAdded(bgMargins)
        delta = textRect.topLeft() - bgRect.topLeft()

        translation = QPoint(rect.x() + x, rect.y()) + delta
        if int(alignment) & int(Qt.AlignmentFlag.AlignHCenter):
            translation.setX(
                translation.x()
                + (rect.width() - bgRect.width()) // 2
            )
        if int(alignment) & int(Qt.AlignmentFlag.AlignVCenter):
            translation.setY(
                translation.y()
                + (rect.height() - bgRect.height()) // 2
            )

        bgC = getattr(
            theme,
            "secondaryAlternativeColor"
            if enabled
            else "secondaryAlternativeColorDisabled",
            QColor(200, 200, 200),
        )
        p.setBrush(bgC)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(
            bgRect.translated(translation),
            radius + borderW,
            radius + borderW,
        )

        fgC = getattr(
            theme,
            "backgroundColorMain2"
            if enabled
            else "backgroundColorMain3",
            QColor(255, 255, 255),
        )
        p.setBrush(fgC)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(
            fgRect.translated(translation), radius, radius
        )

        textC = getattr(
            theme,
            "secondaryColor"
            if enabled
            else "secondaryColorDisabled",
            QColor(0, 0, 0),
        )
        textFlags = (
            Qt.AlignmentFlag.AlignCenter
            | Qt.TextFlag.TextSingleLine
            | Qt.TextFlag.TextHideMnemonic
        )
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(textC)
        p.drawText(
            textRect.translated(translation),
            int(textFlags),
            part,
        )

        x += bgRect.width() + spacing


def drawElidedMultiLineText(
    p: QPainter,
    rect: QRect,
    text: str,
    paintDevice: object,
) -> None:
    """Draw elided multi-line text with ellipsis."""
    fm = p.fontMetrics()
    leading = fm.leading()
    maxWidth = rect.width()
    maxHeight = rect.height()

    textLayout = QTextLayout(text, p.font(), paintDevice)
    textLayout.setCacheEnabled(True)
    height = 0.0
    lastLine = -1
    textLayout.beginLayout()
    while True:
        line = textLayout.createLine()
        if not line.isValid():
            break
        line.setLineWidth(maxWidth)
        height += leading
        line.setPosition(QPointF(0, height))
        height += line.height()
        if height <= maxHeight:
            lastLine += 1
    textLayout.endLayout()

    lineCount = textLayout.lineCount()
    for i in range(lastLine + 1):
        line = textLayout.lineAt(i)
        lineRect = QRect(
            rect.topLeft() + line.position().toPoint(),
            QSize(maxWidth, int(line.height())),
        )
        if (
            i < lastLine or lastLine == lineCount - 1
        ) and line.naturalTextWidth() < maxWidth:
            line.draw(p, rect.topLeft())
        else:
            lineText = removeTrailingWhitespaces(
                textLayout.text()[
                    line.textStart() : line.textStart()
                    + line.textLength()
                ]
            )
            ellipsis = "\u2026"

            from qlementine.utils._font import textWidth

            ellipsisWidth = textWidth(fm, ellipsis)
            elidedText = removeTrailingWhitespaces(
                fm.elidedText(
                    lineText,
                    Qt.TextElideMode.ElideRight,
                    maxWidth - ellipsisWidth,
                    Qt.TextFlag.TextSingleLine,
                )
            )
            if not elidedText.endswith(ellipsis):
                elidedText = (
                    removeTrailingWhitespaces(elidedText)
                    + ellipsis
                )
            textFlags = (
                Qt.AlignmentFlag.AlignLeft
                | Qt.TextFlag.TextSingleLine
            )
            p.drawText(lineRect, int(textFlags), elidedText)


def makeCheckPixmap(size: QSize, color: QColor) -> QPixmap:
    """Generate a pixmap with a check mark."""
    checkRect = QRect(0, 0, size.width(), size.height())
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    defaultSize = 16.0
    defaultPenWidth = 2.0
    penWidth = (size.width() / defaultSize) * defaultPenWidth

    p = QPainter(pixmap)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(
        QPen(
            color,
            penWidth,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
    )
    drawCheckBoxIndicator(checkRect, p, 1.0)
    p.end()
    return pixmap


def makeArrowLeftPixmap(size: QSize, color: QColor) -> QPixmap:
    """Generate a pixmap with a left arrow."""
    rect = QRect(0, 0, size.width(), size.height())
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    penWidth = (size.width() / 16.0) * 1.01

    p = QPainter(pixmap)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(
        QPen(
            color,
            penWidth,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
    )
    drawArrowLeft(rect, p)
    p.end()
    return pixmap


def makeArrowRightPixmap(size: QSize, color: QColor) -> QPixmap:
    """Generate a pixmap with a right arrow."""
    rect = QRect(0, 0, size.width(), size.height())
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    penWidth = (size.width() / 16.0) * 1.01

    p = QPainter(pixmap)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(
        QPen(
            color,
            penWidth,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
    )
    drawArrowRight(rect, p)
    p.end()
    return pixmap


def makeMessageBoxWarningPixmap(
    size: QSize, bgColor: QColor, fgColor: QColor
) -> QPixmap:
    """Generate a warning message box pixmap."""
    from qlementine.utils._image import makePixmapFromSvg

    bgSvg = ":/qlementine/resources/icons/messagebox_warning_bg.svg"
    fgSvg = ":/qlementine/resources/icons/messagebox_warning_fg.svg"
    return makePixmapFromSvg(bgSvg, bgColor, fgSvg, fgColor, size)


def makeMessageBoxCriticalPixmap(
    size: QSize, bgColor: QColor, fgColor: QColor
) -> QPixmap:
    """Generate a critical message box pixmap."""
    from qlementine.utils._image import makePixmapFromSvg

    bgSvg = ":/qlementine/resources/icons/messagebox_critical_bg.svg"
    fgSvg = ":/qlementine/resources/icons/messagebox_critical_fg.svg"
    return makePixmapFromSvg(bgSvg, bgColor, fgSvg, fgColor, size)


def makeMessageBoxQuestionPixmap(
    size: QSize, bgColor: QColor, fgColor: QColor
) -> QPixmap:
    """Generate a question message box pixmap."""
    from qlementine.utils._image import makePixmapFromSvg

    bgSvg = ":/qlementine/resources/icons/messagebox_question_bg.svg"
    fgSvg = ":/qlementine/resources/icons/messagebox_question_fg.svg"
    return makePixmapFromSvg(bgSvg, bgColor, fgSvg, fgColor, size)


def makeMessageBoxInformationPixmap(
    size: QSize, bgColor: QColor, fgColor: QColor
) -> QPixmap:
    """Generate an information message box pixmap."""
    from qlementine.utils._image import makePixmapFromSvg

    bgSvg = ":/qlementine/resources/icons/messagebox_information_bg.svg"
    fgSvg = ":/qlementine/resources/icons/messagebox_information_fg.svg"
    return makePixmapFromSvg(bgSvg, bgColor, fgSvg, fgColor, size)


def drawIcon(
    rect: QRect,
    p: QPainter,
    icon: QIcon,
    mouse: MouseState,
    checked: CheckState,
    widget: QWidget | None,
    colorize: bool = False,
    color: QColor | None = None,
) -> QRect:
    """Draw an icon centered in *rect*. Returns the actual drawn rect."""
    if rect.isEmpty() or icon.isNull():
        return QRect(rect.x(), rect.y(), 0, 0)

    from qlementine.utils._state import getIconMode, getIconState
    from qlementine.utils._image import getColorizedPixmap

    iconSize = rect.size()
    iconMode = getIconMode(mouse)
    iconState = getIconState(checked)

    dpr = (
        widget.devicePixelRatio()
        if widget
        else QApplication.instance().devicePixelRatio()
    )
    pixmap = icon.pixmap(iconSize, dpr, iconMode, iconState)
    if colorize and color is not None:
        pixmap = getColorizedPixmap(pixmap, color)

    if pixmap.isNull():
        return QRect(rect.x(), rect.y(), 0, 0)

    pr = pixmap.devicePixelRatio()
    tw = int(pixmap.width() / pr) if pr else 0
    th = int(pixmap.height() / pr) if pr else 0
    tx = rect.x() + (rect.width() - tw) // 2
    ty = rect.y() + (rect.height() - th) // 2
    targetRect = QRect(tx, ty, tw, th)

    p.drawPixmap(targetRect, pixmap)
    return targetRect


def getMenuLabelAndShortcut(text: str) -> tuple[str, str]:
    """Split menu text into (label, shortcut) on tab character."""
    parts = text.split("\t", 1)
    label = parts[0] if parts else ""
    shortcut = parts[1] if len(parts) > 1 else ""
    return label, shortcut


def drawSubMenuIndicator(rect: QRect, p: QPainter) -> None:
    """Draw a right-pointing sub-menu arrow indicator."""
    w = rect.width()
    h = rect.width()
    x = rect.x()
    y = rect.y()
    s = 16.0
    p1 = QPointF(10.5 / s * w + x, 4.5 / s * h + y)
    p2 = QPointF(14.0 / s * w + x, 8.0 / s * h + y)
    p3 = QPointF(10.5 / s * w + x, 11.5 / s * h + y)
    path = QPainterPath()
    path.moveTo(p1)
    path.lineTo(p2)
    path.lineTo(p3)
    p.drawPath(path)


def drawSpinBoxArrowIndicator(
    rect: QRect,
    p: QPainter,
    buttonSymbol: int,
    subControl: int,
    iconSize: QSize,
) -> None:
    """Draw a spinbox up/down arrow or +/- indicator."""
    NoButtons = 2  # QAbstractSpinBox::NoButtons
    PlusMinus = 1  # QAbstractSpinBox::PlusMinus
    SC_SpinBoxUp = QStyle.SubControl.SC_SpinBoxUp
    SC_SpinBoxDown = QStyle.SubControl.SC_SpinBoxDown

    if buttonSymbol == NoButtons:
        return

    iw = min(rect.width(), iconSize.width())
    ih = min(rect.height(), iconSize.height())
    ix = rect.x() + (rect.width() - iw) // 2
    iy = rect.y() + (rect.height() - ih) // 2

    x, y, w, h = ix, iy, iw, ih

    if buttonSymbol == PlusMinus:
        if subControl == SC_SpinBoxUp:
            p.drawLine(
                QPointF(x + w / 2, y), QPointF(x + w / 2, y + h)
            )
            p.drawLine(
                QPointF(x, y + h / 2), QPointF(x + w, y + h / 2)
            )
        elif subControl == SC_SpinBoxDown:
            p.drawLine(
                QPointF(x, y + h / 2), QPointF(x + w, y + h / 2)
            )
    else:  # UpDownArrows
        s = 8.0
        if subControl == SC_SpinBoxUp:
            p1 = QPointF(1.0 / s * w + x, 5.0 / s * h + y)
            p2 = QPointF(4.0 / s * w + x, 2.0 / s * h + y)
            p3 = QPointF(7.0 / s * w + x, 5.0 / s * h + y)
            path = QPainterPath()
            path.moveTo(p1)
            path.lineTo(p2)
            path.lineTo(p3)
            p.drawPath(path)
        elif subControl == SC_SpinBoxDown:
            p1 = QPointF(1.0 / s * w + x, 3.0 / s * h + y)
            p2 = QPointF(4.0 / s * w + x, 6.0 / s * h + y)
            p3 = QPointF(7.0 / s * w + x, 3.0 / s * h + y)
            path = QPainterPath()
            path.moveTo(p1)
            path.lineTo(p2)
            path.lineTo(p3)
            p.drawPath(path)


def drawSliderTickMarks(
    p: QPainter,
    tickmarksRect: QRect,
    tickColor: QColor,
    min_val: int,
    max_val: int,
    interval: int,
    tickThickness: int,
    singleStep: int,
    pageStep: int,
) -> None:
    """Draw tick marks for a slider."""
    sliderLength = tickmarksRect.width()
    tickInterval = getTickInterval(
        interval, singleStep, pageStep, min_val, max_val, sliderLength
    )
    if tickInterval <= 0:
        return

    p.setPen(QPen(tickColor, tickThickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap))
    p.setBrush(Qt.BrushStyle.NoBrush)

    y1 = tickmarksRect.top()
    y2 = tickmarksRect.bottom() + 1

    v = min_val
    while v <= max_val:
        x1 = min(
            tickmarksRect.right(),
            tickmarksRect.left()
            + QStyle.sliderPositionFromValue(min_val, max_val, v, sliderLength),
        )
        p.drawLine(x1, y1, x1, y2)
        v += tickInterval


def drawDialTickMarks(
    p: QPainter,
    tickmarksRect: QRect,
    tickColor: QColor,
    min_val: int,
    max_val: int,
    tickThickness: int,
    tickLength: int,
    singleStep: int,
    pageStep: int,
    minArcLength: int,
) -> None:
    """Draw tick marks for a dial."""
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(QPen(tickColor, tickThickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap))
    p.setBrush(Qt.BrushStyle.NoBrush)

    centerX = tickmarksRect.x() + tickmarksRect.width() / 2
    centerY = tickmarksRect.y() + tickmarksRect.height() / 2
    r1 = tickmarksRect.width() / 2
    r2 = r1 - tickLength

    PI_4 = _PI_4
    anglePerStep = 6.0 * PI_4 / (max_val - min_val) if max_val != min_val else 0.0
    arcPerStep = anglePerStep * r1
    tickInterval = singleStep if arcPerStep > minArcLength else pageStep
    if tickInterval <= 0:
        return

    v = float(min_val)
    while v <= max_val:
        ratio = (v - min_val) / (max_val - min_val) if max_val != min_val else 0
        angle = (ratio - 1.0) * 6.0 * PI_4 + PI_4
        cosA = math.cos(angle)
        sinA = math.sin(angle)

        x1 = centerX + r1 * cosA
        y1 = centerY + r1 * sinA
        x2 = centerX + r2 * cosA
        y2 = centerY + r2 * sinA
        p.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        v += tickInterval


def drawDial(
    p: QPainter,
    dialRect: QRect,
    min_val: int,
    max_val: int,
    value: float,
    bgColor: QColor,
    handleColor: QColor,
    grooveColor: QColor,
    valueColor: QColor,
    markColor: QColor,
    grooveThickness: int,
    markLength: int,
    markThickness: int,
) -> None:
    """Draw a dial (circular knob) widget."""
    angleSpreadDegrees = 270
    startAngleDegrees = 225
    qtAnglePrecision = 16
    angleSpreadRadians = 6.0 * _PI_4
    startAngleRadians = _PI_4

    # Background
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(bgColor)
    p.drawEllipse(dialRect)

    # Value arc
    halfGT = grooveThickness / 2.0
    arcRect = QRectF(dialRect).marginsRemoved(
        QMarginsF(halfGT, halfGT, halfGT, halfGT)
    )
    startAngle = startAngleDegrees * qtAnglePrecision
    ratio = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.0
    angleLength = -(angleSpreadDegrees * ratio) * qtAnglePrecision

    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(valueColor, grooveThickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    p.drawArc(arcRect, startAngle, int(angleLength))

    # Pie overlay below
    if value > min_val:
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(valueColor)
        circlePerimeter = QLEMENTINE_PI * dialRect.width()
        cropLength = (halfGT / circlePerimeter) * 90 if circlePerimeter else 0
        shiftAngle = cropLength * qtAnglePrecision
        p.drawPie(dialRect, startAngle, int(angleLength + shiftAngle))

    # Dead zone pie
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(bgColor)
    p.drawPie(dialRect, startAngle, 90 * qtAnglePrecision)

    # Front circle
    gt = grooveThickness
    dialFrontRect = dialRect.adjusted(gt, gt, -gt, -gt)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(handleColor)
    p.drawEllipse(dialFrontRect)

    # Mark line
    markRect = QRectF(dialFrontRect)
    markAngle = startAngleRadians + (ratio - 1.0) * angleSpreadRadians
    cosA = math.cos(markAngle)
    sinA = math.sin(markAngle)
    p1Radius = (markRect.width() - 2.0) / 2.0
    p2Radius = p1Radius - markLength
    center = markRect.center()
    pt1 = QPointF(p1Radius * cosA + center.x(), p1Radius * sinA + center.y())
    pt2 = QPointF(p2Radius * cosA + center.x(), p2Radius * sinA + center.y())
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(markColor, markThickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap))
    p.drawLine(pt1, pt2)


def getPixmap(
    icon: QIcon,
    iconSize: QSize,
    mouse: MouseState,
    checked: CheckState,
    widget: QWidget | None = None,
) -> QPixmap:
    """Get a cached pixmap from an icon for the given state."""
    from qlementine.utils._state import getIconMode, getIconState

    iconMode = getIconMode(mouse)
    iconState = getIconState(checked)
    app = QApplication.instance()
    dpr = widget.devicePixelRatio() if widget else (app.devicePixelRatio() if app else 1.0)

    cacheKey = (
        f"qlementine_icon_pixmap_{icon.cacheKey()}"
        f"_{iconSize.width()}_{iconSize.height()}"
        f"_{dpr}_{int(iconMode)}_{int(iconState)}"
    )
    result = QPixmapCache.find(cacheKey)
    if result is not None:
        if isinstance(result, tuple):
            ok, pm = result
            if ok:
                return pm
        else:
            return result

    pixmap = icon.pixmap(iconSize, dpr, iconMode, iconState)
    QPixmapCache.insert(cacheKey, pixmap)
    return pixmap
