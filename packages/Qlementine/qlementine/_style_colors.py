"""Color accessor mixin for QlementineStyle."""

from __future__ import annotations

from qlementine._qt import QtGui
from qlementine._enums import (
    ActiveState,
    AlternateState,
    AutoIconColor,
    CheckState,
    ColorRole,
    FocusState,
    MouseState,
    SelectionState,
    Status,
    TextRole,
)
from qlementine.utils._color import colorWithAlphaF, getColorSourceOver

QColor = QtGui.QColor
QFont = QtGui.QFont
QPalette = QtGui.QPalette

__all__ = ["QlementineStyleColorsMixin"]


class QlementineStyleColorsMixin:
    """Mixin providing ~90 virtual color accessor methods.

    Subclass must set ``self._theme`` to a ``Theme`` instance.
    """

    # ------------------------------------------------------------------
    # Generic color
    # ------------------------------------------------------------------

    def color(self, mouse: MouseState, role: ColorRole) -> QColor:
        primary = role == ColorRole.Primary
        if mouse == MouseState.Pressed:
            return (
                self._theme.primaryColorPressed
                if primary
                else self._theme.secondaryColorPressed
            )
        if mouse == MouseState.Hovered:
            return (
                self._theme.primaryColorHovered
                if primary
                else self._theme.secondaryColorHovered
            )
        if mouse == MouseState.Disabled:
            return (
                self._theme.primaryColorDisabled
                if primary
                else self._theme.secondaryColorDisabled
            )
        if mouse == MouseState.Transparent:
            return (
                self._theme.primaryColorTransparent
                if primary
                else self._theme.secondaryColorTransparent
            )
        return (
            self._theme.primaryColor
            if primary
            else self._theme.secondaryColor
        )

    # ------------------------------------------------------------------
    # Frame
    # ------------------------------------------------------------------

    def frameBackgroundColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.backgroundColorMainTransparent
        return self._theme.backgroundColorMain1

    # ------------------------------------------------------------------
    # Button
    # ------------------------------------------------------------------

    def buttonBackgroundColor(
        self,
        mouse: MouseState,
        role: ColorRole,
        w: object = None,
    ) -> QColor:
        primary = role == ColorRole.Primary
        if mouse == MouseState.Pressed:
            return (
                self._theme.primaryColorPressed
                if primary
                else self._theme.neutralColorPressed
            )
        if mouse == MouseState.Hovered:
            return (
                self._theme.primaryColorHovered
                if primary
                else self._theme.neutralColorHovered
            )
        if mouse == MouseState.Disabled:
            return (
                self._theme.primaryColorDisabled
                if primary
                else self._theme.neutralColorDisabled
            )
        if mouse == MouseState.Transparent:
            return (
                self._theme.primaryColorTransparent
                if primary
                else self._theme.neutralColorTransparent
            )
        return (
            self._theme.primaryColor
            if primary
            else self._theme.neutralColor
        )

    def buttonForegroundColor(
        self,
        mouse: MouseState,
        role: ColorRole,
        w: object = None,
    ) -> QColor:
        primary = role == ColorRole.Primary
        if mouse == MouseState.Pressed:
            return (
                self._theme.primaryColorForegroundPressed
                if primary
                else self._theme.secondaryColor
            )
        if mouse == MouseState.Hovered:
            return (
                self._theme.primaryColorForegroundHovered
                if primary
                else self._theme.secondaryColor
            )
        if mouse == MouseState.Disabled:
            return (
                self._theme.primaryColorForegroundDisabled
                if primary
                else self._theme.secondaryColorDisabled
            )
        return (
            self._theme.primaryColorForeground
            if primary
            else self._theme.secondaryColor
        )

    # ------------------------------------------------------------------
    # Tool button
    # ------------------------------------------------------------------

    def toolButtonBackgroundColor(
        self, mouse: MouseState, role: ColorRole
    ) -> QColor:
        primary = role == ColorRole.Primary
        if mouse == MouseState.Pressed:
            return (
                self._theme.primaryColorPressed
                if primary
                else self._theme.neutralColorHovered
            )
        if mouse == MouseState.Hovered:
            return (
                self._theme.primaryColorHovered
                if primary
                else self._theme.neutralColor
            )
        if mouse == MouseState.Disabled:
            return (
                self._theme.primaryColorDisabled
                if primary
                else self._theme.neutralColorTransparent
            )
        return (
            self._theme.primaryColor
            if primary
            else self._theme.neutralColorTransparent
        )

    def toolButtonForegroundColor(
        self, mouse: MouseState, role: ColorRole
    ) -> QColor:
        primary = role == ColorRole.Primary
        if mouse == MouseState.Disabled:
            return (
                self._theme.primaryColorForegroundDisabled
                if primary
                else self._theme.secondaryColorDisabled
            )
        return (
            self._theme.primaryColorForeground
            if primary
            else self._theme.secondaryColor
        )

    def toolButtonSeparatorColor(
        self, mouse: MouseState, role: ColorRole
    ) -> QColor:
        if mouse == MouseState.Pressed:
            return self._theme.neutralColorPressed
        if mouse == MouseState.Hovered:
            return self._theme.neutralColorHovered
        if mouse == MouseState.Normal:
            return self._theme.neutralColor
        return self._theme.neutralColorDisabled

    # ------------------------------------------------------------------
    # Command button
    # ------------------------------------------------------------------

    def commandButtonBackgroundColor(
        self, mouse: MouseState, role: ColorRole
    ) -> QColor:
        return self.buttonBackgroundColor(mouse, role)

    def commandButtonTextColor(
        self, mouse: MouseState, role: ColorRole
    ) -> QColor:
        return self.toolButtonForegroundColor(mouse, role)

    def commandButtonDescriptionColor(
        self, mouse: MouseState, role: ColorRole
    ) -> QColor:
        primary = role == ColorRole.Primary
        if mouse == MouseState.Disabled:
            return (
                self._theme.primaryColorForegroundDisabled
                if primary
                else self._theme.secondaryAlternativeColorDisabled
            )
        return (
            self._theme.primaryColorForegroundDisabled
            if primary
            else self._theme.secondaryAlternativeColor
        )

    def commandButtonIconColor(
        self, mouse: MouseState, role: ColorRole
    ) -> QColor:
        return self.commandButtonTextColor(mouse, role)

    # ------------------------------------------------------------------
    # Check button
    # ------------------------------------------------------------------

    def checkButtonBackgroundColor(
        self, mouse: MouseState, checked: CheckState
    ) -> QColor:
        if checked in (CheckState.Checked, CheckState.Indeterminate):
            return self.buttonBackgroundColor(mouse, ColorRole.Primary)
        # NotChecked
        if mouse == MouseState.Pressed:
            return self._theme.backgroundColorMain3
        if mouse == MouseState.Disabled:
            return self._theme.backgroundColorMain2
        return self._theme.backgroundColorMain1

    def checkButtonForegroundColor(
        self, mouse: MouseState, checked: CheckState
    ) -> QColor:
        return self.buttonForegroundColor(mouse, ColorRole.Primary)

    def checkButtonBorderColor(
        self,
        mouse: MouseState,
        focus: FocusState,
        checked: CheckState,
    ) -> QColor:
        if checked in (CheckState.Checked, CheckState.Indeterminate):
            return self.checkButtonBackgroundColor(mouse, checked)
        # NotChecked
        if focus == FocusState.Focused:
            return self._theme.primaryColor
        if mouse == MouseState.Hovered:
            return self._theme.borderColorHovered
        if mouse == MouseState.Pressed:
            return self._theme.borderColorPressed
        if mouse == MouseState.Disabled:
            return self._theme.borderColorDisabled
        return self._theme.borderColor

    # ------------------------------------------------------------------
    # Radio button
    # ------------------------------------------------------------------

    def radioButtonBackgroundColor(
        self, mouse: MouseState, checked: CheckState
    ) -> QColor:
        return self.checkButtonBackgroundColor(mouse, checked)

    def radioButtonForegroundColor(
        self, mouse: MouseState, checked: CheckState
    ) -> QColor:
        return self.checkButtonForegroundColor(mouse, checked)

    def radioButtonBorderColor(
        self,
        mouse: MouseState,
        focus: FocusState,
        checked: CheckState,
    ) -> QColor:
        return self.checkButtonBorderColor(mouse, focus, checked)

    # ------------------------------------------------------------------
    # ComboBox
    # ------------------------------------------------------------------

    def comboBoxBackgroundColor(self, mouse: MouseState) -> QColor:
        return self.buttonBackgroundColor(mouse, ColorRole.Secondary)

    def comboBoxForegroundColor(self, mouse: MouseState) -> QColor:
        return self.buttonForegroundColor(mouse, ColorRole.Secondary)

    def comboBoxTextColor(
        self,
        mouse: MouseState,
        status: Status,
        w: object = None,
    ) -> QColor:
        if status == Status.Error:
            return self._theme.statusColorError
        if status == Status.Warning:
            return self._theme.statusColorWarning
        if status == Status.Success:
            return self._theme.statusColorSuccess
        return self.comboBoxForegroundColor(mouse)

    # ------------------------------------------------------------------
    # SpinBox
    # ------------------------------------------------------------------

    def spinBoxBackgroundColor(self, mouse: MouseState) -> QColor:
        return self.textFieldBackgroundColor(mouse, Status.Default)

    def spinBoxBorderColor(
        self, mouse: MouseState, focus: FocusState
    ) -> QColor:
        return self.textFieldBorderColor(mouse, focus, Status.Default)

    def spinBoxButtonBackgroundColor(self, mouse: MouseState) -> QColor:
        return self.buttonBackgroundColor(mouse, ColorRole.Secondary)

    def spinBoxButtonForegroundColor(self, mouse: MouseState) -> QColor:
        return self.buttonForegroundColor(mouse, ColorRole.Secondary)

    # ------------------------------------------------------------------
    # List item
    # ------------------------------------------------------------------

    def listItemRowBackgroundColor(
        self, mouse: MouseState, alternate: AlternateState
    ) -> QColor:
        is_alternate = alternate == AlternateState.Alternate
        is_enabled = mouse != MouseState.Disabled
        group = (
            QPalette.ColorGroup.Normal
            if is_enabled
            else QPalette.ColorGroup.Disabled
        )
        cr = (
            QPalette.ColorRole.AlternateBase
            if is_alternate
            else QPalette.ColorRole.Base
        )
        return self._theme.palette.color(group, cr)

    def listItemBackgroundColor(
        self,
        mouse: MouseState,
        selected: SelectionState,
        focus: FocusState,
        active: ActiveState,
        index: object = None,
        widget: object = None,
    ) -> QColor:
        is_selected = selected == SelectionState.Selected
        is_active = (
            active == ActiveState.Active and focus == FocusState.Focused
        )

        if is_active:
            if mouse == MouseState.Pressed:
                return (
                    self._theme.primaryColor
                    if is_selected
                    else self._theme.neutralColor
                )
            if mouse == MouseState.Hovered:
                return (
                    self._theme.primaryColor
                    if is_selected
                    else self._theme.neutralColorDisabled
                )
            if mouse == MouseState.Disabled:
                return (
                    self._theme.primaryColorDisabled
                    if is_selected
                    else self._theme.neutralColorTransparent
                )
            return (
                self._theme.primaryColor
                if is_selected
                else self._theme.neutralColorTransparent
            )
        else:
            if mouse == MouseState.Pressed:
                return self._theme.neutralColor
            if mouse == MouseState.Hovered:
                return (
                    self._theme.neutralColor
                    if is_selected
                    else self._theme.neutralColorDisabled
                )
            if mouse == MouseState.Disabled:
                return (
                    self._theme.neutralColor
                    if is_selected
                    else self._theme.neutralColorTransparent
                )
            return (
                self._theme.neutralColor
                if is_selected
                else self._theme.neutralColorTransparent
            )

    def listItemForegroundColor(
        self,
        mouse: MouseState,
        selected: SelectionState,
        focus: FocusState,
        active: ActiveState,
    ) -> QColor:
        is_selected = selected == SelectionState.Selected
        is_active = active == ActiveState.Active

        if is_active:
            if mouse == MouseState.Disabled:
                return (
                    self._theme.primaryColorForegroundDisabled
                    if is_selected
                    else self._theme.secondaryColorDisabled
                )
            return (
                self._theme.primaryColorForeground
                if is_selected
                else self._theme.secondaryColor
            )
        else:
            if mouse == MouseState.Disabled:
                return self._theme.secondaryColorDisabled
            return self._theme.secondaryColor

    def listItemAutoIconColor(
        self,
        mouse: MouseState,
        selected: SelectionState,
        focus: FocusState,
        active: ActiveState,
        index: object = None,
        widget: object = None,
    ) -> AutoIconColor:
        return self.autoIconColor(widget)

    def listItemCaptionForegroundColor(
        self,
        mouse: MouseState,
        selected: SelectionState,
        focus: FocusState,
        active: ActiveState,
    ) -> QColor:
        is_selected = selected == SelectionState.Selected
        is_active = active == ActiveState.Active

        if is_active:
            if mouse == MouseState.Disabled:
                return (
                    self._theme.primaryColorForegroundDisabled
                    if is_selected
                    else self._theme.secondaryAlternativeColorDisabled
                )
            return (
                self._theme.primaryColorForeground
                if is_selected
                else self._theme.secondaryAlternativeColor
            )
        else:
            if mouse == MouseState.Disabled:
                return self._theme.secondaryAlternativeColorDisabled
            return self._theme.secondaryAlternativeColor

    def listItemCheckButtonBackgroundColor(
        self,
        mouse: MouseState,
        checked: CheckState,
        selected: SelectionState,
        active: ActiveState,
    ) -> QColor:
        is_checked = checked != CheckState.NotChecked
        is_enabled = mouse != MouseState.Disabled
        if selected == SelectionState.Selected:
            if is_enabled:
                return (
                    self._theme.primaryAlternativeColor
                    if is_checked
                    else self._theme.backgroundColorMain1
                )
            return (
                self._theme.primaryAlternativeColorDisabled
                if is_checked
                else self._theme.neutralColorDisabled
            )
        # NotSelected
        if is_enabled:
            return (
                self._theme.primaryColor
                if is_checked
                else self._theme.backgroundColorMain1
            )
        return (
            self._theme.primaryColorDisabled
            if is_checked
            else self._theme.backgroundColorMain2
        )

    def listItemCheckButtonBorderColor(
        self,
        mouse: MouseState,
        checked: CheckState,
        selected: SelectionState,
        active: ActiveState,
    ) -> QColor:
        is_checked = checked != CheckState.NotChecked
        is_enabled = mouse != MouseState.Disabled
        if selected == SelectionState.Selected:
            if is_enabled:
                return (
                    self._theme.primaryAlternativeColorTransparent
                    if is_checked
                    else self._theme.primaryColor
                )
            return (
                self._theme.primaryAlternativeColorTransparent
                if is_checked
                else self._theme.borderColorTransparent
            )
        # NotSelected
        if is_enabled:
            return (
                self._theme.primaryColor
                if is_checked
                else self._theme.borderColor
            )
        return (
            self._theme.primaryColorDisabled
            if is_checked
            else self._theme.borderColorDisabled
        )

    def listItemCheckButtonForegroundColor(
        self,
        mouse: MouseState,
        checked: CheckState,
        selected: SelectionState,
        active: ActiveState,
    ) -> QColor:
        return self.checkButtonForegroundColor(mouse, checked)

    def cellItemFocusBorderColor(
        self,
        focus: FocusState,
        selected: SelectionState,
        active: ActiveState,
    ) -> QColor:
        if selected == SelectionState.Selected:
            return (
                self._theme.neutralColorPressed
                if focus == FocusState.Focused
                else self._theme.neutralColorTransparent
            )
        return (
            self._theme.primaryColor
            if focus == FocusState.Focused
            else self._theme.primaryColorTransparent
        )

    # ------------------------------------------------------------------
    # Menu
    # ------------------------------------------------------------------

    def menuBackgroundColor(self) -> QColor:
        return self._theme.backgroundColorMain1

    def menuBorderColor(self) -> QColor:
        return self._theme.borderColor

    def menuSeparatorColor(self) -> QColor:
        return self._theme.borderColorDisabled

    def menuItemBackgroundColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Hovered:
            return self._theme.primaryColor
        if mouse == MouseState.Pressed:
            return self._theme.primaryColorHovered
        return self._theme.primaryColorTransparent

    def menuItemForegroundColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Hovered:
            return self._theme.primaryColorForegroundHovered
        if mouse == MouseState.Pressed:
            return self._theme.primaryColorForegroundPressed
        if mouse == MouseState.Disabled:
            return self._theme.secondaryColorDisabled
        return self._theme.secondaryColor

    def menuItemSecondaryForegroundColor(
        self, mouse: MouseState
    ) -> QColor:
        if mouse == MouseState.Hovered:
            return self._theme.primaryColorForegroundHovered
        if mouse == MouseState.Pressed:
            return self._theme.primaryColorForegroundPressed
        if mouse == MouseState.Disabled:
            return self._theme.secondaryAlternativeColorDisabled
        return self._theme.secondaryAlternativeColor

    # ------------------------------------------------------------------
    # Menu bar
    # ------------------------------------------------------------------

    def menuBarBackgroundColor(self) -> QColor:
        return self._theme.backgroundColorMain2

    def menuBarBorderColor(self) -> QColor:
        return self._theme.borderColor

    def menuBarItemBackgroundColor(
        self, mouse: MouseState, selected: SelectionState
    ) -> QColor:
        if mouse == MouseState.Hovered:
            return self._theme.neutralColorDisabled
        if mouse == MouseState.Pressed:
            return self._theme.neutralColor
        return self._theme.neutralColorTransparent

    def menuBarItemForegroundColor(
        self, mouse: MouseState, selected: SelectionState
    ) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.secondaryColorDisabled
        return self._theme.secondaryColor

    # ------------------------------------------------------------------
    # Tab bar / tabs
    # ------------------------------------------------------------------

    def tabBarBackgroundColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.backgroundColorMain3
        return self._theme.backgroundColorTabBar

    def tabBarShadowColor(self) -> QColor:
        return self._theme.shadowColor1

    def tabBarBottomShadowColor(self) -> QColor:
        return self._theme.shadowColor1

    def tabBackgroundColor(
        self, mouse: MouseState, selected: SelectionState
    ) -> QColor:
        is_selected = selected == SelectionState.Selected
        selected_tab = self._theme.backgroundColorMain2
        hover_tab = self._theme.neutralColor
        default_tab = self._theme.backgroundColorMainTransparent

        if mouse == MouseState.Hovered:
            return selected_tab if is_selected else hover_tab
        if mouse == MouseState.Pressed:
            return self._theme.backgroundColorMain2
        if mouse == MouseState.Normal:
            return selected_tab if is_selected else default_tab
        return default_tab

    def tabForegroundColor(
        self, mouse: MouseState, selected: SelectionState
    ) -> QColor:
        return self.buttonForegroundColor(mouse, ColorRole.Secondary)

    def tabCloseButtonBackgroundColor(
        self, mouse: MouseState, selected: SelectionState
    ) -> QColor:
        is_selected = selected == SelectionState.Selected
        if mouse == MouseState.Pressed:
            return (
                self._theme.neutralColorPressed
                if is_selected
                else self._theme.semiTransparentColor4
            )
        if mouse == MouseState.Hovered:
            return (
                self._theme.neutralColor
                if is_selected
                else self._theme.semiTransparentColor2
            )
        return (
            self._theme.neutralColorTransparent
            if is_selected
            else self._theme.semiTransparentColorTransparent
        )

    def tabCloseButtonForegroundColor(
        self, mouse: MouseState, selected: SelectionState
    ) -> QColor:
        if mouse in (
            MouseState.Pressed,
            MouseState.Hovered,
            MouseState.Normal,
        ):
            return self._theme.secondaryColor
        if mouse in (MouseState.Disabled, MouseState.Transparent):
            return self._theme.secondaryColorTransparent
        return (
            self._theme.secondaryColor
            if selected == SelectionState.Selected
            else self._theme.secondaryColorTransparent
        )

    def tabBarScrollButtonBackgroundColor(
        self, mouse: MouseState
    ) -> QColor:
        if mouse == MouseState.Pressed:
            return self._theme.semiTransparentColor4
        if mouse == MouseState.Hovered:
            return self._theme.semiTransparentColor2
        return self._theme.semiTransparentColorTransparent

    # ------------------------------------------------------------------
    # Progress bar
    # ------------------------------------------------------------------

    def progressBarGrooveColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.neutralColorDisabled
        return self._theme.neutralColor

    def progressBarValueColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.primaryColorDisabled
        return self._theme.primaryColor

    # ------------------------------------------------------------------
    # Text field
    # ------------------------------------------------------------------

    def textFieldBackgroundColor(
        self, mouse: MouseState, status: Status
    ) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.backgroundColorMain3
        return self._theme.backgroundColorMain1

    def textFieldBorderColor(
        self, mouse: MouseState, focus: FocusState, status: Status
    ) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.borderColorDisabled

        active = (
            focus == FocusState.Focused
            or mouse == MouseState.Hovered
            or mouse == MouseState.Pressed
        )
        if status == Status.Error:
            return (
                self._theme.statusColorErrorHovered
                if active
                else self._theme.statusColorError
            )
        if status == Status.Warning:
            return (
                self._theme.statusColorWarningHovered
                if active
                else self._theme.statusColorWarning
            )
        if status == Status.Success:
            return (
                self._theme.statusColorSuccessHovered
                if active
                else self._theme.statusColorSuccess
            )
        # Info / Default
        return (
            self._theme.primaryColor
            if active
            else self._theme.borderColor
        )

    def textFieldForegroundColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.secondaryColorDisabled
        return self._theme.secondaryColor

    # ------------------------------------------------------------------
    # Slider
    # ------------------------------------------------------------------

    def sliderGrooveColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.neutralColorDisabled
        return self._theme.neutralColor

    def sliderValueColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.primaryColorDisabled
        return self._theme.primaryColor

    def sliderHandleColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.neutralColorDisabled
        if mouse == MouseState.Pressed:
            return self._theme.primaryColorForegroundPressed
        if mouse == MouseState.Hovered:
            return self._theme.primaryColorForegroundHovered
        return self._theme.primaryColorForeground

    def sliderTickColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.borderColorDisabled
        return self._theme.borderColor

    # ------------------------------------------------------------------
    # Dial
    # ------------------------------------------------------------------

    def dialHandleColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.neutralColorDisabled
        return self._theme.neutralColor

    def dialGrooveColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.neutralColorDisabled
        return self._theme.neutralColorPressed

    def dialValueColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.primaryColorDisabled
        return self._theme.primaryColor

    def dialTickColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.neutralColorDisabled
        return self._theme.neutralColorPressed

    def dialMarkColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.secondaryColorDisabled
        return self._theme.secondaryColor

    def dialBackgroundColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.neutralColorDisabled
        return self._theme.neutralColorPressed

    # ------------------------------------------------------------------
    # Label
    # ------------------------------------------------------------------

    def labelForegroundColor(
        self, mouse: MouseState, w: object = None
    ) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.secondaryColorDisabled
        return self._theme.secondaryColor

    def labelCaptionForegroundColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.secondaryAlternativeColorDisabled
        return self._theme.secondaryAlternativeColor

    # ------------------------------------------------------------------
    # Icon foreground
    # ------------------------------------------------------------------

    def iconForegroundColor(
        self, mouse: MouseState, role: ColorRole
    ) -> QColor:
        primary = role == ColorRole.Primary
        if mouse == MouseState.Disabled:
            return (
                self._theme.primaryColorForegroundDisabled
                if primary
                else self._theme.secondaryColorForegroundDisabled
            )
        return (
            self._theme.primaryColorForeground
            if primary
            else self._theme.secondaryColorForeground
        )

    # ------------------------------------------------------------------
    # Toolbar
    # ------------------------------------------------------------------

    def toolBarBackgroundColor(self) -> QColor:
        return self._theme.backgroundColorMain2

    def toolBarBorderColor(self) -> QColor:
        return self._theme.borderColor

    def toolBarSeparatorColor(self) -> QColor:
        return self._theme.secondaryColorDisabled

    # ------------------------------------------------------------------
    # Tooltip
    # ------------------------------------------------------------------

    def toolTipBackgroundColor(self) -> QColor:
        return self._theme.secondaryColor

    def toolTipBorderColor(self) -> QColor:
        return self._theme.secondaryColorPressed

    def toolTipForegroundColor(self) -> QColor:
        return self._theme.secondaryColorForeground

    # ------------------------------------------------------------------
    # Scrollbar
    # ------------------------------------------------------------------

    def scrollBarGrooveColor(self, mouse: MouseState) -> QColor:
        if mouse in (MouseState.Hovered, MouseState.Pressed):
            return self._theme.semiTransparentColor4
        return self._theme.semiTransparentColorTransparent

    def scrollBarHandleColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Hovered:
            return self._theme.secondaryAlternativeColorHovered
        if mouse == MouseState.Pressed:
            return self._theme.secondaryAlternativeColorPressed
        if mouse == MouseState.Disabled:
            return self._theme.semiTransparentColor1
        return self._theme.semiTransparentColor4

    def getScrollBarThickness(self, mouse: MouseState) -> int:
        if mouse in (MouseState.Hovered, MouseState.Pressed):
            return self._theme.scrollBarThicknessFull
        return self._theme.scrollBarThicknessSmall

    # ------------------------------------------------------------------
    # GroupBox
    # ------------------------------------------------------------------

    def groupBoxTitleColor(
        self, mouse: MouseState, w: object = None
    ) -> QColor:
        return self.labelForegroundColor(mouse, w)

    def groupBoxBorderColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.borderColorDisabled
        return self._theme.borderColor

    def groupBoxBackgroundColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.backgroundColorMainTransparent
        return getColorSourceOver(
            self._theme.backgroundColorMain2,
            colorWithAlphaF(
                self._theme.backgroundColorMain3,
                self._theme.backgroundColorMain3.alphaF() * 0.75,
            ),
        )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def statusColor(self, status: Status, mouse: MouseState) -> QColor:
        if status == Status.Success:
            if mouse == MouseState.Disabled:
                return self._theme.statusColorSuccessDisabled
            if mouse == MouseState.Pressed:
                return self._theme.statusColorSuccessPressed
            if mouse == MouseState.Hovered:
                return self._theme.statusColorSuccessHovered
            return self._theme.statusColorSuccess
        if status == Status.Warning:
            if mouse == MouseState.Disabled:
                return self._theme.statusColorWarningDisabled
            if mouse == MouseState.Pressed:
                return self._theme.statusColorWarningPressed
            if mouse == MouseState.Hovered:
                return self._theme.statusColorWarningHovered
            return self._theme.statusColorWarning
        if status == Status.Error:
            if mouse == MouseState.Disabled:
                return self._theme.statusColorErrorDisabled
            if mouse == MouseState.Pressed:
                return self._theme.statusColorErrorPressed
            if mouse == MouseState.Hovered:
                return self._theme.statusColorErrorHovered
            return self._theme.statusColorError
        # Default / Info
        if mouse == MouseState.Disabled:
            return self._theme.statusColorInfoDisabled
        if mouse == MouseState.Pressed:
            return self._theme.statusColorInfoPressed
        if mouse == MouseState.Hovered:
            return self._theme.statusColorInfoHovered
        return self._theme.statusColorInfo

    def statusColorForeground(
        self, status: Status, mouse: MouseState
    ) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.statusColorForegroundDisabled
        if mouse == MouseState.Pressed:
            return self._theme.statusColorForegroundPressed
        if mouse == MouseState.Hovered:
            return self._theme.statusColorForegroundHovered
        return self._theme.statusColorForeground

    def focusBorderColor(self, status: Status) -> QColor:
        if status == Status.Default:
            return self._theme.focusColor
        sc = self.statusColor(status, MouseState.Normal)
        focus_alpha = self._theme.focusColor.alpha()
        result = QColor(sc.red(), sc.green(), sc.blue(), focus_alpha)
        return result.lighter(110)

    def frameBorderColor(self) -> QColor:
        return self._theme.borderColorDisabled

    def separatorColor(self) -> QColor:
        return self._theme.borderColor

    # ------------------------------------------------------------------
    # Text role utilities
    # ------------------------------------------------------------------

    def colorForTextRole(
        self, role: TextRole, mouse: MouseState
    ) -> QColor:
        if role == TextRole.Caption:
            if mouse == MouseState.Disabled:
                return self._theme.secondaryAlternativeColorDisabled
            return self._theme.secondaryAlternativeColor
        if mouse == MouseState.Disabled:
            return self._theme.secondaryColorDisabled
        return self._theme.secondaryColor

    def pixelSizeForTextRole(self, role: TextRole) -> int:
        if role == TextRole.Caption:
            return self._theme.fontSizeS1
        if role == TextRole.H1:
            return self._theme.fontSizeH1
        if role == TextRole.H2:
            return self._theme.fontSizeH2
        if role == TextRole.H3:
            return self._theme.fontSizeH3
        if role == TextRole.H4:
            return self._theme.fontSizeH4
        if role == TextRole.H5:
            return self._theme.fontSizeH5
        return self._theme.fontSize

    def fontForTextRole(self, role: TextRole) -> QFont:
        if role == TextRole.Caption:
            return self._theme.fontCaption
        if role == TextRole.H1:
            return self._theme.fontH1
        if role == TextRole.H2:
            return self._theme.fontH2
        if role == TextRole.H3:
            return self._theme.fontH3
        if role == TextRole.H4:
            return self._theme.fontH4
        if role == TextRole.H5:
            return self._theme.fontH5
        return self._theme.fontRegular

    def paletteForTextRole(self, role: TextRole) -> QPalette:
        result = QPalette(self._theme.palette)
        text = self.colorForTextRole(role, MouseState.Normal)
        text_disabled = self.colorForTextRole(role, MouseState.Disabled)

        for cr in (
            QPalette.ColorRole.Text,
            QPalette.ColorRole.WindowText,
            QPalette.ColorRole.BrightText,
        ):
            result.setColor(QPalette.ColorGroup.All, cr, text)
            result.setColor(QPalette.ColorGroup.Disabled, cr, text_disabled)

        return result

    # ------------------------------------------------------------------
    # Switch
    # ------------------------------------------------------------------

    def switchGrooveColor(
        self, mouse: MouseState, checked: CheckState
    ) -> QColor:
        return self.checkButtonBackgroundColor(mouse, checked)

    def switchGrooveBorderColor(
        self,
        mouse: MouseState,
        focus: FocusState,
        checked: CheckState,
    ) -> QColor:
        return self.checkButtonBorderColor(mouse, focus, checked)

    def switchHandleColor(
        self, mouse: MouseState, checked: CheckState
    ) -> QColor:
        primary = checked != CheckState.NotChecked
        if mouse == MouseState.Pressed:
            return (
                self._theme.primaryColorForegroundPressed
                if primary
                else self._theme.secondaryColorPressed
            )
        if mouse == MouseState.Hovered:
            return (
                self._theme.primaryColorForegroundHovered
                if primary
                else self._theme.secondaryColorHovered
            )
        if mouse == MouseState.Disabled:
            return (
                self._theme.primaryColorForegroundDisabled
                if primary
                else self._theme.secondaryColorDisabled
            )
        return (
            self._theme.primaryColorForeground
            if primary
            else self._theme.secondaryColor
        )

    # ------------------------------------------------------------------
    # Table
    # ------------------------------------------------------------------

    def tableHeaderBgColor(
        self, mouse: MouseState, checked: CheckState
    ) -> QColor:
        if mouse == MouseState.Pressed:
            return self._theme.neutralColorHovered
        if mouse == MouseState.Hovered:
            return self._theme.neutralColor
        if mouse == MouseState.Disabled:
            return self._theme.neutralColor
        return self._theme.backgroundColorMain3

    def tableHeaderFgColor(
        self, mouse: MouseState, checked: CheckState
    ) -> QColor:
        if mouse == MouseState.Disabled:
            return self._theme.secondaryColorDisabled
        return self._theme.secondaryColor

    def tableLineColor(self) -> QColor:
        return self._theme.borderColor

    # ------------------------------------------------------------------
    # Status bar
    # ------------------------------------------------------------------

    def statusBarBackgroundColor(self) -> QColor:
        return self._theme.backgroundColorMain2

    def statusBarBorderColor(self) -> QColor:
        return self._theme.borderColor

    def statusBarSeparatorColor(self) -> QColor:
        return self._theme.secondaryColorDisabled

    # ------------------------------------------------------------------
    # Splitter
    # ------------------------------------------------------------------

    def splitterColor(self, mouse: MouseState) -> QColor:
        if mouse == MouseState.Normal:
            return self._theme.borderColor
        if mouse == MouseState.Hovered:
            return self._theme.primaryColor
        if mouse == MouseState.Pressed:
            return self._theme.primaryColorPressed
        return self._theme.borderColorTransparent
