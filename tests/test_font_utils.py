"""Tests for FontUtils free functions."""

from __future__ import annotations

from _qt_compat import Qlementine, QtGui


def test_point_size_to_pixel_size(qapp):
    result = Qlementine.pointSizeToPixelSize(12.0, 96.0)
    assert isinstance(result, float)
    assert result > 0


def test_pixel_size_to_point_size(qapp):
    result = Qlementine.pixelSizeToPointSize(16.0, 96.0)
    assert isinstance(result, float)
    assert result > 0


def test_roundtrip_size_conversion(qapp):
    dpi = 96.0
    original = 12.0
    pixels = Qlementine.pointSizeToPixelSize(original, dpi)
    points = Qlementine.pixelSizeToPointSize(pixels, dpi)
    assert abs(points - original) < 0.01


def test_text_width(qapp):
    font = QtGui.QFont("Arial", 12)
    fm = QtGui.QFontMetrics(font)
    width = Qlementine.textWidth(fm, "Hello World")
    assert isinstance(width, int)
    assert width > 0
