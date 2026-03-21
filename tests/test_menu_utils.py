"""Tests for MenuUtils free functions."""

from __future__ import annotations

from _qt_compat import Qlementine, QtWidgets


def test_get_top_level_menu_returns_self(qapp):
    menu = QtWidgets.QMenu()
    result = Qlementine.getTopLevelMenu(menu)
    assert result is menu


def test_get_top_level_menu_with_submenu(qapp):
    parent = QtWidgets.QMenu("Parent")
    child = parent.addMenu("Child")
    result = Qlementine.getTopLevelMenu(child)
    assert result is parent
