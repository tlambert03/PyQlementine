"""Image utility functions."""

from __future__ import annotations

import math

from qlementine._qt import QtCore, QtGui
from qlementine._enums import ColorizeMode
from qlementine._radiuses import RadiusesF

QColor = QtGui.QColor
QImage = QtGui.QImage
QPainter = QtGui.QPainter
QPixmap = QtGui.QPixmap
QPixmapCache = QtGui.QPixmapCache
QSize = QtCore.QSize
QPoint = QtCore.QPoint
QRect = QtCore.QRect
QRectF = QtCore.QRectF
Qt = QtCore.Qt

# blur sigma conversion factor matching C++ pixelToSigma
pixelToSigma = 2.5

__all__ = [
    "blurRadiusNecessarySpace",
    "colorizeImage",
    "colorizePixmap",
    "getBlurredImage",
    "getBlurredPixmap",
    "getCachedPixmap",
    "getColorizedPixmap",
    "getColorizedPixmapKey",
    "getDropShadowPixmap",
    "getExtendedImage",
    "getImageAspectRatio",
    "getTintedPixmap",
    "getTintedPixmapKey",
    "makeFitPixmap",
    "makePixmapFromSvg",
    "makeRoundedPixmap",
    "tintPixmap",
]


def colorizeImage(
    pixmap: QPixmap, color: QColor
) -> QImage:
    """Colorize a QPixmap, returning a QImage."""
    if pixmap.isNull():
        return QImage()

    image_size = pixmap.size()
    input_image = pixmap.toImage().convertToFormat(
        QImage.Format.Format_ARGB32
    )
    output_image = QImage(image_size, input_image.format())

    out_rgba = color.rgba()
    out_r = (out_rgba >> 16) & 0xFF
    out_g = (out_rgba >> 8) & 0xFF
    out_b = out_rgba & 0xFF
    out_af = ((out_rgba >> 24) & 0xFF) / 255.0

    for x in range(image_size.width()):
        for y in range(image_size.height()):
            px = input_image.pixel(x, y)
            in_a = (px >> 24) & 0xFF
            new_a = int(in_a * out_af)
            new_pixel = (
                (new_a << 24) | (out_r << 16) | (out_g << 8) | out_b
            )
            output_image.setPixel(x, y, new_pixel)

    output_image.setDevicePixelRatio(
        input_image.devicePixelRatioF()
    )
    return output_image


def colorizePixmap(pixmap: QPixmap, color: QColor) -> QPixmap:
    """Colorize a QPixmap."""
    return QPixmap.fromImage(colorizeImage(pixmap, color))


def _grayscale(image: QImage) -> QImage:
    """Convert image to grayscale preserving alpha."""
    result = QImage(image.size(), image.format())
    result.setDevicePixelRatio(image.devicePixelRatioF())
    for x in range(image.width()):
        for y in range(image.height()):
            px = image.pixel(x, y)
            a = (px >> 24) & 0xFF
            r = (px >> 16) & 0xFF
            g = (px >> 8) & 0xFF
            b = px & 0xFF
            gray = (r * 11 + g * 16 + b * 5) // 32
            result.setPixel(
                x, y, (a << 24) | (gray << 16) | (gray << 8) | gray
            )
    return result


def tintPixmap(pixmap: QPixmap, color: QColor) -> QPixmap:
    """Tint a QPixmap, preserving contrast between shades."""
    if pixmap.isNull():
        return QPixmap()

    input_image = pixmap.toImage()
    has_alpha = input_image.hasAlphaChannel()
    fmt = (
        QImage.Format.Format_ARGB32_Premultiplied
        if has_alpha
        else QImage.Format.Format_RGB32
    )
    input_image = input_image.convertToFormat(fmt)

    output_image = QImage(input_image.size(), input_image.format())
    output_image.setDevicePixelRatio(
        input_image.devicePixelRatioF()
    )

    # Grayscale then screen-composite with color
    gray = _grayscale(input_image)
    painter = QPainter(output_image)
    painter.drawImage(0, 0, gray)
    painter.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_Screen
    )
    painter.fillRect(input_image.rect(), color)
    painter.end()

    if has_alpha:
        mask_painter = QPainter(output_image)
        mask_painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_DestinationIn
        )
        mask_painter.drawImage(0, 0, input_image)
        mask_painter.end()

    return QPixmap.fromImage(output_image)


