"""Menu utility functions."""

from __future__ import annotations

from qlementine._qt import QtCore, QtWidgets

QMenu = QtWidgets.QMenu
QTimer = QtCore.QTimer

__all__ = [
    "flashAction",
    "getTopLevelMenu",
]


def getTopLevelMenu(menu: QMenu) -> QMenu:
    """Walk up the parent chain and return the top-level QMenu."""
    parent = menu
    while parent is not None:
        parent_menu = parent.parentWidget()
        if isinstance(parent_menu, QMenu):
            parent = parent_menu
        else:
            break
    return parent


_FLASH_BLINK_DURATION = 60  # ms
_FLASH_DURATION = 60  # ms


def flashAction(
    action: QtWidgets.QAction,
    menu: QMenu,
    onAnimationFinished: object | None = None,
) -> None:
    """Flash a menu action (animate highlight blink)."""
    if menu is None or action is None:
        return

    action.setProperty("qlementine_flashing", True)
    menu.blockSignals(True)
    elapsed = 0

    def _tick() -> None:
        nonlocal elapsed
        if elapsed < _FLASH_DURATION and menu and action:
            elapsed += _FLASH_BLINK_DURATION
            current = menu.activeAction()
            menu.setActiveAction(action if current is None else None)
        else:
            timer.stop()
            if action:
                action.setProperty("qlementine_flashing", False)
            if menu:
                menu.setActiveAction(action)
                menu.blockSignals(False)
            if callable(onAnimationFinished):
                onAnimationFinished()

    timer = QTimer(action)
    timer.setInterval(_FLASH_BLINK_DURATION)
    timer.timeout.connect(_tick)
    timer.start()
