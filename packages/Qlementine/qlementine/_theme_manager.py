"""ThemeManager - manages a collection of Themes for a QlementineStyle."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from qlementine._qt import QtCore, Signal
from qlementine._theme import Theme

if TYPE_CHECKING:
    from qlementine._style import QlementineStyle

__all__ = ["ThemeManager"]


class ThemeManager(QtCore.QObject):
    """Stores a list of Theme objects and synchronises with a style."""

    currentThemeChanged = Signal()
    themeCountChanged = Signal()

    def __init__(
        self,
        style: QlementineStyle | None = None,
        parent: QtCore.QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._themes: list[Theme] = []
        self._style: QlementineStyle | None = None
        self._current_index: int = -1
        if style is not None:
            self.setStyle(style)

    def style(self) -> QlementineStyle | None:
        return self._style

    def setStyle(self, style: QlementineStyle | None) -> None:
        if style is not self._style:
            self._style = style
            self._synchronize_theme_on_style()
            self.currentThemeChanged.emit()
            self.themeCountChanged.emit()

    def themes(self) -> list[Theme]:
        return self._themes

    def addTheme(self, theme: Theme) -> None:
        self._themes.append(theme)
        self.themeCountChanged.emit()
        if self._current_index < 0:
            self.setCurrentThemeIndex(0)

    def loadDirectory(self, path: str) -> None:
        if not os.path.isdir(path):
            return
        entries = sorted(os.listdir(path), key=str.lower)
        for name in entries:
            if not name.lower().endswith(".json"):
                continue
            full = os.path.join(path, name)
            if not os.path.isfile(full):
                continue
            try:
                theme = Theme.fromJsonPath(full)
            except ValueError:
                continue
            self.addTheme(theme)

    def currentTheme(self) -> str:
        if 0 <= self._current_index < self.themeCount():
            return self._themes[self._current_index].meta.name
        return ""

    def setCurrentTheme(self, key: str) -> None:
        index = self.themeIndex(key)
        self.setCurrentThemeIndex(index)

    def currentThemeIndex(self) -> int:
        return self._current_index

    def setCurrentThemeIndex(self, index: int) -> None:
        if 0 <= index < self.themeCount():
            if index != self._current_index:
                self._current_index = index
                self._synchronize_theme_on_style()
                self.currentThemeChanged.emit()

    def themeCount(self) -> int:
        return len(self._themes)

    def setNextTheme(self) -> None:
        if self.themeCount() > 1:
            nxt = (self._current_index + 1) % self.themeCount()
            self.setCurrentThemeIndex(nxt)

    def setPreviousTheme(self) -> None:
        if self.themeCount() > 1:
            prev = self._current_index - 1
            if prev < 0:
                prev = self.themeCount() - 1
            self.setCurrentThemeIndex(prev)

    def themeIndex(self, key: str) -> int:
        for i, theme in enumerate(self._themes):
            if theme.meta.name == key:
                return i
        return -1

    def _synchronize_theme_on_style(self) -> None:
        if self._style is None:
            return
        if not self._themes:
            return
        if 0 <= self._current_index < self.themeCount():
            self._style.setTheme(self._themes[self._current_index])
        else:
            self.addTheme(self._style.theme())
            self.setCurrentThemeIndex(self.themeCount() - 1)
