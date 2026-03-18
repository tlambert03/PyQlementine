"""Tests for all enums exposed by the Qlementine bindings."""

from __future__ import annotations

from _qt_compat import Qlementine


def test_color_role_members():
    assert Qlementine.ColorRole.Primary is not None
    assert Qlementine.ColorRole.Secondary is not None


def test_color_role_distinct():
    assert Qlementine.ColorRole.Primary != Qlementine.ColorRole.Secondary


def test_mouse_state_members():
    ms = Qlementine.MouseState
    assert ms.Transparent is not None
    assert ms.Normal is not None
    assert ms.Hovered is not None
    assert ms.Pressed is not None
    assert ms.Disabled is not None


def test_mouse_state_distinct():
    ms = Qlementine.MouseState
    values = {ms.Transparent, ms.Normal, ms.Hovered, ms.Pressed, ms.Disabled}
    assert len(values) == 5


def test_check_state_members():
    cs = Qlementine.CheckState
    assert cs.NotChecked is not None
    assert cs.Checked is not None
    assert cs.Indeterminate is not None


def test_focus_state_members():
    assert Qlementine.FocusState.NotFocused is not None
    assert Qlementine.FocusState.Focused is not None


def test_active_state_members():
    assert Qlementine.ActiveState.NotActive is not None
    assert Qlementine.ActiveState.Active is not None


def test_selection_state_members():
    assert Qlementine.SelectionState.NotSelected is not None
    assert Qlementine.SelectionState.Selected is not None


def test_alternate_state_members():
    assert Qlementine.AlternateState.NotAlternate is not None
    assert Qlementine.AlternateState.Alternate is not None


def test_default_state_members():
    assert Qlementine.DefaultState.NotDefault is not None
    assert Qlementine.DefaultState.Default is not None


def test_status_members():
    s = Qlementine.Status
    assert s.Default is not None
    assert s.Info is not None
    assert s.Success is not None
    assert s.Warning is not None
    assert s.Error is not None


def test_status_distinct():
    s = Qlementine.Status
    values = {s.Default, s.Info, s.Success, s.Warning, s.Error}
    assert len(values) == 5


def test_text_role_members():
    tr = Qlementine.TextRole
    assert tr.Caption is not None
    assert tr.Default is not None
    assert tr.H1 is not None
    assert tr.H2 is not None
    assert tr.H3 is not None
    assert tr.H4 is not None
    assert tr.H5 is not None


def test_text_role_distinct():
    tr = Qlementine.TextRole
    values = {tr.Caption, tr.Default, tr.H1, tr.H2, tr.H3, tr.H4, tr.H5}
    assert len(values) == 7


def test_color_mode_members():
    assert Qlementine.ColorMode.RGB is not None
    assert Qlementine.ColorMode.RGBA is not None


def test_color_mode_distinct():
    assert Qlementine.ColorMode.RGB != Qlementine.ColorMode.RGBA


def test_auto_icon_color_members():
    aic = Qlementine.AutoIconColor
    assert aic.None_ is not None
    assert aic.ForegroundColor is not None
    assert aic.TextColor is not None


def test_status_badge_members():
    sb = Qlementine.StatusBadge
    assert sb.Success is not None
    assert sb.Info is not None
    assert sb.Warning is not None
    assert sb.Error is not None


def test_status_badge_size_members():
    sbs = Qlementine.StatusBadgeSize
    assert sbs.Small is not None
    assert sbs.Medium is not None


def test_colorize_mode_members():
    cm = Qlementine.ColorizeMode
    assert cm.Colorize is not None
    assert cm.Tint is not None