def _toHex(value: int) -> str:
    """Convert integer to hex string."""
    return f"{value:016x}"


def getColorizedPixmapKey(
    pixmap: QPixmap, color: QColor
) -> str:
    """Get cache key for a colorized pixmap."""
    return f"qlementine_color_{_toHex(pixmap.cacheKey())}_{_toHex(color.rgba())}"


def getTintedPixmapKey(
    pixmap: QPixmap, color: QColor
) -> str:
    """Get cache key for a tinted pixmap."""
    return f"qlementine_tint_{_toHex(pixmap.cacheKey())}_{_toHex(color.rgba())}"


def getCachedPixmap(
    pixmap: QPixmap,
    color: QColor,
    mode: ColorizeMode,
) -> QPixmap:
    """Get or create a cached colorized/tinted pixmap."""
    if pixmap.isNull():
        return pixmap

    tint = mode == ColorizeMode.Tint
    key = (
        getTintedPixmapKey(pixmap, color)
        if tint
        else getColorizedPixmapKey(pixmap, color)
    )

    cached = QPixmapCache.find(key)
    if cached is not None and not cached.isNull():
        return cached

    new_pixmap = (
        tintPixmap(pixmap, color)
        if tint
        else colorizePixmap(pixmap, color)
    )
    QPixmapCache.insert(key, new_pixmap)
    found = QPixmapCache.find(key)
    if found is not None and not found.isNull():
        return found
    return pixmap


def getColorizedPixmap(
    pixmap: QPixmap, color: QColor
) -> QPixmap:
    """Get a colorized version of the pixmap (cached)."""
    return getCachedPixmap(pixmap, color, ColorizeMode.Colorize)


def getTintedPixmap(
    pixmap: QPixmap, color: QColor
) -> QPixmap:
    """Get a tinted version of the pixmap (cached)."""
    return getCachedPixmap(pixmap, color, ColorizeMode.Tint)


def makePixmapFromSvg(
    svgPathOrBg: str,
    sizeOrBgColor: QSize | QColor,
    fgPathOrNone: str | None = None,
    fgColor: QColor | None = None,
    size: QSize | None = None,
) -> QPixmap:
    """Make a QPixmap from SVG file(s)."""
    try:
        from PySide6.QtSvg import QSvgRenderer
    except ImportError:
        from PyQt6.QtSvg import QSvgRenderer  # type: ignore

    if fgPathOrNone is not None:
        # Two-SVG composite variant
        bgPath = svgPathOrBg
        bgColor = sizeOrBgColor
        fgPath = fgPathOrNone
        assert fgColor is not None
        assert size is not None
        bgPixmap = _renderSvg(bgPath, size, QSvgRenderer)
        fgPixmap = _renderSvg(fgPath, size, QSvgRenderer)
        coloredBg = colorizePixmap(bgPixmap, bgColor)
        coloredFg = colorizePixmap(fgPixmap, fgColor)
        result = QPixmap(size)
        result.fill(Qt.GlobalColor.transparent)
        p = QPainter(result)
        p.drawPixmap(0, 0, coloredBg)
        p.drawPixmap(0, 0, coloredFg)
        p.end()
        return result

    # Single-SVG variant
    svgPath = svgPathOrBg
    actual_size = sizeOrBgColor
    if not svgPath:
        return QPixmap()
    return _renderSvg(svgPath, actual_size, QSvgRenderer)


def _renderSvg(
    svgPath: str, size: QSize, QSvgRenderer: type
) -> QPixmap:
    """Render an SVG to a QPixmap."""
    renderer = QSvgRenderer(svgPath)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(
        QPainter.RenderHint.Antialiasing, True
    )
    renderer.render(painter, QRectF(pixmap.rect()))
    painter.end()
    return pixmap


