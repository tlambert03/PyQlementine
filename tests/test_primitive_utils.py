"""Tests for PrimitiveUtils free functions."""

from __future__ import annotations

from _qt_compat import QColor, Qlementine, QSize, Qt, QtCore, QtGui, QWidget

CheckState = Qlementine.CheckState
MouseState = Qlementine.MouseState
RadiusesF = Qlementine.RadiusesF
Theme = Qlementine.Theme


def _make_painter():
    """Create a pixmap and painter for drawing tests."""
    pixmap = QtGui.QPixmap(100, 100)
    pixmap.fill(QColor(255, 255, 255))
    painter = QtGui.QPainter(pixmap)
    return pixmap, painter


def test_get_pixel_ratio(qapp):
    w = QWidget()
    ratio = Qlementine.getPixelRatio(w)
    assert isinstance(ratio, float)
    assert ratio > 0


def test_draw_ellipse_border(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawEllipseBorder(
        painter, QtCore.QRectF(10, 10, 80, 80), QColor(255, 0, 0), 2.0
    )
    painter.end()


def test_get_multiple_radiuses_rect_path(qapp):
    path = Qlementine.getMultipleRadiusesRectPath(
        QtCore.QRectF(0, 0, 100, 100), RadiusesF(5.0, 10.0, 15.0, 20.0)
    )
    assert isinstance(path, QtGui.QPainterPath)


def test_draw_rounded_rect_qrectf(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRoundedRect(
        painter, QtCore.QRectF(10, 10, 80, 80), QtGui.QBrush(QColor(0, 0, 255)), 5.0
    )
    painter.end()


def test_draw_rounded_rect_qrect(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRoundedRect(
        painter, QtCore.QRect(10, 10, 80, 80), QtGui.QBrush(QColor(0, 0, 255)), 5.0
    )
    painter.end()


def test_draw_rounded_rect_qrect_radiuses(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRoundedRect(
        painter,
        QtCore.QRect(10, 10, 80, 80),
        QtGui.QBrush(QColor(0, 255, 0)),
        RadiusesF(5.0),
    )
    painter.end()


def test_draw_rounded_rect_border(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRoundedRectBorder(
        painter, QtCore.QRectF(10, 10, 80, 80), QColor(255, 0, 0), 2.0, 5.0
    )
    painter.end()


def test_draw_rounded_rect_border_radiuses(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRoundedRectBorder(
        painter,
        QtCore.QRect(10, 10, 80, 80),
        QColor(255, 0, 0),
        2.0,
        RadiusesF(5.0),
    )
    painter.end()


def test_draw_rect_border(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRectBorder(
        painter, QtCore.QRect(10, 10, 80, 80), QColor(0, 0, 0), 1.0
    )
    painter.end()


def test_draw_rounded_triangle(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRoundedTriangle(painter, QtCore.QRectF(10, 10, 80, 80), 3.0)
    painter.end()


def test_draw_checkerboard(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawCheckerboard(
        painter,
        QtCore.QRectF(0, 0, 100, 100),
        QColor(200, 200, 200),
        QColor(255, 255, 255),
        10.0,
    )
    painter.end()


def test_draw_progress_bar_value_rect(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawProgressBarValueRect(
        painter, QtCore.QRect(0, 0, 100, 20), QColor(0, 128, 255), 0.0, 100.0, 50.0
    )
    painter.end()


def test_draw_color_mark(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawColorMark(
        painter, QtCore.QRect(10, 10, 20, 20), QColor(255, 0, 0), QColor(0, 0, 0)
    )
    painter.end()


def test_draw_debug_rect(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawDebugRect(QtCore.QRect(10, 10, 80, 80), painter)
    painter.end()


def test_get_menu_indicator_path(qapp):
    path = Qlementine.getMenuIndicatorPath(QtCore.QRect(0, 0, 20, 20))
    assert isinstance(path, QtGui.QPainterPath)


def test_draw_combo_box_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawComboBoxIndicator(QtCore.QRect(10, 10, 20, 20), painter)
    painter.end()


def test_draw_check_box_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawCheckBoxIndicator(QtCore.QRect(0, 0, 16, 16), painter)
    painter.end()


def test_draw_radio_button_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRadioButtonIndicator(QtCore.QRect(0, 0, 16, 16), painter)
    painter.end()


def test_draw_arrows(qapp):
    _pixmap, painter = _make_painter()
    rect = QtCore.QRect(10, 10, 20, 20)
    Qlementine.drawArrowRight(rect, painter)
    Qlementine.drawArrowLeft(rect, painter)
    Qlementine.drawArrowDown(rect, painter)
    Qlementine.drawArrowUp(rect, painter)
    painter.end()


def test_draw_close_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawCloseIndicator(QtCore.QRect(0, 0, 16, 16), painter)
    painter.end()


def test_draw_tree_view_indicator(qapp):
    _pixmap, painter = _make_painter()
    rect = QtCore.QRect(0, 0, 16, 16)
    Qlementine.drawTreeViewIndicator(rect, painter, True)
    Qlementine.drawTreeViewIndicator(rect, painter, False)
    painter.end()


def test_draw_calendar_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawCalendarIndicator(
        QtCore.QRect(0, 0, 16, 16), painter, QColor(0, 0, 0)
    )
    painter.end()


def test_draw_grip_indicator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawGripIndicator(
        QtCore.QRect(0, 0, 20, 20),
        painter,
        QColor(128, 128, 128),
        Qt.Orientation.Horizontal,
    )
    painter.end()


def test_get_tick_interval():
    result = Qlementine.getTickInterval(0, 1, 10, 0, 100, 200)
    assert isinstance(result, int)


def test_draw_tab(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawTab(
        painter,
        QtCore.QRect(0, 0, 80, 30),
        RadiusesF(5.0),
        QColor(200, 200, 200),
    )
    painter.end()


def test_draw_tab_shadow(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawTabShadow(
        painter,
        QtCore.QRect(0, 0, 80, 30),
        RadiusesF(5.0),
        QColor(0, 0, 0),
    )
    painter.end()


def test_draw_radio_button(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawRadioButton(
        painter,
        QtCore.QRect(0, 0, 20, 20),
        QColor(255, 255, 255),
        QColor(128, 128, 128),
        QColor(0, 120, 212),
        1.0,
        1.0,
    )
    painter.end()


def test_draw_check_button(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawCheckButton(
        painter,
        QtCore.QRect(0, 0, 20, 20),
        3.0,
        QColor(255, 255, 255),
        QColor(128, 128, 128),
        QColor(0, 120, 212),
        1.0,
        1.0,
        CheckState.Checked,
    )
    painter.end()


def test_draw_menu_separator(qapp):
    _pixmap, painter = _make_painter()
    Qlementine.drawMenuSeparator(
        painter, QtCore.QRect(0, 0, 100, 2), QColor(200, 200, 200), 1
    )
    painter.end()


def test_remove_trailing_whitespaces():
    assert Qlementine.removeTrailingWhitespaces("hello   ") == "hello"
    assert Qlementine.removeTrailingWhitespaces("no trailing") == "no trailing"


def test_displayed_shortcut_string():
    from PyQt6.QtGui import QKeySequence

    ks = QKeySequence("Ctrl+S")
    result = Qlementine.displayedShortcutString(ks)
    assert isinstance(result, str)
    assert len(result) > 0


def test_shortcut_size_hint(qapp):
    from PyQt6.QtGui import QKeySequence

    ks = QKeySequence("Ctrl+S")
    size = Qlementine.shortcutSizeHint(ks, Theme())
    assert isinstance(size, QtCore.QSize)
    assert size.width() > 0


def test_make_check_pixmap(qapp):
    result = Qlementine.makeCheckPixmap(QSize(16, 16), QColor(0, 0, 0))
    assert isinstance(result, QtGui.QPixmap)
    assert not result.isNull()


def test_make_arrow_pixmaps(qapp):
    for func in [Qlementine.makeArrowLeftPixmap, Qlementine.makeArrowRightPixmap]:
        result = func(QSize(16, 16), QColor(0, 0, 0))
        assert isinstance(result, QtGui.QPixmap)


def test_make_message_box_pixmaps(qapp):
    for func in [
        Qlementine.makeMessageBoxWarningPixmap,
        Qlementine.makeMessageBoxCriticalPixmap,
        Qlementine.makeMessageBoxQuestionPixmap,
        Qlementine.makeMessageBoxInformationPixmap,
    ]:
        result = func(QSize(32, 32), QColor(255, 200, 0), QColor(0, 0, 0))
        assert isinstance(result, QtGui.QPixmap)


def test_get_tab_path(qapp):
    path = Qlementine.getTabPath(QtCore.QRect(0, 0, 80, 30), RadiusesF(5.0))
    assert isinstance(path, QtGui.QPainterPath)


def test_draw_elided_multi_line_text(qapp):
    pixmap, painter = _make_painter()
    Qlementine.drawElidedMultiLineText(
        painter, QtCore.QRect(0, 0, 80, 80), "Hello World", pixmap
    )
    painter.end()


def test_draw_shortcut(qapp):
    from PyQt6.QtGui import QKeySequence

    _pixmap, painter = _make_painter()
    ks = QKeySequence("Ctrl+S")
    Qlementine.drawShortcut(painter, ks, QtCore.QRect(0, 0, 80, 20), Theme(), True)
    painter.end()


def test_draw_icon(qapp):
    _pixmap, painter = _make_painter()
    icon = QtGui.QIcon()
    w = QWidget()
    Qlementine.drawIcon(
        QtCore.QRect(0, 0, 16, 16),
        painter,
        icon,
        MouseState.Normal,
        CheckState.NotChecked,
        w,
    )
    painter.end()
