"""Color utility functions."""

from __future__ import annotations

import re

from qlementine._qt import QtGui

QColor = QtGui.QColor

__all__ = [
    "colorWithAlpha",
    "colorWithAlphaF",
    "getColorSourceOver",
    "getContrastRatio",
    "toHexRGB",
    "toHexRGBA",
    "tryGetColorFromVariant",
]


def colorWithAlphaF(color: QColor, alpha: float) -> QColor:
    """Return a copy of *color* with the given float alpha (0.0-1.0)."""
    alpha = min(1.0, max(0.0, alpha))
    result = QColor(color)
    result.setAlphaF(alpha)
    return result


def colorWithAlpha(color: QColor, alpha: int) -> QColor:
    """Return a copy of *color* with the given int alpha (0-255)."""
    alpha = min(255, max(0, alpha))
    result = QColor(color)
    result.setAlpha(alpha)
    return result


def getColorSourceOver(background: QColor, foreground: QColor) -> QColor:
    """Alpha-composite *foreground* over *background* (SourceOver)."""
    bg_a = background.alphaF()
    bg_r = background.redF() * bg_a
    bg_g = background.greenF() * bg_a
    bg_b = background.blueF() * bg_a

    fg_a = foreground.alphaF()
    fg_r = foreground.redF() * fg_a
    fg_g = foreground.greenF() * fg_a
    fg_b = foreground.blueF() * fg_a
    fg_a_inv = 1.0 - fg_a

    final_a = bg_a + fg_a - bg_a * fg_a
    final_r = fg_r + bg_r * fg_a_inv
    final_g = fg_g + bg_g * fg_a_inv
    final_b = fg_b + bg_b * fg_a_inv

    return QColor.fromRgba(
        _qRgba(
            int(final_r * 255),
            int(final_g * 255),
            int(final_b * 255),
            int(final_a * 255),
        )
    )


def _qRgba(r: int, g: int, b: int, a: int) -> int:
    """Mimic qRgba(): pack ARGB into a 32-bit unsigned int."""
    return ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)


def toHexRGB(color: QColor) -> str:
    """Return ``#rrggbb`` hex string."""
    return f"#{color.red():02x}{color.green():02x}{color.blue():02x}"


def toHexRGBA(color: QColor) -> str:
    """Return ``#rrggbbaa`` hex string."""
    return (
        f"#{color.red():02x}{color.green():02x}"
        f"{color.blue():02x}{color.alpha():02x}"
    )


def getContrastRatio(color1: QColor, color2: QColor) -> float:
    """Contrast ratio stub (upstream returns 4.5)."""
    return 4.5


# ---------------------------------------------------------------------------
# tryGetColorFromVariant and helpers
# ---------------------------------------------------------------------------

_RGB_RE = re.compile(
    r"^\s*rgb\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,"
    r"\s*(\d{1,3})\s*\)\s*$",
    re.IGNORECASE,
)
_RGBA_RE = re.compile(
    r"^\s*rgba\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,"
    r"\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)\s*$",
    re.IGNORECASE,
)


def _tryGetColorFromVariantList(variant_list: list) -> QColor | None:
    n = len(variant_list)
    if n not in (3, 4):
        return None
    try:
        r, g, b = int(variant_list[0]), int(variant_list[1]), int(variant_list[2])
    except (TypeError, ValueError):
        return None
    a = 255
    if n == 4:
        try:
            a = int(variant_list[3])
        except (TypeError, ValueError):
            pass
    return QColor(r, g, b, a)


def _tryGetColorFromHexaString(s: str) -> QColor | None:
    s = s.strip()
    if not s.startswith("#"):
        return None
    length = len(s)
    if length not in (7, 9):  # #RRGGBB or #RRGGBBAA
        return None
    try:
        r = int(s[1:3], 16)
        g = int(s[3:5], 16)
        b = int(s[5:7], 16)
    except ValueError:
        return None
    color = QColor(r, g, b)
    if length == 9:
        try:
            a = int(s[7:9], 16)
            color.setAlpha(a)
        except ValueError:
            pass
    return color


def _tryGetColorFromRGBAString(s: str) -> QColor | None:
    m = _RGB_RE.match(s)
    if m:
        return QColor(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = _RGBA_RE.match(s)
    if m:
        return QColor(
            int(m.group(1)), int(m.group(2)),
            int(m.group(3)), int(m.group(4)),
        )
    return None


def tryGetColorFromVariant(variant: object) -> QColor | None:
    """Parse a value (list or string) into a QColor, or return None."""
    if isinstance(variant, list):
        return _tryGetColorFromVariantList(variant)
    if isinstance(variant, str):
        result = _tryGetColorFromHexaString(variant)
        if result is not None:
            return result
        return _tryGetColorFromRGBAString(variant)
    return None
