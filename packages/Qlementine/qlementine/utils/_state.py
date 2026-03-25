"""State utility functions."""

from __future__ import annotations

from qlementine._qt import QtCore, QtGui, QtWidgets
from qlementine._enums import (
    ActiveState,
    AlternateState,
    CheckState,
    ColorRole,
    FocusState,
    MouseState,
    SelectionState,
)

QStyle = QtWidgets.QStyle
Qt = QtCore.Qt
QIcon = QtGui.QIcon
QPalette = QtGui.QPalette

__all__ = [
    "activeStateToString",
    "checkStateToString",
    "focusStateToString",
    "getActiveState",
    "getAlternateState",
    "getCheckState",
    "getColorRole",
    "getComboBoxItemMouseState",
    "getFocusState",
    "getIconMode",
    "getIconState",
    "getMenuItemMouseState",
    "getMouseState",
    "getPaletteColorGroup",
    "getScrollBarHandleState",
    "getSelectionState",
    "getSliderHandleState",
    "getState",
    "getTabItemMouseState",
    "getToolButtonMouseState",
    "mouseStateToString",
    "printState",
    "selectionStateToString",
]


def getMouseState(
    flags_or_pressed: QStyle.StateFlag | bool,
    hovered: bool | None = None,
    enabled: bool | None = None,
) -> MouseState:
    """Get MouseState from QStyle.StateFlag or (pressed, hovered, enabled)."""
    if hovered is not None:
        # Called as getMouseState(pressed, hovered, enabled)
        pressed = bool(flags_or_pressed)
        en = enabled if enabled is not None else True
        if not en:
            return MouseState.Disabled
        if pressed:
            return MouseState.Pressed
        if hovered:
            return MouseState.Hovered
        return MouseState.Normal
    # Called with QStyle.StateFlag
    state = flags_or_hovered
    if not (state & QStyle.StateFlag.State_Enabled):
        return MouseState.Disabled
    if state & QStyle.StateFlag.State_Sunken:
        return MouseState.Pressed
    if state & QStyle.StateFlag.State_MouseOver:
        return MouseState.Hovered
    return MouseState.Normal


def getToolButtonMouseState(state: QStyle.StateFlag) -> MouseState:
    """Get MouseState for a tool button."""
    if not (state & QStyle.StateFlag.State_Enabled):
        return MouseState.Disabled
    if state & QStyle.StateFlag.State_Sunken:
        return MouseState.Pressed
    if (
        state & QStyle.StateFlag.State_MouseOver
        or state & QStyle.StateFlag.State_Selected
    ):
        return MouseState.Hovered
    return MouseState.Transparent


def getMenuItemMouseState(state: QStyle.StateFlag) -> MouseState:
    """Get MouseState for a menu item."""
    return getToolButtonMouseState(state)


def getComboBoxItemMouseState(state: QStyle.StateFlag) -> MouseState:
    """Get MouseState for a combo box item."""
    # state is already a QStyle.StateFlag
    if not (state & QStyle.StateFlag.State_Enabled):
        return MouseState.Disabled
    if state & QStyle.StateFlag.State_Sunken:
        return MouseState.Pressed
    if state & QStyle.StateFlag.State_Selected:
        return MouseState.Hovered
    return MouseState.Transparent


def getTabItemMouseState(
    state: QStyle.StateFlag, tabIsHovered: bool
) -> MouseState:
    """Get MouseState for a tab item."""
    # state is already a QStyle.StateFlag
    selected = bool(state & QStyle.StateFlag.State_Selected)
    if selected or tabIsHovered:
        if not (state & QStyle.StateFlag.State_Enabled):
            return MouseState.Disabled
        if state & QStyle.StateFlag.State_Sunken:
            return MouseState.Pressed
        if state & QStyle.StateFlag.State_MouseOver:
            return MouseState.Hovered
        return MouseState.Normal
    if state & QStyle.StateFlag.State_Enabled:
        return MouseState.Transparent
    return MouseState.Disabled


def getColorRole(
    checked_or_state: CheckState | QStyle.StateFlag | bool,
    isDefault: bool = False,
) -> ColorRole:
    """Get ColorRole from CheckState, state flags, or bool."""
    if isinstance(checked_or_state, CheckState):
        return getColorRole(
            checked_or_state == CheckState.Checked, False
        )
    if isinstance(checked_or_state, bool):
        return (
            ColorRole.Primary
            if checked_or_state or isDefault
            else ColorRole.Secondary
        )
    # QStyle.StateFlag
    on = bool(checked_or_state & QStyle.StateFlag.State_On)
    return getColorRole(on, isDefault)


def getSliderHandleState(
    state: QStyle.StateFlag,
    activeSubControls: QStyle.SubControl,
) -> MouseState:
    """Get MouseState for slider handle."""
    handleActive = (
        activeSubControls == QStyle.SubControl.SC_SliderHandle and state
    )
    return getMouseState(state) if handleActive else MouseState.Normal


def getScrollBarHandleState(
    state: QStyle.StateFlag,
    activeSubControls: QStyle.SubControl,
) -> MouseState:
    """Get MouseState for scroll bar handle."""
    # state is already a QStyle.StateFlag
    handleActive = (
        activeSubControls == QStyle.SubControl.SC_ScrollBarSlider
        and state
    )
    if handleActive:
        return getMouseState(state)
    if not (state & QStyle.StateFlag.State_Enabled):
        return MouseState.Disabled
    if state & QStyle.StateFlag.State_MouseOver:
        return MouseState.Normal
    return MouseState.Transparent


def getFocusState(
    flags_or_bool: QStyle.StateFlag | bool,
) -> FocusState:
    """Get FocusState from QStyle.StateFlag or bool."""
    if isinstance(flags_or_bool, bool):
        return (
            FocusState.Focused if flags_or_bool else FocusState.NotFocused
        )
    return (
        FocusState.Focused
        if flags_or_bool & QStyle.StateFlag.State_HasFocus
        else FocusState.NotFocused
    )


