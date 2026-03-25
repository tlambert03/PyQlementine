"""Metrics and sizing mixin for QlementineStyle."""

from __future__ import annotations

import sys

from qlementine._qt import QtCore, QtGui, QtWidgets
from qlementine._enums import CheckState, MouseState
from qlementine._radiuses import RadiusesF
from qlementine.utils._image import blurRadiusNecessarySpace
from qlementine.utils._state import (
    getActiveState,
    getAlternateState,
    getCheckState,
    getColorRole,
    getFocusState,
    getMenuItemMouseState,
    getMouseState,
    getScrollBarHandleState,
    getSelectionState,
    getToolButtonMouseState,
)
from qlementine.utils._style import getHPaddings

QStyle = QtWidgets.QStyle
QCommonStyle = QtWidgets.QCommonStyle
QAbstractItemView = QtWidgets.QAbstractItemView
QAbstractSpinBox = QtWidgets.QAbstractSpinBox
QComboBox = QtWidgets.QComboBox
QDateTimeEdit = QtWidgets.QDateTimeEdit
QDial = QtWidgets.QDial
QDialogButtonBox = QtWidgets.QDialogButtonBox
QFormLayout = QtWidgets.QFormLayout
QFrame = QtWidgets.QFrame
QGroupBox = QtWidgets.QGroupBox
QLineEdit = QtWidgets.QLineEdit
QMenu = QtWidgets.QMenu
QSlider = QtWidgets.QSlider
QTabBar = QtWidgets.QTabBar
QTabWidget = QtWidgets.QTabWidget
QToolBar = QtWidgets.QToolBar
QWizard = QtWidgets.QWizard

QColor = QtGui.QColor
QFont = QtGui.QFont
QFontMetrics = QtGui.QFontMetrics
QPalette = QtGui.QPalette

QEvent = QtCore.QEvent
QMargins = QtCore.QMargins
QPoint = QtCore.QPoint
QRect = QtCore.QRect
QSize = QtCore.QSize
Qt = QtCore.Qt

# Hardcoded constants from qpushbutton.cpp / qcombobox.cpp / qlinedit_p.cpp
hardcodedButtonSpacing = 4
hardcodedLineEditHMargin = 2

__all__ = ["QlementineStyleMetricsMixin"]


def _text_width(fm: QFontMetrics, text: str) -> int:
    """Portable text width helper."""
    return fm.horizontalAdvance(text)


