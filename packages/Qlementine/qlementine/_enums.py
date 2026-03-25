"""Qlementine enum types."""

from __future__ import annotations

from enum import IntEnum

__all__ = [
    "ActiveState",
    "AlternateState",
    "AutoIconColor",
    "CheckState",
    "ColorMode",
    "ColorRole",
    "ColorizeMode",
    "DefaultState",
    "FocusState",
    "MouseState",
    "SelectionState",
    "Status",
    "StatusBadge",
    "StatusBadgeSize",
    "TextRole",
]


class ColorRole(IntEnum):
    """Color family to highlight or not the widget."""

    Primary = 0
    Secondary = 1


class MouseState(IntEnum):
    """Mouse interaction state."""

    Transparent = 0
    Normal = 1
    Hovered = 2
    Pressed = 3
    Disabled = 4


class CheckState(IntEnum):
    """Is the widget checked or not."""

    NotChecked = 0
    Checked = 1
    Indeterminate = 2


class FocusState(IntEnum):
    """Has the widget keyboard focus or not."""

    NotFocused = 0
    Focused = 1


class ActiveState(IntEnum):
    """Is the list element the current item."""

    NotActive = 0
    Active = 1


class SelectionState(IntEnum):
    """Is the widget selected or not."""

    NotSelected = 0
    Selected = 1


class AlternateState(IntEnum):
    """Does the ListView row need alternate color."""

    NotAlternate = 0
    Alternate = 1


class DefaultState(IntEnum):
    """Is the button the default button."""

    NotDefault = 0
    Default = 1


class Status(IntEnum):
    """Feedback status displayed to the user."""

    Default = 0
    Info = 1
    Success = 2
    Warning = 3
    Error = 4


class TextRole(IntEnum):
    """Role given to the text or QLabel."""

    Caption = -1
    Default = 0
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5


class ColorMode(IntEnum):
    """Color mode."""

    RGB = 0
    RGBA = 1


class AutoIconColor(IntEnum):
    """Automatic icon colorization mode."""

    None_ = 0
    ForegroundColor = 1
    TextColor = 2


class ColorizeMode(IntEnum):
    """How to apply color to a pixmap."""

    Colorize = 0
    Tint = 1


class StatusBadge(IntEnum):
    """Status badge type."""

    Success = 0
    Info = 1
    Warning = 2
    Error = 3


class StatusBadgeSize(IntEnum):
    """Status badge size."""

    Small = 0
    Medium = 1