def makeRoundedPixmap(
    pixmap: QPixmap,
    radius_or_radiuses: float | RadiusesF,
    topRight: float | None = None,
    bottomRight: float | None = None,
    bottomLeft: float | None = None,
) -> QPixmap:
    """Make a QPixmap with rounded corners."""
    if pixmap.isNull():
        return QPixmap()

    if isinstance(radius_or_radiuses, RadiusesF):
        radiuses = radius_or_radiuses
    elif topRight is not None:
        radiuses = RadiusesF(
            radius_or_radiuses,
            topRight,
            bottomRight if bottomRight is not None else 0.0,
            bottomLeft if bottomLeft is not None else 0.0,
        )
    else:
        radiuses = RadiusesF(radius_or_radiuses)

    from qlementine.utils._primitive import drawRoundedRect

    result = QPixmap(pixmap.size())
    result.fill(Qt.GlobalColor.transparent)

    p = QPainter(result)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    brush = QtGui.QBrush(Qt.GlobalColor.white)
    drawRoundedRect(
        p,
        result.rect(),
        brush,
        radiuses,
    )
    p.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_SourceIn
    )
    p.drawPixmap(result.rect(), pixmap)
    p.end()

    result.setDevicePixelRatio(pixmap.devicePixelRatio())
    return result


def makeFitPixmap(pixmap: QPixmap, size: QSize) -> QPixmap:
    """Make a pixmap that fits the requested size."""
    if pixmap.isNull():
        return QPixmap()

    result = QPixmap(size)
    result.fill(Qt.GlobalColor.transparent)

    scaled = pixmap.scaled(
        size,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation,
    )
    x = (result.width() - scaled.width()) // 2
    y = (result.height() - scaled.height()) // 2

    p = QPainter(result)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.drawPixmap(int(x), int(y), scaled)
    p.end()
    return result


def getImageAspectRatio(path: str) -> float:
    """Get aspect ratio of image without loading it fully."""
    if not path:
        return 1.0
    reader = QtGui.QImageReader(path)
    size = reader.size()
    if size.height() == 0:
        return 1.0
    return size.width() / float(size.height())


def getExtendedImage(
    input_: QPixmap | QImage, padding: int
) -> QImage:
    """Get a version of the image with transparent padding."""
    if isinstance(input_, QPixmap):
        if input_.isNull():
            return QImage()
        return getExtendedImage(input_.toImage(), padding)

    if input_.isNull():
        return QImage()

    pxRatio = input_.devicePixelRatioF()
    actualPadding = int(
        math.ceil(max(padding, 0) * pxRatio)
    )
    actualExtension = 2 * actualPadding
    actualSize = input_.size()
    extendedSize = QSize(
        actualSize.width() + actualExtension,
        actualSize.height() + actualExtension,
    )

    result = QImage(
        extendedSize,
        QImage.Format.Format_ARGB32_Premultiplied,
    )
    result.fill(Qt.GlobalColor.transparent)

    # Copy pixels from input
    inp = input_.convertToFormat(
        QImage.Format.Format_ARGB32_Premultiplied
    )
    p = QPainter(result)
    p.drawImage(actualPadding, actualPadding, inp)
    p.end()

    result.setDevicePixelRatio(pxRatio)
    return result