class QlementineStyleMetricsMixin:
    """Mixin providing pixelMetric, styleHint, sizeFromContents, etc."""

    # ----------------------------------------------------------------
    # pixelMetric
    # ----------------------------------------------------------------

    def pixelMetric(self, m, opt=None, w=None):
        PM = QStyle.PixelMetric
        theme = self._theme

        if m == PM.PM_SmallIconSize:
            return theme.iconSize.height()
        if m == PM.PM_LargeIconSize:
            return theme.iconSizeLarge.height()
        if m == PM.PM_ButtonMargin:
            return theme.spacing
        if m == PM.PM_ButtonDefaultIndicator:
            return theme.iconSize.width()
        if m == PM.PM_MenuButtonIndicator:
            return theme.iconSize.width()
        if m in (PM.PM_ButtonShiftHorizontal, PM.PM_ButtonShiftVertical):
            return 0
        if m == PM.PM_ButtonIconSize:
            return theme.iconSize.height()
        if m == PM.PM_LineEditIconMargin:
            return theme.spacing
        if m == PM.PM_LineEditIconSize:
            return theme.iconSize.height()
        if m == PM.PM_DefaultFrameWidth:
            if isinstance(w, QLineEdit):
                return 1
            return 0
        if m == PM.PM_ComboBoxFrameWidth:
            return theme.spacing
        if m == PM.PM_SpinBoxFrameWidth:
            return theme.borderWidth
        if m == PM.PM_SliderControlThickness:
            return theme.controlHeightMedium
        if m == PM.PM_SliderThickness:
            return theme.iconSize.height()
        if m == PM.PM_SliderLength:
            return theme.iconSize.width()
        if m == PM.PM_SliderTickmarkOffset:
            return theme.sliderTickSpacing
        if m == PM.PM_SliderSpaceAvailable:
            if opt is not None:
                return opt.rect.width() - self.pixelMetric(
                    PM.PM_SliderLength, opt, w
                )
            return super().pixelMetric(m, opt, w)
        if m == PM.PM_MaximumDragDistance:
            return -1
        if m == PM.PM_TabBarTabOverlap:
            return int(theme.borderRadius)
        if m in (PM.PM_TabBarTabHSpace, PM.PM_TabBarTabVSpace):
            return 0
        if m == PM.PM_TabBarBaseHeight:
            return theme.controlHeightLarge + theme.spacing
        if m == PM.PM_TabBarBaseOverlap:
            return 0
        if m in (
            PM.PM_TabBarTabShiftHorizontal,
            PM.PM_TabBarTabShiftVertical,
        ):
            return 0
        if m == PM.PM_TabBarScrollButtonWidth:
            return theme.controlHeightLarge + int(theme.spacing * 1.5)
        if m == PM.PM_TabBarIconSize:
            return theme.iconSize.height()
        if m in (
            PM.PM_TabCloseIndicatorWidth,
            PM.PM_TabCloseIndicatorHeight,
        ):
            return theme.controlHeightMedium
        if m == PM.PM_ProgressBarChunkWidth:
            return 0
        if m == PM.PM_SplitterWidth:
            return 1
        if m == PM.PM_MenuScrollerHeight:
            return theme.controlHeightSmall
        if m in (PM.PM_MenuHMargin, PM.PM_MenuVMargin):
            border_w = 1 if isinstance(w, QMenu) else 0
            return theme.spacing // 2 + border_w
        if m == PM.PM_MenuPanelWidth:
            return blurRadiusNecessarySpace(theme.spacing)
        if m == PM.PM_MenuTearoffHeight:
            return theme.controlHeightSmall
        if m == PM.PM_SubMenuOverlap:
            return 0
        if m == PM.PM_MenuBarPanelWidth:
            return theme.borderWidth
        if m in (
            PM.PM_MenuBarItemSpacing,
            PM.PM_MenuBarVMargin,
            PM.PM_MenuBarHMargin,
        ):
            return 0
        if m in (PM.PM_IndicatorWidth, PM.PM_ExclusiveIndicatorWidth):
            return theme.iconSize.width()
        if m in (PM.PM_IndicatorHeight, PM.PM_ExclusiveIndicatorHeight):
            return theme.iconSize.height()
        if m == PM.PM_MessageBoxIconSize:
            return theme.iconSizeLarge.height()
        if m == PM.PM_ToolBarFrameWidth:
            return theme.borderWidth
        if m == PM.PM_ToolBarHandleExtent:
            return theme.spacing // 2
        if m == PM.PM_ToolBarItemSpacing:
            return theme.spacing // 2
        if m == PM.PM_ToolBarItemMargin:
            return theme.spacing
        if m == PM.PM_ToolBarSeparatorExtent:
            return theme.spacing * 2
        if m == PM.PM_ToolBarExtensionExtent:
            return theme.iconSize.height() + theme.spacing
        if m == PM.PM_ToolBarIconSize:
            return theme.iconSize.height()
        if m == PM.PM_IconViewIconSize:
            return self.pixelMetric(PM.PM_LargeIconSize, opt, w)
        if m == PM.PM_ListViewIconSize:
            return self.pixelMetric(PM.PM_SmallIconSize, opt, w)
        if m == PM.PM_HeaderDefaultSectionSizeHorizontal:
            return int(theme.controlDefaultWidth * 1.5)
        if m == PM.PM_HeaderDefaultSectionSizeVertical:
            return theme.controlHeightMedium
        if m in (PM.PM_FocusFrameVMargin, PM.PM_FocusFrameHMargin):
            return 2 * theme.focusBorderWidth
        if m == PM.PM_ToolTipLabelFrameWidth:
            return theme.spacing // 2
        if m in (
            PM.PM_RadioButtonLabelSpacing,
            PM.PM_CheckBoxLabelSpacing,
        ):
            return theme.spacing
        if m in (
            PM.PM_LayoutLeftMargin,
            PM.PM_LayoutTopMargin,
            PM.PM_LayoutRightMargin,
            PM.PM_LayoutBottomMargin,
        ):
            return theme.spacing * 2
        if m in (
            PM.PM_LayoutHorizontalSpacing,
            PM.PM_LayoutVerticalSpacing,
        ):
            return theme.spacing
        if m == PM.PM_TextCursorWidth:
            return 1
        if m == PM.PM_ScrollBarExtent:
            return theme.scrollBarThicknessFull + theme.scrollBarMargin
        if m == PM.PM_ScrollBarSliderMin:
            return theme.controlHeightLarge
        if m == PM.PM_ScrollView_ScrollBarSpacing:
            return 0
        if m == PM.PM_ScrollView_ScrollBarOverlap:
            return 1  # True
        if m == PM.PM_TreeViewIndentation:
            return int(theme.spacing * 2.5)
        if m == PM.PM_HeaderMargin:
            return theme.spacing
        if m == PM.PM_HeaderMarkSize:
            return theme.iconSize.height()

        return super().pixelMetric(m, opt, w)

    # ----------------------------------------------------------------
    # styleHint
    # ----------------------------------------------------------------

    def styleHint(self, sh, opt=None, w=None, shret=None):
        SH = QStyle.StyleHint
        theme = self._theme

        if sh == SH.SH_EtchDisabledText:
            return False
        if sh == SH.SH_DitherDisabledText:
            return False
        if sh in (SH.SH_Widget_Animation_Duration,):
            return theme.animationDuration
        if sh == SH.SH_Workspace_FillSpaceOnMaximize:
            return True
        if sh == SH.SH_ScrollBar_MiddleClickAbsolutePosition:
            return False
        if sh == SH.SH_ScrollBar_ScrollWhenPointerLeavesControl:
            return True
        if sh == SH.SH_ScrollBar_LeftClickAbsolutePosition:
            return True
        if sh == SH.SH_ScrollBar_ContextMenu:
            return False
        if sh == SH.SH_ScrollBar_RollBetweenButtons:
            return False
        if sh == SH.SH_ScrollView_FrameOnlyAroundContents:
            return False
        if sh == SH.SH_ScrollBar_Transient:
            return True
        if sh == SH.SH_TabBar_SelectMouseType:
            return int(QEvent.Type.MouseButtonPress)
        if sh == SH.SH_TabBar_Alignment:
            return int(Qt.AlignmentFlag.AlignLeft)
        if sh == SH.SH_TabBar_ElideMode:
            return Qt.TextElideMode.ElideNone.value
        if sh == SH.SH_TabBar_CloseButtonPosition:
            return QTabBar.ButtonPosition.RightSide.value
        if sh == SH.SH_TabBar_ChangeCurrentDelay:
            return 500
        if sh == SH.SH_TabBar_PreferNoArrows:
            return False
        if sh == SH.SH_TabWidget_DefaultTabPosition:
            return QTabWidget.TabPosition.North.value
        if sh == SH.SH_Slider_SnapToValue:
            return True
        if sh == SH.SH_Slider_SloppyKeyEvents:
            return False
        if sh == SH.SH_Slider_StopMouseOverSlider:
            return True
        if sh == SH.SH_Slider_AbsoluteSetButtons:
            return Qt.MouseButton.LeftButton.value
        if sh == SH.SH_Slider_PageSetButtons:
            return Qt.MouseButton.LeftButton.value
        if sh == SH.SH_ProgressDialog_CenterCancelButton:
            return False
        if sh == SH.SH_ProgressDialog_TextLabelAlignment:
            return int(Qt.AlignmentFlag.AlignLeft)
        if sh == SH.SH_PrintDialog_RightAlignButtons:
            return True
        if sh == SH.SH_FontDialog_SelectAssociatedText:
            return False
        if sh == SH.SH_DialogButtonBox_ButtonsHaveIcons:
            return False
        if sh == SH.SH_MessageBox_TextInteractionFlags:
            return (
                Qt.TextInteractionFlag.LinksAccessibleByKeyboard
                | Qt.TextInteractionFlag.LinksAccessibleByMouse
            ).value
        if sh == SH.SH_MessageBox_CenterButtons:
            return False
        if sh == SH.SH_Menu_AllowActiveAndDisabled:
            return False
        if sh == SH.SH_Menu_SpaceActivatesItem:
            return True
        if sh == SH.SH_Menu_SubMenuPopupDelay:
            return 300
        if sh == SH.SH_Menu_MouseTracking:
            return True
        if sh == SH.SH_Menu_Scrollable:
            return True
        if sh == SH.SH_Menu_FillScreenWithScroll:
            return True
        if sh == SH.SH_Menu_KeyboardSearch:
            return True
        if sh == SH.SH_Menu_SelectionWrap:
            return True
        if sh == SH.SH_Menu_FlashTriggeredItem:
            return True
        if sh == SH.SH_Menu_FadeOutOnHide:
            return True
        if sh == SH.SH_Menu_SupportsSections:
            return False
        if sh == SH.SH_MenuBar_MouseTracking:
            return True
        if sh == SH.SH_MenuBar_AltKeyNavigation:
            return True
        if sh == SH.SH_DrawMenuBarSeparator:
            return True
        if sh == SH.SH_MainWindow_SpaceBelowMenuBar:
            return False
        if sh == SH.SH_ComboBox_ListMouseTracking:
            return True
        if sh == SH.SH_ComboBox_Popup:
            return True
        if sh == SH.SH_ComboBox_PopupFrameStyle:
            return int(QFrame.Shape.StyledPanel) | int(
                QFrame.Shadow.Plain
            )
        if hasattr(SH, "SH_ComboBox_UseNativePopup"):
            if sh == SH.SH_ComboBox_UseNativePopup:
                return False
        if sh == SH.SH_ComboBox_AllowWheelScrolling:
            return False
        if sh == SH.SH_TitleBar_ShowToolTipsOnButtons:
            return True
        if sh == SH.SH_BlinkCursorWhenTextSelected:
            return True
        if sh == SH.SH_GroupBox_TextLabelVerticalAlignment:
            return int(Qt.AlignmentFlag.AlignVCenter)
        if sh == SH.SH_GroupBox_TextLabelColor:
            v = theme.secondaryColor.rgba() & 0xFFFFFFFF
            return v - (1 << 32) if v >= (1 << 31) else v
        if sh == SH.SH_Table_GridLineColor:
            v = self.tableLineColor().rgba() & 0xFFFFFFFF
            return v - (1 << 32) if v >= (1 << 31) else v
        if sh == SH.SH_Header_ArrowAlignment:
            return int(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )
        if sh == SH.SH_SpinBox_AnimateButton:
            return True
        if sh == SH.SH_SpinBox_KeyPressAutoRepeatRate:
            return 75
        if sh == SH.SH_SpinBox_ClickAutoRepeatRate:
            return 75
        if sh == SH.SH_SpinBox_ButtonsInsideFrame:
            return False
        if sh == SH.SH_SpinBox_StepModifier:
            return Qt.KeyboardModifier.ControlModifier.value
        if sh == SH.SH_SpinBox_ClickAutoRepeatThreshold:
            return 500
        if sh == SH.SH_SpinControls_DisableOnBounds:
            return True
        if sh == SH.SH_ToolBox_SelectedPageTitleBold:
            return True
        if sh == SH.SH_Button_FocusPolicy:
            return int(Qt.FocusPolicy.TabFocus)
        if sh == SH.SH_FocusFrame_Mask:
            if w is not None and shret is not None:
                try:
                    fbw = theme.focusBorderWidth
                    wr = w.rect()
                    extended = wr.adjusted(-fbw, -fbw, fbw, fbw)
                    shret.region = QtGui.QRegion(extended)
                    return 1
                except Exception:
                    pass
            return 0
        if sh == SH.SH_ItemView_ChangeHighlightOnFocus:
            return True
        if sh == SH.SH_ItemView_EllipsisLocation:
            return int(Qt.AlignmentFlag.AlignTrailing)
        if sh == SH.SH_ItemView_ShowDecorationSelected:
            return True
        if sh == SH.SH_ItemView_ActivateItemOnSingleClick:
            return True
        if sh == SH.SH_ItemView_MovementWithoutUpdatingSelection:
            return True
        if sh == SH.SH_ItemView_ArrowKeysNavigateIntoChildren:
            return True
        if sh == SH.SH_ItemView_PaintAlternatingRowColorsForEmptyArea:
            return True
        if sh == SH.SH_ItemView_DrawDelegateFrame:
            return False
        if sh == SH.SH_ItemView_ScrollMode:
            return QAbstractItemView.ScrollMode.ScrollPerPixel.value
        if sh == SH.SH_LineEdit_PasswordCharacter:
            return 0x2022  # Bullet
        if sh == SH.SH_LineEdit_PasswordMaskDelay:
            return 0
        if sh == SH.SH_FocusFrame_AboveWidget:
            return True
        if sh == SH.SH_ToolBar_Movable:
            return False
        if sh == SH.SH_ToolButtonStyle:
            return Qt.ToolButtonStyle.ToolButtonIconOnly.value
        if sh == SH.SH_FormLayoutFieldGrowthPolicy:
            return (
                QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow.value
            )
        if sh == SH.SH_FormLayoutFormAlignment:
            return int(Qt.AlignmentFlag.AlignLeft)
        if sh == SH.SH_FormLayoutLabelAlignment:
            return int(Qt.AlignmentFlag.AlignLeft)
        if sh == SH.SH_FormLayoutWrapPolicy:
            return QFormLayout.RowWrapPolicy.WrapLongRows.value
        if sh == SH.SH_ToolTip_WakeUpDelay:
            return 700
        if sh == SH.SH_ToolTip_FallAsleepDelay:
            return 2500
        if sh == SH.SH_ToolTipLabel_Opacity:
            return 255
        if sh == SH.SH_Splitter_OpaqueResize:
            return True
        if sh == SH.SH_RequestSoftwareInputPanel:
            return 1  # RSIP_OnMouseClick

        return super().styleHint(sh, opt, w, shret)

    # ----------------------------------------------------------------
    # sizeFromContents
    # ----------------------------------------------------------------

    def sizeFromContents(self, ct, opt, s, w=None):
        CT = QStyle.ContentsType
        theme = self._theme
        PM = QStyle.PixelMetric

        if ct == CT.CT_PushButton:
            optB = opt
            if not isinstance(
                optB, QtWidgets.QStyleOptionButton
            ):
                return super().sizeFromContents(ct, opt, s, w)

            hasIcon = not optB.icon.isNull()
            hasText = bool(optB.text)
            hasMenu = bool(
                optB.features
                & QtWidgets.QStyleOptionButton.ButtonFeature.HasMenu
            )

            contentWidth = 0
            if hasText:
                contentWidth += _text_width(optB.fontMetrics, optB.text)
            if hasIcon:
                contentWidth += optB.iconSize.width()
                if hasText:
                    contentWidth += theme.spacing
            if hasMenu:
                contentWidth += optB.iconSize.width() + theme.spacing

            padding = self.pixelMetric(PM.PM_ButtonMargin, opt, w)
            pL, pR = getHPaddings(hasIcon, hasText, hasMenu, padding)
            defaultH = theme.controlHeightLarge
            rw = max(defaultH, contentWidth + pL + pR)
            rh = max(defaultH, s.height() + padding)

            if w is not None:
                maxSz = w.maximumSize()
                QMAX = 16777215
                if maxSz.width() != QMAX and maxSz.width() > -1:
                    rw = min(rw, maxSz.width())
                if maxSz.height() != QMAX and maxSz.height() > -1:
                    rh = min(rh, maxSz.height())

            return QSize(rw, rh)

        if ct in (CT.CT_CheckBox, CT.CT_RadioButton):
            optB = opt
            if not isinstance(
                optB, QtWidgets.QStyleOptionButton
            ):
                return super().sizeFromContents(ct, opt, s, w)

            actual = QSize(s)
            if not optB.icon.isNull():
                actual.setWidth(
                    actual.width() - hardcodedButtonSpacing
                )
                if not optB.text:
                    actual.setWidth(0)
                else:
                    actual.setWidth(actual.width() + theme.spacing)

            indicatorSize = self.pixelMetric(PM.PM_IndicatorWidth, opt, w)
            indicatorSpacing = self.pixelMetric(
                PM.PM_CheckBoxLabelSpacing, opt, w
            )
            actual.setWidth(
                actual.width() + indicatorSize + indicatorSpacing
            )
            actual.setHeight(max(actual.height(), indicatorSize))

            vMargin = self.pixelMetric(PM.PM_ButtonMargin, opt, w) // 2
            rw = actual.width()
            rh = max(theme.controlHeightMedium, actual.height() + vMargin)
            return QSize(rw, rh)

        if ct == CT.CT_ToolButton:
            optTB = opt
            if not isinstance(
                optTB, QtWidgets.QStyleOptionToolButton
            ):
                return super().sizeFromContents(ct, opt, s, w)

            spacing = theme.spacing
            iconSize = optTB.iconSize

            if w is not None and w.inherits("QLineEditIconButton"):
                return QSize(theme.iconSize)
            if w is not None and w.inherits("QMenuBarExtension"):
                extent = self.pixelMetric(PM.PM_ToolBarExtensionExtent)
                return QSize(extent, extent)
            if w is not None and isinstance(
                w.parentWidget(), QTabBar
            ):
                rw = theme.controlHeightMedium + int(spacing * 1.5)
                rh = theme.controlHeightLarge + spacing
                return QSize(rw, rh)

            buttonStyle = optTB.toolButtonStyle
            hasMenu = bool(
                optTB.features
                & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.HasMenu
            )
            menuSep = bool(
                hasMenu
                and (
                    optTB.features
                    & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.MenuButtonPopup
                )
            )
            separatorW = theme.borderWidth if menuSep else 0
            menuIndicatorW = (
                separatorW + iconSize.width() + spacing // 2
                if hasMenu
                else 0
            )
            rh = (
                theme.controlHeightLarge
                if iconSize.height() < theme.controlHeightLarge
                else iconSize.height() + spacing
            )

            TBS = Qt.ToolButtonStyle
            if buttonStyle == TBS.ToolButtonTextOnly:
                textW = optTB.fontMetrics.boundingRect(
                    optTB.rect, int(Qt.AlignmentFlag.AlignCenter),
                    optTB.text,
                ).width()
                lp = spacing * 2
                rp = spacing if hasMenu else spacing * 2
                return QSize(lp + textW + rp + menuIndicatorW, rh)
            if buttonStyle == TBS.ToolButtonIconOnly:
                return QSize(
                    iconSize.width() + spacing * 2 + menuIndicatorW, rh
                )
            # TextBesideIcon / TextUnderIcon
            iconW = iconSize.width()
            textW = optTB.fontMetrics.boundingRect(
                optTB.rect, int(Qt.AlignmentFlag.AlignCenter),
                optTB.text,
            ).width()
            lp = spacing
            rp = spacing if hasMenu else spacing * 2
            return QSize(
                lp + iconW + spacing + textW + rp + menuIndicatorW, rh
            )

        if ct == CT.CT_ComboBox:
            optCB = opt
            if not isinstance(
                optCB, QtWidgets.QStyleOptionComboBox
            ):
                return super().sizeFromContents(ct, opt, s, w)

            parentW = w.parentWidget() if w else None
            ppW = parentW.parentWidget() if parentW else None
            isTabCell = isinstance(ppW, QAbstractItemView)

            rh = theme.controlHeightLarge
            rw = optCB.rect.size().width() if isTabCell else s.width()

            if not optCB.currentIcon.isNull():
                rw -= hardcodedButtonSpacing
                if not optCB.currentText:
                    rw = 0
                else:
                    rw += theme.spacing

            if not isTabCell:
                indicatorSize = theme.iconSize
                rw += theme.spacing + indicatorSize.width()
                framePadding = self.pixelMetric(
                    PM.PM_ComboBoxFrameWidth, optCB, w
                )
                hMargin = self.pixelMetric(PM.PM_ButtonMargin, opt, w)
                rw += hMargin + framePadding * 2

            return QSize(rw, rh)

        if ct == CT.CT_ProgressBar:
            optPB = opt
            if not isinstance(
                optPB, QtWidgets.QStyleOptionProgressBar
            ):
                return super().sizeFromContents(ct, opt, s, w)

            indeterminate = (
                optPB.maximum == 0 and optPB.minimum == 0
            )
            showText = not indeterminate and optPB.textVisible
            maxText = "" if indeterminate else f"{optPB.maximum}%"
            labelW = (
                optPB.fontMetrics.boundingRect(
                    optPB.rect,
                    int(Qt.AlignmentFlag.AlignRight),
                    maxText,
                ).width()
                if showText
                else 0
            )
            labelH = optPB.fontMetrics.height() if showText else 0
            spacing = theme.spacing
            barH = theme.progressBarGrooveHeight
            defaultH = theme.controlHeightMedium
            rh = min(defaultH, max(labelH, barH))
            rw = theme.controlDefaultWidth + (
                spacing + labelW if showText else 0
            )
            return QSize(rw, rh)

        if ct == CT.CT_MenuItem:
            optMI = opt
            if not isinstance(
                optMI, QtWidgets.QStyleOptionMenuItem
            ):
                return super().sizeFromContents(ct, opt, s, w)

            MIT = QtWidgets.QStyleOptionMenuItem.MenuItemType
            if optMI.menuItemType == MIT.Separator:
                h = theme.spacing + theme.borderWidth
                return QSize(h, h)

            if optMI.menuItemType in (MIT.Normal, MIT.SubMenu):
                hPadding = theme.spacing
                vPadding = theme.spacing // 2
                iconSz = theme.iconSize
                spacing = theme.spacing
                fm = optMI.fontMetrics
                text = optMI.text
                tabIdx = text.find("\t")
                label = text[:tabIdx] if tabIdx >= 0 else text
                shortcut = text[tabIdx + 1:] if tabIdx >= 0 else ""

                labelW = fm.boundingRect(
                    optMI.rect,
                    int(Qt.AlignmentFlag.AlignLeft),
                    label,
                ).width()

                hasArrow = optMI.menuItemType == MIT.SubMenu
                arrowW = (
                    spacing + iconSz.width() if hasArrow else spacing
                )

                hasShortcut = len(shortcut) > 0
                reservedW = optMI.reservedShortcutWidth
                shortcutTextW = (
                    fm.boundingRect(shortcut).width()
                    if hasShortcut
                    else 0
                )
                shortcutW = max(reservedW, shortcutTextW)

                dontShowIcons = (
                    QtCore.QCoreApplication.testAttribute(
                        Qt.ApplicationAttribute.AA_DontShowIconsInMenus
                    )
                )
                iconW = (
                    optMI.maxIconWidth + spacing
                    if not dontShowIcons and optMI.maxIconWidth > 0
                    else 0
                )

                hasCheck = (
                    optMI.menuHasCheckableItems
                    or optMI.checkType
                    != QtWidgets.QStyleOptionMenuItem.CheckType.NotCheckable
                )
                checkW = (
                    iconSz.width() + spacing if hasCheck else 0
                )

                rw = max(
                    0,
                    hPadding
                    + checkW
                    + iconW
                    + labelW
                    + shortcutW
                    + arrowW
                    + hPadding,
                )
                rh = max(
                    theme.controlHeightMedium,
                    iconSz.height() + vPadding,
                )
                return QSize(rw, rh)

            return QSize()

        if ct == CT.CT_MenuBarItem:
            hPadding = theme.spacing
            vPadding = theme.spacing // 2
            rh = max(
                theme.iconSize.height() + theme.spacing, s.height()
            )
            rw = s.width() + 2 * hPadding
            rh2 = s.height() + 2 * vPadding
            return QSize(rw, max(rh, rh2))

        if ct == CT.CT_MenuBar:
            return QSize(s)
        if ct == CT.CT_Menu:
            return QSize(s)

        if ct == CT.CT_TabBarTab:
            optTab = opt
            if not isinstance(optTab, QtWidgets.QStyleOptionTab):
                return super().sizeFromContents(ct, opt, s, w)

            spacing = theme.spacing
            rh = theme.controlHeightLarge + spacing
            rw = spacing * 2

            if (
                hasattr(optTab, "leftButtonSize")
                and not optTab.leftButtonSize.isEmpty()
            ):
                rw += optTab.leftButtonSize.width() + spacing
            if (
                hasattr(optTab, "rightButtonSize")
                and not optTab.rightButtonSize.isEmpty()
            ):
                rw += optTab.rightButtonSize.width() + spacing
            if not optTab.icon.isNull() and not optTab.iconSize.isEmpty():
                rw += optTab.iconSize.width() + spacing
            if optTab.text:
                rw += _text_width(optTab.fontMetrics, optTab.text)

            tabMax = theme.tabBarTabMaxWidth
            tabMin = theme.tabBarTabMinWidth
            if tabMin > tabMax:
                tabMin, tabMax = tabMax, tabMin
            if tabMax > 0:
                rw = min(rw, tabMax)
            if tabMin > 0:
                rw = max(rw, tabMin)

            return QSize(rw, rh)

        if ct == CT.CT_Slider:
            optSl = opt
            if isinstance(optSl, QtWidgets.QStyleOptionSlider):
                rect = optSl.rect
                if optSl.orientation == Qt.Orientation.Horizontal:
                    return QSize(
                        rect.width(), theme.controlHeightMedium
                    )
                return QSize(theme.controlHeightMedium, rect.height())

        if ct == CT.CT_LineEdit:
            if isinstance(opt, QtWidgets.QStyleOptionFrame):
                rw = s.width() - 2 * hardcodedLineEditHMargin
                rh = theme.controlHeightLarge
                if w is not None:
                    parent = w.parentWidget()
                    ppw = parent.parentWidget() if parent else None
                    if isinstance(ppw, QAbstractItemView):
                        return QSize(s)
                return QSize(rw, rh)

        if ct == CT.CT_SpinBox:
            optSB = opt
            if isinstance(optSB, QtWidgets.QStyleOptionSpinBox):
                isDTE = isinstance(w, QDateTimeEdit)
                hasButtons = (
                    optSB.buttonSymbols
                    != QAbstractSpinBox.ButtonSymbols.NoButtons
                )
                buttonW = (
                    theme.controlHeightLarge
                    if isDTE or hasButtons
                    else 0
                )
                dateTimeW = theme.iconSize.width() if isDTE else 0
                borderW = (
                    self.pixelMetric(PM.PM_SpinBoxFrameWidth, opt, w)
                    if optSB.frame
                    else 0
                )
                return QSize(
                    s.width() + buttonW + dateTimeW + 2 * borderW,
                    theme.controlHeightLarge,
                )

        if ct == CT.CT_HeaderSection:
            optH = opt
            if isinstance(optH, QtWidgets.QStyleOptionHeader):
                spacing = theme.spacing
                font = QFont(w.font()) if w else QFont()
                font.setBold(True)
                lineW = theme.borderWidth
                iconExtent = self.pixelMetric(PM.PM_SmallIconSize, opt)
                fm = QFontMetrics(font)
                textW = _text_width(fm, optH.text)
                hasIcon = not optH.icon.isNull()
                iconW = iconExtent + spacing if hasIcon else 0
                hasArrow = (
                    optH.sortIndicator
                    != QtWidgets.QStyleOptionHeader.SortIndicator.None_
                )
                arrowW = iconExtent + spacing if hasArrow else 0
                paddingH = self.pixelMetric(PM.PM_HeaderMargin)
                paddingV = paddingH // 2
                textH = fm.height()
                rw = lineW + paddingH + iconW + textW + arrowW + paddingH + lineW
                rh = lineW + paddingV + max(iconExtent, textH) + paddingV + lineW
                return QSize(rw, rh)

        if ct == CT.CT_GroupBox:
            optGB = opt
            if isinstance(optGB, QtWidgets.QStyleOptionGroupBox):
                hasTitle = bool(
                    optGB.subControls
                    & QStyle.SubControl.SC_GroupBoxLabel
                )
                hasCheckbox = bool(
                    optGB.subControls
                    & QStyle.SubControl.SC_GroupBoxCheckBox
                )
                hasFrame = not bool(
                    optGB.features
                    & QtWidgets.QStyleOptionFrame.FrameFeature.Flat
                )
                fm = QFontMetrics(theme.fontH5)
                labelH = (
                    max(theme.controlHeightMedium, fm.height())
                    if hasTitle
                    else 0
                )
                labelW = fm.boundingRect(
                    optGB.rect,
                    int(Qt.AlignmentFlag.AlignLeft),
                    optGB.text,
                ).width()
                checkBoxSize = theme.iconSize
                titleBottomSpacing = (
                    theme.spacing // 2
                    if hasFrame and (hasTitle or hasCheckbox)
                    else 0
                )
                titleH = (
                    max(labelH, checkBoxSize.height())
                    if hasTitle or hasCheckbox
                    else 0
                )
                spacing = theme.spacing
                titleW = checkBoxSize.width() + spacing + labelW
                leftPadding = (
                    spacing if hasTitle or hasCheckbox else 0
                )
                rw = max(s.width() + leftPadding, titleW)
                rh = titleH + titleBottomSpacing + s.height()
                return QSize(rw, rh)

        if ct == CT.CT_ItemViewItem:
            optItem = opt
            if isinstance(
                optItem, QtWidgets.QStyleOptionViewItem
            ):
                features = optItem.features
                spacing = theme.spacing
                hPadding = spacing
                VIF = QtWidgets.QStyleOptionViewItem.ViewItemFeature
                hasIcon = bool(
                    features & VIF.HasDecoration
                ) and not optItem.icon.isNull()
                iconSz = (
                    optItem.decorationSize
                    if hasIcon
                    else QSize(0, 0)
                )
                hasText = bool(
                    features & VIF.HasDisplay
                ) and bool(optItem.text)
                textH = optItem.fontMetrics.height() if hasText else 0
                hasCheck = bool(features & VIF.HasCheckIndicator)
                checkSz = (
                    theme.iconSize if hasCheck else QSize(0, 0)
                )
                font = QFont(w.font()) if w else QFont()
                fm = QFontMetrics(font)
                textW = _text_width(fm, optItem.text)
                rw = (
                    textW
                    + 2 * hPadding
                    + (iconSz.width() + spacing if iconSz.width() > 0 else 0)
                    + (
                        checkSz.width() + spacing
                        if checkSz.width() > 0
                        else 0
                    )
                )
                defaultH = theme.controlHeightLarge
                rh = max(
                    iconSz.height() + spacing,
                    textH + spacing,
                    defaultH,
                )
                return QSize(rw, rh)

        return super().sizeFromContents(ct, opt, s, w)

    # ----------------------------------------------------------------
    # subElementRect
    # ----------------------------------------------------------------

    def subElementRect(self, se, opt, w=None):
        SE = QStyle.SubElement
        PM = QStyle.PixelMetric
        theme = self._theme
        rect = opt.rect

        if se == SE.SE_PushButtonContents:
            optB = opt
            if isinstance(optB, QtWidgets.QStyleOptionButton):
                hasIcon = not optB.icon.isNull()
                hasText = bool(optB.text)
                hasMenu = bool(
                    optB.features
                    & QtWidgets.QStyleOptionButton.ButtonFeature.HasMenu
                )
                padding = self.pixelMetric(PM.PM_ButtonMargin)
                pL, pR = getHPaddings(
                    hasIcon, hasText, hasMenu, padding
                )
                if pL + pR >= rect.width():
                    return QRect(rect)
                return rect.adjusted(pL, 0, -pR, 0)
            return QRect(rect)

        if se == SE.SE_PushButtonBevel:
            return QRect(rect)

        if se == SE.SE_PushButtonFocusRect:
            bw = theme.focusBorderWidth
            return rect.translated(bw * 2, bw * 2).adjusted(
                -bw, -bw, bw, bw
            )

        if se in (
            SE.SE_RadioButtonIndicator,
            SE.SE_CheckBoxIndicator,
        ):
            sz = self.pixelMetric(PM.PM_IndicatorWidth)
            y = rect.y() + (rect.height() - sz) // 2
            return QRect(rect.x(), y, sz, sz)

        if se in (
            SE.SE_RadioButtonFocusRect,
            SE.SE_CheckBoxFocusRect,
        ):
            bw = theme.focusBorderWidth
            checkR = self.subElementRect(
                SE.SE_CheckBoxIndicator, opt, w
            ).adjusted(-bw, -bw, bw, bw)
            dx = self.pixelMetric(PM.PM_FocusFrameHMargin, opt, w)
            dy = self.pixelMetric(PM.PM_FocusFrameVMargin, opt, w)
            return checkR.translated(dx, dy)

        if se in (
            SE.SE_RadioButtonContents,
            SE.SE_CheckBoxContents,
        ):
            indSz = self.pixelMetric(PM.PM_IndicatorWidth)
            sp = self.pixelMetric(PM.PM_CheckBoxLabelSpacing)
            return rect.adjusted(indSz + sp, 0, 0, 0)

        if se in (
            SE.SE_CheckBoxClickRect,
            SE.SE_RadioButtonClickRect,
        ):
            return QRect(rect)

        if se == SE.SE_ComboBoxFocusRect:
            bw = theme.focusBorderWidth
            return rect.translated(bw * 2, bw * 2).adjusted(
                -bw, -bw, bw, bw
            )

        if se == SE.SE_SliderFocusRect:
            optSl = opt
            if isinstance(optSl, QtWidgets.QStyleOptionSlider):
                isDial = isinstance(w, QDial)
                cc = (
                    QStyle.ComplexControl.CC_Dial
                    if isDial
                    else QStyle.ComplexControl.CC_Slider
                )
                sc = (
                    QStyle.SubControl.SC_DialHandle
                    if isDial
                    else QStyle.SubControl.SC_SliderHandle
                )
                handleR = self.subControlRect(cc, optSl, sc, w)
                dx = self.pixelMetric(PM.PM_FocusFrameHMargin, opt, w)
                dy = self.pixelMetric(PM.PM_FocusFrameVMargin, opt, w)
                hm = dx // 2
                vm = dy // 2
                return handleR.translated(dx, dy).adjusted(
                    -hm, -vm, hm, vm
                )
            return QRect(rect)

        if se in (
            SE.SE_ProgressBarContents,
            SE.SE_ProgressBarGroove,
        ):
            optPB = opt
            if isinstance(
                optPB, QtWidgets.QStyleOptionProgressBar
            ):
                showText = optPB.textVisible
                labelW = (
                    optPB.fontMetrics.boundingRect(
                        optPB.rect,
                        int(Qt.AlignmentFlag.AlignRight),
                        "100%",
                    ).width()
                    if showText
                    else 0
                )
                sp = theme.spacing if showText else 0
                barW = rect.width() - labelW - sp
                barH = theme.progressBarGrooveHeight
                barY = rect.y() + (rect.height() - barH) // 2
                return QRect(rect.x(), barY, barW, barH)
            return QRect()

        if se == SE.SE_ProgressBarLabel:
            optPB = opt
            if isinstance(
                optPB, QtWidgets.QStyleOptionProgressBar
            ):
                showText = optPB.textVisible
                labelW = (
                    optPB.fontMetrics.boundingRect(
                        optPB.rect,
                        int(Qt.AlignmentFlag.AlignRight),
                        "100%",
                    ).width()
                    if showText
                    else 0
                )
                labelH = (
                    optPB.fontMetrics.height() if showText else 0
                )
                labelX = rect.right() - labelW
                labelY = rect.y() + (rect.height() - labelH) // 2
                return QRect(labelX, labelY, labelW, labelH)
            return QRect()

        if se == SE.SE_HeaderLabel:
            optH = opt
            if isinstance(optH, QtWidgets.QStyleOptionHeader):
                paddingH = self.pixelMetric(PM.PM_HeaderMargin)
                return QRect(
                    rect.x() + paddingH,
                    rect.y(),
                    rect.width() - paddingH * 2,
                    rect.height(),
                )
            return QRect()

        if se == SE.SE_HeaderArrow:
            optH = opt
            if isinstance(optH, QtWidgets.QStyleOptionHeader):
                hasArrow = (
                    optH.sortIndicator
                    != QtWidgets.QStyleOptionHeader.SortIndicator.None_
                )
                if hasArrow:
                    paddingH = self.pixelMetric(PM.PM_HeaderMargin)
                    iconExt = self.pixelMetric(PM.PM_SmallIconSize)
                    arrowX = rect.x() + rect.width() - paddingH - iconExt
                    arrowY = rect.y() + (rect.height() - iconExt) // 2
                    return QRect(arrowX, arrowY, iconExt, iconExt)

        if se == SE.SE_LineEditContents:
            optF = opt
            if isinstance(optF, QtWidgets.QStyleOptionFrame):
                bw = optF.lineWidth
                hm = theme.spacing // 2
                return optF.rect.adjusted(
                    bw + hm, bw, -bw - hm, -bw
                )
            return QRect()

        if se == SE.SE_TabBarTearIndicatorLeft:
            shadowW = theme.spacing * 3
            return QRect(rect.x(), rect.y(), shadowW, rect.height())

        if se == SE.SE_TabBarTearIndicatorRight:
            scrollBtnW = (
                theme.controlHeightMedium * 2 + theme.spacing * 3
            )
            shadowW = theme.spacing * 3
            x = rect.x() + rect.width() - shadowW - scrollBtnW
            return QRect(x, rect.y(), shadowW + scrollBtnW, rect.height())

        if se == SE.SE_TabBarTabLeftButton:
            optTab = opt
            if isinstance(optTab, QtWidgets.QStyleOptionTab):
                btnSz = optTab.leftButtonSize
                padTop = theme.tabBarPaddingTop
                sp = theme.spacing
                x = rect.x() + sp
                y = (
                    rect.y()
                    + padTop
                    + (rect.height() - padTop - btnSz.height()) // 2
                )
                return QRect(x, y, btnSz.width(), btnSz.height())
            return QRect()

        if se == SE.SE_TabBarTabRightButton:
            optTab = opt
            if isinstance(optTab, QtWidgets.QStyleOptionTab):
                btnSz = optTab.rightButtonSize
                sp = theme.spacing
                padTop = theme.tabBarPaddingTop
                x = rect.x() + rect.width() - sp - btnSz.width()
                y = (
                    rect.y()
                    + padTop
                    + (rect.height() - padTop - btnSz.height()) // 2
                )
                return QRect(x, y, btnSz.width(), btnSz.height())
            return QRect()

        if se == SE.SE_TabBarTabText:
            optTab = opt
            if isinstance(optTab, QtWidgets.QStyleOptionTab):
                sp = theme.spacing
                lbw = (
                    optTab.leftButtonSize.width() + sp
                    if optTab.leftButtonSize.width() > 0
                    else 0
                )
                rbw = (
                    optTab.rightButtonSize.width() + sp
                    if optTab.rightButtonSize.width() > 0
                    else 0
                )
                x = rect.x() + sp + lbw
                y = rect.y() + theme.tabBarPaddingTop
                width = rect.width() - lbw - rbw - sp * 2
                height = rect.height() - theme.tabBarPaddingTop
                return QRect(x, y, width, height)
            return QRect()

        if se == SE.SE_TabBarScrollLeftButton:
            sp = theme.spacing
            rw = theme.controlHeightMedium + int(sp * 1.5)
            rh = theme.controlHeightLarge + sp
            x = rect.x() + rect.width() - 2 * rw
            return QRect(x, rect.y(), rw, rh)

        if se == SE.SE_TabBarScrollRightButton:
            sp = theme.spacing
            rw = theme.controlHeightMedium + int(sp * 1.5)
            rh = theme.controlHeightLarge + sp
            x = rect.x() + rect.width() - rw + sp // 2
            return QRect(x, rect.y(), rw, rh)

        return super().subElementRect(se, opt, w)

    # ----------------------------------------------------------------
    # subControlRect
    # ----------------------------------------------------------------

    def subControlRect(self, cc, opt, sc, w=None):
        CC = QStyle.ComplexControl
        SC = QStyle.SubControl
        PM = QStyle.PixelMetric
        theme = self._theme

        if cc == CC.CC_SpinBox:
            optSB = opt
            if isinstance(optSB, QtWidgets.QStyleOptionSpinBox):
                totalR = optSB.rect
                noButtons = (
                    optSB.buttonSymbols
                    == QAbstractSpinBox.ButtonSymbols.NoButtons
                )
                if sc == SC.SC_SpinBoxUp:
                    if noButtons:
                        return QRect()
                    iconDim = self.pixelMetric(PM.PM_ButtonIconSize)
                    bw = iconDim + 2 * theme.borderWidth
                    bh = totalR.height() // 2
                    bx = totalR.right() - bw
                    by = totalR.top()
                    return QRect(bx, by, bw, bh)
                if sc == SC.SC_SpinBoxDown:
                    if noButtons:
                        return QRect()
                    iconDim = self.pixelMetric(PM.PM_ButtonIconSize)
                    bw = iconDim + 2 * theme.borderWidth
                    bh = totalR.height() // 2
                    bx = totalR.right() - bw
                    by = totalR.bottom() + 1 - bh
                    return QRect(bx, by, bw, bh)
                if sc == SC.SC_SpinBoxEditField:
                    if noButtons:
                        return QRect(totalR)
                    iconDim = self.pixelMetric(PM.PM_ButtonIconSize)
                    bw = iconDim + 2 * theme.borderWidth + 1
                    return QRect(
                        totalR.x(),
                        totalR.y(),
                        totalR.width() - bw,
                        totalR.height(),
                    )
                if sc == SC.SC_SpinBoxFrame:
                    return QRect(opt.rect)
            return QRect()

        if cc == CC.CC_ComboBox:
            optCB = opt
            if isinstance(optCB, QtWidgets.QStyleOptionComboBox):
                if sc == SC.SC_ComboBoxArrow:
                    indicatorSz = theme.iconSize
                    hPad = theme.spacing
                    bw = indicatorSz.width() + hPad * 2
                    bh = optCB.rect.height()
                    bx = optCB.rect.x() + optCB.rect.width() - bw
                    by = optCB.rect.y()
                    return QRect(bx, by, bw, bh)
                if sc == SC.SC_ComboBoxEditField:
                    if optCB.editable:
                        hasIcon = not optCB.currentIcon.isNull()
                        indicatorSz = theme.iconSize
                        sp = theme.spacing
                        shiftX = int(sp * 2.5) if hasIcon else 0
                        indicatorBtnW = sp * 2 + indicatorSz.width()
                        editW = (
                            optCB.rect.width() - indicatorBtnW + shiftX
                        )
                        return QRect(
                            optCB.rect.x() - shiftX,
                            optCB.rect.y(),
                            editW,
                            optCB.rect.height(),
                        )
                    return QRect()
                if sc == SC.SC_ComboBoxFrame:
                    frameH = theme.controlHeightLarge
                    frameW = optCB.rect.width()
                    frameX = optCB.rect.x()
                    frameY = (
                        optCB.rect.y()
                        + (optCB.rect.height() - frameH) // 2
                    )
                    return QRect(frameX, frameY, frameW, frameH)
                if sc == SC.SC_ComboBoxListBoxPopup:
                    cMH = self.pixelMetric(PM.PM_MenuHMargin)
                    cMV = self.pixelMetric(PM.PM_MenuVMargin)
                    shadowW = theme.spacing
                    borderW = theme.borderWidth
                    rw = max(
                        opt.rect.width(),
                        w.width() if w else opt.rect.width(),
                    )
                    rh = opt.rect.height() + 12
                    rx = opt.rect.x() - shadowW - borderW - cMH
                    ry = opt.rect.y() - shadowW - borderW - cMV // 2
                    return QRect(rx, ry, rw, rh)
            return QRect()

        if cc == CC.CC_ScrollBar:
            optSB = opt
            if isinstance(optSB, QtWidgets.QStyleOptionSlider):
                horizontal = (
                    optSB.orientation == Qt.Orientation.Horizontal
                )
                r = optSB.rect
                margin = theme.scrollBarMargin

                if sc == SC.SC_ScrollBarAddPage:
                    total = r.width() if horizontal else r.height()
                    hc = QStyle.sliderPositionFromValue(
                        optSB.minimum,
                        optSB.maximum,
                        optSB.sliderPosition,
                        total,
                        optSB.upsideDown,
                    )
                    if horizontal:
                        return QRect(r.x(), r.y(), hc, r.height())
                    return QRect(r.x(), r.y(), r.width(), hc)

                if sc == SC.SC_ScrollBarSubPage:
                    total = r.width() if horizontal else r.height()
                    hc = QStyle.sliderPositionFromValue(
                        optSB.minimum,
                        optSB.maximum,
                        optSB.sliderPosition,
                        total,
                        optSB.upsideDown,
                    )
                    if horizontal:
                        return QRect(
                            r.x() + hc,
                            r.y(),
                            r.width() - hc,
                            r.height(),
                        )
                    return QRect(
                        r.x(),
                        r.y() + hc,
                        r.width(),
                        r.height() - hc,
                    )

                if sc == SC.SC_ScrollBarSlider:
                    if optSB.maximum != optSB.minimum:
                        rng = optSB.maximum - optSB.minimum
                        maxLen = (
                            (r.width() if horizontal else r.height())
                            - 2 * margin
                        )
                        minLen = self.pixelMetric(
                            PM.PM_ScrollBarSliderMin, optSB, w
                        )
                        if minLen > maxLen:
                            maxLen, minLen = minLen, maxLen
                        length = max(
                            0.0,
                            (optSB.pageStep * maxLen)
                            / (rng + optSB.pageStep),
                        )
                        handleLen = max(
                            minLen, min(int(length), maxLen)
                        )
                        handleStart = QStyle.sliderPositionFromValue(
                            optSB.minimum,
                            optSB.maximum,
                            optSB.sliderPosition,
                            maxLen - handleLen,
                            optSB.upsideDown,
                        )
                        if horizontal:
                            return QRect(
                                r.x() + margin + handleStart,
                                r.y(),
                                handleLen,
                                r.height() - margin,
                            )
                        return QRect(
                            r.x(),
                            r.y() + margin + handleStart,
                            r.width() - margin,
                            handleLen,
                        )
                    return QRect(r)

                if sc == SC.SC_ScrollBarGroove:
                    if horizontal:
                        return QRect(
                            r.x() + margin,
                            r.y(),
                            r.width() - 2 * margin,
                            r.height() - margin,
                        )
                    return QRect(
                        r.x(),
                        r.y() + margin,
                        r.width() - margin,
                        r.height() - 2 * margin,
                    )

                # SC_ScrollBarAddLine etc - not handled
                return QRect()
            return QRect()

        if cc == CC.CC_Slider:
            optSl = opt
            if isinstance(optSl, QtWidgets.QStyleOptionSlider):
                if sc == SC.SC_SliderGroove:
                    grooveW = opt.rect.width()
                    grooveH = theme.sliderGrooveHeight
                    grooveX = opt.rect.x()
                    grooveY = (
                        opt.rect.y()
                        + (opt.rect.height() - grooveH) // 2
                    )
                    return QRect(grooveX, grooveY, grooveW, grooveH)
                if sc == SC.SC_SliderHandle:
                    handleW = self.pixelMetric(PM.PM_SliderLength)
                    handleH = self.pixelMetric(PM.PM_SliderThickness)
                    handleY = (
                        opt.rect.y()
                        + (opt.rect.height() - handleH) // 2
                    )
                    mn = optSl.minimum
                    mx = optSl.maximum
                    pos = float(optSl.sliderPosition)
                    if mx != mn:
                        ratio = (pos - mn) / (mx - mn)
                    else:
                        ratio = 0.0
                    handleX = opt.rect.x() + int(
                        ratio * (opt.rect.width() - handleW)
                    )
                    return QRect(handleX, handleY, handleW, handleH)
                if sc == SC.SC_SliderTickmarks:
                    tp = optSl.tickPosition
                    if tp == QSlider.TickPosition.TicksAbove:
                        grooveR = self.subControlRect(
                            cc, opt, SC.SC_SliderGroove, w
                        )
                        handleThick = self.pixelMetric(PM.PM_SliderLength)
                        tickOff = self.pixelMetric(
                            PM.PM_SliderTickmarkOffset
                        )
                        tmX = opt.rect.x() + handleThick // 2
                        tmH = theme.sliderTickSize
                        tmY = grooveR.top() - tickOff - tmH
                        tmW = grooveR.width() - handleThick
                        return QRect(tmX, tmY, tmW, tmH)
                return QRect()
            return QRect()

        if cc == CC.CC_ToolButton:
            optTB = opt
            if isinstance(
                optTB, QtWidgets.QStyleOptionToolButton
            ):
                r = optTB.rect
                hasMenu = bool(
                    optTB.features
                    & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.HasMenu
                )
                menuSep = bool(
                    optTB.features
                    & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.MenuButtonPopup
                )
                iconSz = optTB.iconSize
                sepW = theme.borderWidth
                sp = theme.spacing
                menuBtnW = (
                    (
                        sepW + iconSz.width() + sp // 2
                        if menuSep
                        else iconSz.width()
                    )
                    if hasMenu
                    else 0
                )
                buttonW = r.width() - menuBtnW
                if sc == SC.SC_ToolButton:
                    return QRect(r.x(), r.y(), buttonW, r.height())
                if sc == SC.SC_ToolButtonMenu:
                    return QRect(
                        r.x() + r.width() - menuBtnW,
                        r.y(),
                        menuBtnW,
                        r.height(),
                    )
                return QRect()
            return QRect()

        if cc == CC.CC_TitleBar:
            # All sub-controls return empty for now
            return QRect()

        if cc == CC.CC_Dial:
            optDl = opt
            if isinstance(optDl, QtWidgets.QStyleOptionSlider):
                totalR = optDl.rect
                hasTicks = bool(
                    optDl.subControls & SC.SC_DialTickmarks
                )
                if sc in (SC.SC_DialHandle, SC.SC_DialGroove):
                    tickSpace = (
                        theme.dialTickLength + theme.dialTickSpacing
                        if hasTicks
                        else 0
                    )
                    minDim = max(
                        0,
                        min(totalR.width(), totalR.height())
                        - tickSpace * 2,
                    )
                    dx = totalR.x() + (totalR.width() - minDim) // 2
                    dy = totalR.y() + (totalR.height() - minDim) // 2
                    return QRect(dx, dy, minDim, minDim)
                if sc == SC.SC_DialTickmarks:
                    if not hasTicks:
                        return QRect()
                    minDim = max(
                        0,
                        min(totalR.width(), totalR.height()),
                    )
                    tx = totalR.x() + (totalR.width() - minDim) // 2
                    ty = totalR.y() + (totalR.height() - minDim) // 2
                    return QRect(tx, ty, minDim, minDim)
                return QRect()
            return QRect()

        if cc == CC.CC_GroupBox:
            optGB = opt
            if isinstance(
                optGB, QtWidgets.QStyleOptionGroupBox
            ):
                r = optGB.rect
                hasTitle = bool(
                    optGB.subControls & SC.SC_GroupBoxLabel
                )
                hasCheckbox = bool(
                    optGB.subControls & SC.SC_GroupBoxCheckBox
                )
                hasFrame = not bool(
                    optGB.features
                    & QtWidgets.QStyleOptionFrame.FrameFeature.Flat
                )
                labelH = (
                    max(
                        theme.controlHeightMedium,
                        QFontMetrics(theme.fontH5).height(),
                    )
                    if hasTitle
                    else 0
                )
                titleBottomSp = (
                    theme.spacing // 2
                    if hasFrame and (hasTitle or hasCheckbox)
                    else 0
                )
                checkBoxSz = (
                    theme.iconSize
                    if hasCheckbox
                    else QSize(0, 0)
                )
                titleH = (
                    max(labelH, checkBoxSz.height())
                    if hasTitle or hasCheckbox
                    else 0
                )
                leftPadding = (
                    theme.spacing
                    if hasTitle or hasCheckbox
                    else 0
                )

                if sc == SC.SC_GroupBoxCheckBox:
                    if hasCheckbox:
                        x = r.x()
                        y = r.y() + (titleH - checkBoxSz.height()) // 2
                        return QRect(
                            QPoint(x, y), checkBoxSz
                        )
                    return QRect()

                if sc == SC.SC_GroupBoxLabel:
                    if hasTitle:
                        sp = theme.spacing if hasCheckbox else 0
                        x = r.x() + checkBoxSz.width() + sp
                        y = r.y()
                        lw = r.width() - checkBoxSz.width() - sp
                        return QRect(x, y, lw, titleH)
                    return QRect()

                if sc in (
                    SC.SC_GroupBoxContents,
                    SC.SC_GroupBoxFrame,
                ):
                    x = r.x() + leftPadding
                    y = r.y() + titleH + titleBottomSp
                    rw = r.width() - leftPadding
                    rh = r.height() - titleH - titleBottomSp
                    return QRect(x, y, rw, rh)

            return QRect()

        if cc == CC.CC_MdiControls:
            return QRect()

        return super().subControlRect(cc, opt, sc, w)

    # ----------------------------------------------------------------
    # hitTestComplexControl
    # ----------------------------------------------------------------

    def hitTestComplexControl(self, cc, opt, pos, w=None):
        CC = QStyle.ComplexControl
        SC = QStyle.SubControl

        if cc == CC.CC_SpinBox:
            optSB = opt
            if isinstance(optSB, QtWidgets.QStyleOptionSpinBox):
                noButtons = (
                    optSB.buttonSymbols
                    == QAbstractSpinBox.ButtonSymbols.NoButtons
                )
                if not noButtons:
                    if optSB.subControls & SC.SC_SpinBoxUp:
                        r = self.subControlRect(
                            cc, opt, SC.SC_SpinBoxUp, w
                        )
                        if r.contains(pos):
                            return SC.SC_SpinBoxUp
                    if optSB.subControls & SC.SC_SpinBoxDown:
                        r = self.subControlRect(
                            cc, opt, SC.SC_SpinBoxDown, w
                        )
                        if r.contains(pos):
                            return SC.SC_SpinBoxDown

                r = self.subControlRect(
                    cc, opt, SC.SC_SpinBoxEditField, w
                )
                if r.contains(pos):
                    return SC.SC_SpinBoxEditField
                r = self.subControlRect(
                    cc, opt, SC.SC_SpinBoxFrame, w
                )
                if r.contains(pos):
                    return SC.SC_SpinBoxFrame
            return SC.SC_None

        if cc == CC.CC_ComboBox:
            r = self.subControlRect(
                cc, opt, SC.SC_ComboBoxEditField, w
            )
            if r.isValid() and r.contains(pos):
                return SC.SC_ComboBoxEditField
            r = self.subControlRect(
                cc, opt, SC.SC_ComboBoxArrow, w
            )
            if r.isValid() and r.contains(pos):
                return SC.SC_ComboBoxArrow
            r = self.subControlRect(
                cc, opt, SC.SC_ComboBoxFrame, w
            )
            if r.isValid() and r.contains(pos):
                return SC.SC_ComboBoxFrame
            return SC.SC_None

        if cc == CC.CC_ScrollBar:
            r = self.subControlRect(
                cc, opt, SC.SC_ScrollBarSlider, w
            )
            if r.isValid() and r.contains(pos):
                return SC.SC_ScrollBarSlider
            for sub in (
                SC.SC_ScrollBarAddLine,
                SC.SC_ScrollBarSubLine,
                SC.SC_ScrollBarAddPage,
                SC.SC_ScrollBarSubPage,
                SC.SC_ScrollBarFirst,
                SC.SC_ScrollBarLast,
                SC.SC_ScrollBarGroove,
            ):
                r = self.subControlRect(cc, opt, sub, w)
                if r.isValid() and r.contains(pos):
                    return sub
            return SC.SC_None

        if cc == CC.CC_Slider:
            optSl = opt
            if isinstance(optSl, QtWidgets.QStyleOptionSlider):
                handleR = self.subControlRect(
                    cc, optSl, SC.SC_SliderHandle, w
                )
                if handleR.isValid() and handleR.contains(pos):
                    return SC.SC_SliderHandle
                grooveR = self.subControlRect(
                    cc, optSl, SC.SC_SliderGroove, w
                )
                clickR = (
                    grooveR
                    if not handleR.isValid()
                    else QRect(
                        grooveR.x(),
                        handleR.y(),
                        grooveR.width(),
                        handleR.height(),
                    )
                )
                if clickR.isValid() and clickR.contains(pos):
                    return SC.SC_SliderGroove
            return SC.SC_None

        if cc == CC.CC_ToolButton:
            r = self.subControlRect(cc, opt, SC.SC_ToolButton, w)
            if r.isValid() and r.contains(pos):
                return SC.SC_ToolButton
            r = self.subControlRect(
                cc, opt, SC.SC_ToolButtonMenu, w
            )
            if r.isValid() and r.contains(pos):
                return SC.SC_ToolButtonMenu
            return SC.SC_None

        if cc == CC.CC_Dial:
            for sub in (
                SC.SC_DialHandle,
                SC.SC_DialGroove,
                SC.SC_DialTickmarks,
            ):
                r = self.subControlRect(cc, opt, sub, w)
                if r.isValid() and r.contains(pos):
                    return sub
            return SC.SC_None

        if cc == CC.CC_GroupBox:
            checkR = self.subControlRect(
                cc, opt, SC.SC_GroupBoxCheckBox, w
            )
            labelR = self.subControlRect(
                cc, opt, SC.SC_GroupBoxLabel, w
            )
            titleR = checkR.united(labelR)
            if titleR.isValid() and titleR.contains(pos):
                return SC.SC_GroupBoxCheckBox
            contR = self.subControlRect(
                cc, opt, SC.SC_GroupBoxContents, w
            )
            if contR.isValid() and contR.contains(pos):
                return SC.SC_GroupBoxContents
            frameR = self.subControlRect(
                cc, opt, SC.SC_GroupBoxFrame, w
            )
            if frameR.isValid() and frameR.contains(pos):
                return SC.SC_GroupBoxFrame
            return SC.SC_None

        return super().hitTestComplexControl(cc, opt, pos, w)

    # ----------------------------------------------------------------
    # layoutSpacing
    # ----------------------------------------------------------------

    def layoutSpacing(self, c1, c2, o, opt=None, w=None):
        return self._theme.spacing