def getCheckState(
    flags_or_bool: QStyle.StateFlag | Qt.CheckState | bool,
) -> CheckState:
    """Get CheckState from QStyle.StateFlag, Qt.CheckState, or bool."""
    if isinstance(flags_or_bool, bool):
        return (
            CheckState.Checked
            if flags_or_bool
            else CheckState.NotChecked
        )
    if isinstance(flags_or_bool, Qt.CheckState):
        if flags_or_bool == Qt.CheckState.Checked:
            return CheckState.Checked
        if flags_or_bool == Qt.CheckState.PartiallyChecked:
            return CheckState.Indeterminate
        return CheckState.NotChecked
    # QStyle.StateFlag
    if flags_or_bool & QStyle.StateFlag.State_On:
        return CheckState.Checked
    if flags_or_bool & QStyle.StateFlag.State_NoChange:
        return CheckState.Indeterminate
    return CheckState.NotChecked


def getActiveState(state: QStyle.StateFlag) -> ActiveState:
    """Get ActiveState from QStyle.StateFlag."""
    # state is already a QStyle.StateFlag
    return (
        ActiveState.Active
        if state & QStyle.StateFlag.State_Active
        else ActiveState.NotActive
    )


def getSelectionState(state: QStyle.StateFlag) -> SelectionState:
    """Get SelectionState from QStyle.StateFlag."""
    # state is already a QStyle.StateFlag
    return (
        SelectionState.Selected
        if state & QStyle.StateFlag.State_Selected
        else SelectionState.NotSelected
    )


def getAlternateState(
    features: int,
) -> AlternateState:
    """Get AlternateState from QStyleOptionViewItem features."""
    VIF = QtWidgets.QStyleOptionViewItem.ViewItemFeature
    return (
        AlternateState.Alternate
        if features & VIF.Alternate
        else AlternateState.NotAlternate
    )


def getState(
    enabled: bool, hover: bool, pressed: bool
) -> QStyle.StateFlag:
    """Build QStyle.StateFlag from booleans."""
    result = QStyle.StateFlag(0)
    if enabled:
        result |= QStyle.StateFlag.State_Enabled
    if pressed:
        result |= QStyle.StateFlag.State_Sunken
    if hover:
        result |= QStyle.StateFlag.State_MouseOver
    return result


def getIconMode(mouse: MouseState) -> QIcon.Mode:
    """Get QIcon.Mode from MouseState."""
    if mouse == MouseState.Disabled:
        return QIcon.Mode.Disabled
    if mouse in (MouseState.Hovered, MouseState.Pressed):
        return QIcon.Mode.Active
    return QIcon.Mode.Normal


def getIconState(checked: CheckState) -> QIcon.State:
    """Get QIcon.State from CheckState."""
    if checked == CheckState.Checked:
        return QIcon.State.On
    return QIcon.State.Off


def getPaletteColorGroup(
    state_or_mouse: QStyle.StateFlag | MouseState,
) -> QPalette.ColorGroup:
    """Get QPalette.ColorGroup from QStyle.StateFlag or MouseState."""
    if isinstance(state_or_mouse, MouseState):
        if state_or_mouse == MouseState.Disabled:
            return QPalette.ColorGroup.Disabled
        if state_or_mouse == MouseState.Hovered:
            return QPalette.ColorGroup.Current
        if state_or_mouse == MouseState.Pressed:
            return QPalette.ColorGroup.Active
        return QPalette.ColorGroup.Normal
    if not (state_or_mouse & QStyle.StateFlag.State_Enabled):
        return QPalette.ColorGroup.Disabled
    return QPalette.ColorGroup.Normal


def mouseStateToString(state: MouseState) -> str:
    """Convert MouseState to string."""
    _MAP = {
        MouseState.Disabled: "disabled",
        MouseState.Hovered: "hovered",
        MouseState.Normal: "normal",
        MouseState.Pressed: "pressed",
        MouseState.Transparent: "transparent",
    }
    return _MAP.get(state, "")


def focusStateToString(state: FocusState) -> str:
    """Convert FocusState to string."""
    _MAP = {
        FocusState.Focused: "focused",
        FocusState.NotFocused: "not focused",
    }
    return _MAP.get(state, "")


def activeStateToString(state: ActiveState) -> str:
    """Convert ActiveState to string."""
    _MAP = {
        ActiveState.Active: "active",
        ActiveState.NotActive: "not active",
    }
    return _MAP.get(state, "")


def selectionStateToString(state: SelectionState) -> str:
    """Convert SelectionState to string."""
    _MAP = {
        SelectionState.Selected: "selected",
        SelectionState.NotSelected: "not selected",
    }
    return _MAP.get(state, "")


def checkStateToString(state: CheckState) -> str:
    """Convert CheckState to string."""
    _MAP = {
        CheckState.Checked: "checked",
        CheckState.NotChecked: "not checked",
        CheckState.Indeterminate: "indeterminate",
    }
    return _MAP.get(state, "")


def printState(state: QStyle.StateFlag) -> str:
    """Return a human-readable description of QStyle.StateFlag."""
    mouse = getMouseState(state)
    focused = getFocusState(state)
    active = getActiveState(state)
    selected = getSelectionState(state)
    checked = getCheckState(state)
    return (
        "{ "
        f"mouse: {mouseStateToString(mouse)}, "
        f"focus: {focusStateToString(focused)}, "
        f"active: {activeStateToString(active)}, "
        f"selected: {selectionStateToString(selected)}, "
        f"checked: {checkStateToString(checked)}"
        " }"
    )