def _fast_gaussian_blur(image: QImage, sigma: float) -> QImage:
    """Simple box-blur approximation of Gaussian blur."""
    if sigma < 0.5:
        return image

    # Use Qt's built-in blur via QGraphicsBlurEffect approach:
    # Draw to a scene and apply blur. Simpler approach: iterative
    # box blur.
    radius = max(1, int(round(sigma * 3)))
    w, h = image.width(), image.height()
    src = image.convertToFormat(
        QImage.Format.Format_ARGB32
    )
    dst = QImage(src.size(), src.format())

    # Horizontal pass
    for y in range(h):
        for x in range(w):
            r_sum = g_sum = b_sum = a_sum = 0
            count = 0
            for dx in range(-radius, radius + 1):
                nx = max(0, min(w - 1, x + dx))
                px = src.pixel(nx, y)
                a_sum += (px >> 24) & 0xFF
                r_sum += (px >> 16) & 0xFF
                g_sum += (px >> 8) & 0xFF
                b_sum += px & 0xFF
                count += 1
            dst.setPixel(
                x,
                y,
                (
                    ((a_sum // count) << 24)
                    | ((r_sum // count) << 16)
                    | ((g_sum // count) << 8)
                    | (b_sum // count)
                ),
            )

    # Vertical pass
    result = QImage(dst.size(), dst.format())
    for x in range(w):
        for y in range(h):
            r_sum = g_sum = b_sum = a_sum = 0
            count = 0
            for dy in range(-radius, radius + 1):
                ny = max(0, min(h - 1, y + dy))
                px = dst.pixel(x, ny)
                a_sum += (px >> 24) & 0xFF
                r_sum += (px >> 16) & 0xFF
                g_sum += (px >> 8) & 0xFF
                b_sum += px & 0xFF
                count += 1
            result.setPixel(
                x,
                y,
                (
                    ((a_sum // count) << 24)
                    | ((r_sum // count) << 16)
                    | ((g_sum // count) << 8)
                    | (b_sum // count)
                ),
            )

    result.setDevicePixelRatio(image.devicePixelRatioF())
    return result


def getBlurredImage(
    inputImage: QImage, blurRadius: float
) -> QImage:
    """Get a blurred version of the image."""
    if inputImage.isNull():
        return QImage()
    sigma = (
        blurRadius * inputImage.devicePixelRatioF() / pixelToSigma
    )
    return _fast_gaussian_blur(inputImage, sigma)


def getBlurredPixmap(
    pixmap: QPixmap, blurRadius: float
) -> QPixmap:
    """Get a blurred version of the pixmap."""
    if pixmap.isNull():
        return QPixmap()
    return QPixmap.fromImage(
        getBlurredImage(pixmap.toImage(), blurRadius)
    )


def getDropShadowPixmap(
    input_or_size: QPixmap | QSize,
    blurRadiusOrBorderRadius: float,
    colorOrBlurRadius: QColor | float | None = None,
    color: QColor | None = None,
) -> QPixmap:
    """Get a drop shadow pixmap."""
    if isinstance(input_or_size, QSize):
        # (size, borderRadius, blurRadius, color?)
        size = input_or_size
        borderRadius = blurRadiusOrBorderRadius
        blurRadius = float(colorOrBlurRadius)
        shadowColor = color if color is not None else QColor(
            Qt.GlobalColor.black
        )

        if size.isEmpty():
            return QPixmap()

        from qlementine.utils._primitive import drawRoundedRect

        colorizedImage = QPixmap(size)
        colorizedImage.fill(Qt.GlobalColor.transparent)
        p = QPainter(colorizedImage)
        drawRoundedRect(
            p,
            QRect(QPoint(0, 0), size),
            QtGui.QBrush(shadowColor),
            borderRadius,
        )
        p.end()

        padding = blurRadiusNecessarySpace(blurRadius) * 2
        extendedImage = getExtendedImage(colorizedImage, padding)
        shadowImage = getBlurredImage(extendedImage, blurRadius)
        output = QPixmap.fromImage(shadowImage)
        output.setDevicePixelRatio(
            colorizedImage.devicePixelRatioF()
        )
        return output

    # (pixmap, blurRadius, color?)
    pixmap = input_or_size
    blurRadius = blurRadiusOrBorderRadius
    shadowColor = (
        colorOrBlurRadius
        if isinstance(colorOrBlurRadius, QColor)
        else QColor(Qt.GlobalColor.black)
    )

    if pixmap.isNull():
        return QPixmap()

    if blurRadius * pixmap.devicePixelRatioF() < 0.5:
        result = QPixmap(pixmap.size())
        result.fill(Qt.GlobalColor.transparent)
        result.setDevicePixelRatio(pixmap.devicePixelRatioF())
        return result

    colorizedImg = colorizeImage(pixmap, shadowColor)
    padding = blurRadiusNecessarySpace(blurRadius)
    extendedImg = getExtendedImage(colorizedImg, padding)
    shadowImg = getBlurredImage(extendedImg, blurRadius)
    output = QPixmap.fromImage(shadowImg)
    output.setDevicePixelRatio(pixmap.devicePixelRatioF())
    return output


def blurRadiusNecessarySpace(blurRadius: float) -> int:
    """Calculate the necessary padding for a blur."""
    return int(math.ceil(blurRadius))
