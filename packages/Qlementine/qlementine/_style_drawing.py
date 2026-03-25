"""Drawing mixin for QlementineStyle."""

from __future__ import annotations

import math
import sys

from qlementine._qt import QtCore, QtGui, QtWidgets
from qlementine._enums import (
    ActiveState,
    AutoIconColor,
    CheckState,
    ColorRole,
    FocusState,
    MouseState,
    SelectionState,
)
from qlementine._radiuses import RadiusesF
from qlementine.utils._image import (
    getDropShadowPixmap,
    getTintedPixmap,
)
from qlementine.utils._primitive import (
    QLEMENTINE_PI,
    drawArrowDown,
    drawArrowUp,
    drawCheckButton,
    drawCloseIndicator,
    drawComboBoxIndicator,
    drawDial,
    drawDialTickMarks,
    drawGripIndicator,
    drawIcon,
    drawMenuSeparator,
    drawProgressBarValueRect,
    drawRadioButton,
    drawRoundedRect,
    drawRoundedRectBorder,
    drawSliderTickMarks,
    drawSpinBoxArrowIndicator,
    drawSubMenuIndicator,
    drawTab,
    drawTreeViewIndicator,
    getMenuIndicatorPath,
    getMenuLabelAndShortcut,
    getMultipleRadiusesRectPath,
    getPixelRatio,
    getPixmap,
    getTickInterval,
)
from qlementine.utils._state import (
    getActiveState,
    getAlternateState,
    getCheckState,
    getColorRole,
    getFocusState,
    getMenuItemMouseState,
    getMouseState,
    getPaletteColorGroup,
    getScrollBarHandleState,
    getSelectionState,
    getSliderHandleState,
    getTabItemMouseState,
    getToolButtonMouseState,
)
from qlementine.utils._style import (
    getHPaddings,
    shouldHaveBoldFont,
    shouldHaveExternalFocusFrame,
    shouldHaveHoverEvents,
    shouldHaveMouseTracking,
    shouldHaveTabFocus,
    shouldNotBeVerticallyCompressed,
    shouldNotHaveWheelEvents,
)
from qlementine.utils._color import getColorSourceOver
from qlementine.utils._font import textWidth

QApplication = QtWidgets.QApplication
QCommonStyle = QtWidgets.QCommonStyle
QStyle = QtWidgets.QStyle
QAbstractButton = QtWidgets.QAbstractButton
QAbstractItemView = QtWidgets.QAbstractItemView
QAbstractSpinBox = QtWidgets.QAbstractSpinBox
QCheckBox = QtWidgets.QCheckBox
QComboBox = QtWidgets.QComboBox
QDateTimeEdit = QtWidgets.QDateTimeEdit
QDial = QtWidgets.QDial
QDialogButtonBox = QtWidgets.QDialogButtonBox
QFocusFrame = QtWidgets.QFocusFrame
QFormLayout = QtWidgets.QFormLayout
QFrame = QtWidgets.QFrame
QGroupBox = QtWidgets.QGroupBox
QLabel = QtWidgets.QLabel
QLineEdit = QtWidgets.QLineEdit
QListView = QtWidgets.QListView
QMainWindow = QtWidgets.QMainWindow
QMenu = QtWidgets.QMenu
QMenuBar = QtWidgets.QMenuBar
QMessageBox = QtWidgets.QMessageBox
QPlainTextEdit = QtWidgets.QPlainTextEdit
QPushButton = QtWidgets.QPushButton
QRadioButton = QtWidgets.QRadioButton
QScrollArea = QtWidgets.QScrollArea
QScrollBar = QtWidgets.QScrollBar
QSizePolicy = QtWidgets.QSizePolicy
QSlider = QtWidgets.QSlider
QSpinBox = QtWidgets.QSpinBox
QTabBar = QtWidgets.QTabBar
QTabWidget = QtWidgets.QTabWidget
QTableView = QtWidgets.QTableView
QTextEdit = QtWidgets.QTextEdit
QToolBar = QtWidgets.QToolBar
QToolButton = QtWidgets.QToolButton
QTreeView = QtWidgets.QTreeView
QWidget = QtWidgets.QWidget

QBrush = QtGui.QBrush
QColor = QtGui.QColor
QCursor = QtGui.QCursor
QFont = QtGui.QFont
QFontMetrics = QtGui.QFontMetrics
QGuiApplication = QtGui.QGuiApplication
QIcon = QtGui.QIcon
QLinearGradient = QtGui.QLinearGradient
QPainter = QtGui.QPainter
QPainterPath = QtGui.QPainterPath
QPalette = QtGui.QPalette
QPen = QtGui.QPen
QPixmap = QtGui.QPixmap
QRegion = QtGui.QRegion

QEvent = QtCore.QEvent
QMargins = QtCore.QMargins
QMarginsF = QtCore.QMarginsF
QPoint = QtCore.QPoint
QPointF = QtCore.QPointF
QRect = QtCore.QRect
QRectF = QtCore.QRectF
QSize = QtCore.QSize
Qt = QtCore.Qt

# Hardcoded constants from Qt sources
hardcodedButtonSpacing = 4
hardcodedLineEditHMargin = 2
iconPenWidth = 1.01

__all__ = ["QlementineStyleDrawingMixin"]

PE = QStyle.PrimitiveElement
CE = QStyle.ControlElement
CC = QStyle.ComplexControl
SE = QStyle.SubElement
SC = QStyle.SubControl
PM = QStyle.PixelMetric
SH = QStyle.StyleHint
State = QStyle.StateFlag


def _areTabBarScrollButtonsVisible(tabBar: QTabBar) -> bool:
    """Check if a QTabBar's scroll buttons are visible."""
    if not tabBar.usesScrollButtons():
        return False
    for tb in tabBar.findChildren(QToolButton):
        if tb.arrowType() == Qt.ArrowType.LeftArrow:
            return tb.isVisible()
    return False


def _tabExtraPadding(theme, optTab) -> QMargins:
    """Return extra padding around a tab for nice curve ends."""
    spacing = theme.spacing
    paddingTop = spacing // 2

    TabPos = QtWidgets.QStyleOptionTab.TabPosition
    SelPos = QtWidgets.QStyleOptionTab.SelectedPosition

    isFirst = optTab.position in (TabPos.OnlyOneTab, TabPos.Beginning)
    isLast = optTab.position in (TabPos.OnlyOneTab, TabPos.End)

    notBesideSelected = (
        optTab.selectedPosition == SelPos.NotAdjacent
    )
    onlyOneTab = optTab.position == TabPos.OnlyOneTab
    isMovedTab = notBesideSelected and onlyOneTab

    paddingLeft = spacing if (isMovedTab or isFirst) else 0
    paddingRight = spacing if (isMovedTab or isLast) else 0
    paddingBottom = 0
    return QMargins(paddingLeft, paddingTop, paddingRight, paddingBottom)


class QlementineStyleDrawingMixin:
    """Mixin providing drawing methods: drawPrimitive, drawControl, etc."""

    # ================================================================
    # standardPalette
    # ================================================================

    def standardPalette(self) -> QPalette:
        return QPalette(self._theme.palette)

    # ================================================================
    # polish / unpolish
    # ================================================================

    def polish(self, arg):
        if isinstance(arg, QPalette):
            arg = super().polish(arg)
            pal = self._theme.palette
            for group in (
                QPalette.ColorGroup.Active,
                QPalette.ColorGroup.Inactive,
                QPalette.ColorGroup.Disabled,
            ):
                for role_val in range(
                    QPalette.ColorRole.NColorRoles.value
                ):
                    cr = QPalette.ColorRole(role_val)
                    arg.setColor(group, cr, pal.color(group, cr))
            return arg

        elif isinstance(arg, QApplication):
            super().polish(arg)
            arg.setFont(self._theme.fontRegular)
            QtCore.QCoreApplication.setAttribute(
                Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False
            )
            QtCore.QCoreApplication.setAttribute(
                Qt.ApplicationAttribute.AA_DontShowShortcutsInContextMenus,
                False,
            )
            QApplication.setEffectEnabled(
                Qt.UIEffect.UI_AnimateMenu, True
            )
            QApplication.setEffectEnabled(
                Qt.UIEffect.UI_FadeMenu, True
            )
            QApplication.setEffectEnabled(
                Qt.UIEffect.UI_AnimateCombo, True
            )
            QApplication.setEffectEnabled(
                Qt.UIEffect.UI_AnimateTooltip, True
            )
            QApplication.setEffectEnabled(
                Qt.UIEffect.UI_FadeTooltip, True
            )

        elif isinstance(arg, QWidget):
            w = arg
            super().polish(w)

            # Tooltip: translucent background
            if sys.platform != "win32" and w.inherits("QTipLabel"):
                w.setBackgroundRole(QPalette.ColorRole.NoRole)
                w.setAutoFillBackground(False)
                w.setAttribute(
                    Qt.WidgetAttribute.WA_TranslucentBackground, True
                )
                w.setAttribute(
                    Qt.WidgetAttribute.WA_NoSystemBackground, True
                )
                w.setAttribute(
                    Qt.WidgetAttribute.WA_OpaquePaintEvent, False
                )

            # Bold font for buttons
            if shouldHaveBoldFont(w):
                font = QFont(w.font())
                font.setBold(True)
                w.setFont(font)

            # Enable hover state
            if shouldHaveHoverEvents(w):
                w.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
                w.setAttribute(
                    Qt.WidgetAttribute.WA_OpaquePaintEvent, False
                )
            if shouldHaveMouseTracking(w):
                w.setMouseTracking(True)

            # Tab focus for buttons
            if shouldHaveTabFocus(w):
                w.setFocusPolicy(Qt.FocusPolicy.TabFocus)

            # Menus: transparent background, frameless
            if isinstance(w, QMenu):
                w.setBackgroundRole(QPalette.ColorRole.NoRole)
                w.setAutoFillBackground(False)
                w.setAttribute(
                    Qt.WidgetAttribute.WA_TranslucentBackground, True
                )
                w.setAttribute(
                    Qt.WidgetAttribute.WA_OpaquePaintEvent, False
                )
                w.setAttribute(
                    Qt.WidgetAttribute.WA_NoSystemBackground, True
                )
                w.setWindowFlag(
                    Qt.WindowType.FramelessWindowHint, True
                )
                w.setWindowFlag(
                    Qt.WindowType.NoDropShadowWindowHint, True
                )

            # ComboBox popup container setup
            if isinstance(w, QAbstractItemView):
                popup = w.parentWidget()
                if popup and popup.inherits(
                    "QComboBoxPrivateContainer"
                ):
                    popup.setAttribute(
                        Qt.WidgetAttribute.WA_TranslucentBackground,
                        True,
                    )
                    popup.setAttribute(
                        Qt.WidgetAttribute.WA_OpaquePaintEvent, False
                    )
                    popup.setAttribute(
                        Qt.WidgetAttribute.WA_NoSystemBackground, True
                    )
                    popup.setWindowFlag(
                        Qt.WindowType.FramelessWindowHint, True
                    )
                    popup.setWindowFlag(
                        Qt.WindowType.NoDropShadowWindowHint, True
                    )
                    shadowW = self._theme.spacing
                    borderW = self._theme.borderWidth
                    margin = shadowW + borderW
                    layout = popup.layout()
                    if layout:
                        layout.setContentsMargins(
                            margin, margin, margin, margin
                        )
                    w.viewport().setAutoFillBackground(False)

            # Prevent vertical compression in form layouts
            if shouldNotBeVerticallyCompressed(w):
                minH = w.minimumHeight()
                if minH in (0, 1):
                    hintH = w.sizeHint().height()
                    if hintH > 0:
                        w.setMinimumHeight(hintH)

            # Disable wheel focus for spinboxes, comboboxes, sliders
            if shouldNotHaveWheelEvents(w):
                if w.focusPolicy() == Qt.FocusPolicy.WheelFocus:
                    w.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            # QScrollArea: no focus
            if isinstance(w, QScrollArea):
                w.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # QSlider: horizontal by default
            if isinstance(w, QSlider):
                w.setOrientation(Qt.Orientation.Horizontal)

    def unpolish(self, arg):
        if isinstance(arg, QApplication):
            super().unpolish(arg)
        elif isinstance(arg, QWidget):
            super().unpolish(arg)
            if shouldHaveHoverEvents(arg):
                arg.setAttribute(
                    Qt.WidgetAttribute.WA_Hover, False
                )
                arg.setAttribute(
                    Qt.WidgetAttribute.WA_OpaquePaintEvent, True
                )
            if shouldHaveMouseTracking(arg):
                arg.setMouseTracking(False)

    # ================================================================
    # drawPrimitive
    # ================================================================

    def drawPrimitive(self, pe, opt, p, w=None):
        theme = self._theme

        if pe == PE.PE_Frame:
            return

        if pe == PE.PE_FrameDefaultButton:
            return super().drawPrimitive(pe, opt, p, w)

        if pe == PE.PE_FrameFocusRect:
            optFocus = opt
            if optFocus.rect.isEmpty():
                return
            borderRadiuses = RadiusesF()
            if hasattr(optFocus, "radiuses"):
                borderRadiuses = optFocus.radiuses
            focused = bool(
                optFocus.state & State.State_HasFocus
            )
            borderW = theme.focusBorderWidth if focused else 0.0
            if borderW >= 0.1:
                status = self.widgetStatus(w)
                borderColor = self.focusBorderColor(status)
                drawRoundedRectBorder(
                    p,
                    QRectF(optFocus.rect),
                    borderColor,
                    borderW,
                    borderRadiuses + borderW
                    if isinstance(borderRadiuses, RadiusesF)
                    else borderRadiuses + borderW,
                )
            return

        if pe == PE.PE_FrameGroupBox:
            if isinstance(
                opt, QtWidgets.QStyleOptionFrame
            ):
                mouse = getMouseState(opt.state)
                bgColor = self.groupBoxBackgroundColor(mouse)
                borderColor = self.groupBoxBorderColor(mouse)
                borderW = theme.borderWidth
                drawRoundedRect(
                    p, opt.rect, bgColor, theme.borderRadius
                )
                drawRoundedRectBorder(
                    p,
                    opt.rect,
                    borderColor,
                    borderW,
                    theme.borderRadius,
                )
            return

        if pe == PE.PE_FrameLineEdit:
            return super().drawPrimitive(pe, opt, p, w)

        if pe == PE.PE_FrameMenu:
            return  # Let PE_PanelMenu do the drawing.

        if pe == PE.PE_FrameStatusBarItem:
            rect = opt.rect
            penColor = theme.borderColor
            penW = theme.borderWidth
            p1 = QPoint(
                rect.x() + 1 + penW, rect.y() + rect.x()
            )
            p2 = QPoint(
                rect.x() + 1 + penW,
                rect.y() + rect.height(),
            )
            p.setPen(
                QPen(
                    penColor,
                    penW,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.FlatCap,
                    Qt.PenJoinStyle.MiterJoin,
                )
            )
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawLine(p1, p2)
            return

        if pe == PE.PE_FrameTabWidget:
            tabWidget = (
                w
                if isinstance(w, QTabWidget)
                else None
            )
            documentMode = (
                tabWidget.documentMode() if tabWidget else False
            )
            tabBar = (
                tabWidget.tabBar() if tabWidget else None
            )
            if not documentMode and tabBar:
                mouse = getMouseState(opt.state)
                radius = theme.borderRadius * 1.5
                borderColor = self.tabBarBackgroundColor(mouse)
                borderW = theme.borderWidth
                drawRoundedRectBorder(
                    p,
                    opt.rect.adjusted(0, -borderW, 0, 0),
                    borderColor,
                    borderW,
                    RadiusesF(0.0, 0.0, radius, radius),
                )
                tabBarH = (
                    theme.controlHeightLarge + theme.spacing
                )
                tabBarOpt = QtWidgets.QStyleOptionTabBarBase()
                tabBarOpt.initFrom(tabBar)
                tabBarOpt.rect = QRect(
                    0, 0, opt.rect.width(), tabBarH
                )
                tabBarOpt.shape = tabBar.shape()
                tabBarOpt.documentMode = documentMode
                self.drawPrimitive(
                    PE.PE_FrameTabBarBase, tabBarOpt, p, tabBar
                )
            return

        if pe == PE.PE_FrameTabBarBase:
            if isinstance(
                opt, QtWidgets.QStyleOptionTabBarBase
            ):
                mouse = getMouseState(opt.state)
                bgColor = self.tabBarBackgroundColor(mouse)
                if opt.documentMode:
                    p.fillRect(opt.rect, bgColor)
                else:
                    radius = theme.borderRadius * 1.5
                    drawRoundedRect(
                        p,
                        opt.rect,
                        bgColor,
                        RadiusesF(radius, radius, 0.0, 0.0),
                    )
            return

        if pe == PE.PE_FrameButtonBevel:
            optButton = opt
            if isinstance(
                opt, QtWidgets.QStyleOptionButton
            ):
                isDefault = bool(
                    optButton.features
                    & QtWidgets.QStyleOptionButton.ButtonFeature.DefaultButton
                )
                isFlat = bool(
                    optButton.features
                    & QtWidgets.QStyleOptionButton.ButtonFeature.Flat
                )
                mouse = (
                    getToolButtonMouseState(opt.state)
                    if isFlat
                    else getMouseState(opt.state)
                )
                role = getColorRole(opt.state, isDefault)
                bgColor = (
                    self.toolButtonBackgroundColor(mouse, role)
                    if isFlat
                    else self.buttonBackgroundColor(
                        mouse, role, w
                    )
                )
                radiuses = (
                    optButton.radiuses
                    if hasattr(optButton, "radiuses")
                    else RadiusesF(theme.borderRadius)
                )
                drawRoundedRect(
                    p, optButton.rect, bgColor, radiuses
                )
            return

        if pe == PE.PE_PanelButtonCommand:
            return super().drawPrimitive(pe, opt, p, w)

        if pe == PE.PE_PanelButtonBevel:
            return super().drawPrimitive(pe, opt, p, w)

        if pe == PE.PE_FrameButtonTool:
            return

        if pe == PE.PE_PanelButtonTool:
            if isinstance(
                opt, QtWidgets.QStyleOptionToolButton
            ):
                rect = opt.rect
                parentWidget = (
                    w.parentWidget() if w else None
                )
                isTabBarScrollButton = (
                    isinstance(parentWidget, QTabBar)
                    and opt.arrowType != Qt.ArrowType.NoArrow
                )
                isMenuBarExtButton = isinstance(
                    parentWidget, QMenuBar
                )
                radius = (
                    theme.menuBarItemBorderRadius
                    if isMenuBarExtButton
                    else theme.borderRadius
                )

                hasMenu = bool(
                    opt.features
                    & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.HasMenu
                )
                menuOnSep = hasMenu and bool(
                    opt.features
                    & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.MenuButtonPopup
                )

                if isTabBarScrollButton:
                    buttonRadiuses = RadiusesF(rect.height())
                elif menuOnSep:
                    buttonRadiuses = RadiusesF(
                        radius, 0.0, 0.0, radius
                    )
                else:
                    buttonRadiuses = RadiusesF(radius)

                buttonState = opt.state
                isExtBtn = (
                    w
                    and w.objectName()
                    == "qt_toolbar_ext_button"
                )
                if isExtBtn:
                    buttonState = buttonState & ~State.State_On
                mouse = getMouseState(buttonState)
                role = getColorRole(buttonState, False)

                bgColor = (
                    self.tabBarScrollButtonBackgroundColor(
                        mouse
                    )
                    if isTabBarScrollButton
                    else self.toolButtonBackgroundColor(
                        mouse, role
                    )
                )
                drawRoundedRect(
                    p, rect, bgColor, buttonRadiuses
                )
            return

        if pe == PE.PE_PanelMenuBar:
            bgColor = self.menuBarBackgroundColor()
            borderColor = self.menuBarBorderColor()
            lineW = theme.borderWidth
            x1 = float(opt.rect.x())
            x2 = float(x1 + opt.rect.width())
            y = (
                opt.rect.y()
                + opt.rect.height()
                - lineW / 2.0
            )
            p.fillRect(opt.rect, bgColor)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(
                QPen(
                    borderColor,
                    lineW,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.FlatCap,
                )
            )
            p.drawLine(
                QPointF(x1, lineW / 2.0),
                QPointF(x2, lineW / 2.0),
            )
            p.drawLine(QPointF(x1, y), QPointF(x2, y))
            return

        if pe == PE.PE_PanelToolBar:
            if isinstance(
                opt, QtWidgets.QStyleOptionToolBar
            ):
                bgColor = self.toolBarBackgroundColor()
                rect = opt.rect
                p.fillRect(rect, bgColor)

                lineW = theme.borderWidth
                lineColor = self.toolBarBorderColor()
                p.setPen(
                    QPen(
                        lineColor,
                        lineW,
                        Qt.PenStyle.SolidLine,
                        Qt.PenCapStyle.FlatCap,
                    )
                )
                p.setBrush(Qt.BrushStyle.NoBrush)

                toolBar = (
                    w
                    if isinstance(w, QToolBar)
                    else None
                )
                if toolBar:
                    orientation = toolBar.orientation()
                    areas = toolBar.allowedAreas()
                    if orientation == Qt.Orientation.Horizontal:
                        if areas & Qt.ToolBarArea.TopToolBarArea:
                            y1 = (
                                rect.y()
                                + rect.height()
                                - lineW / 2.0
                            )
                            p.drawLine(
                                QPointF(rect.x(), y1),
                                QPointF(
                                    rect.x() + rect.width(),
                                    y1,
                                ),
                            )
                        if areas & Qt.ToolBarArea.BottomToolBarArea:
                            y1 = rect.y() + lineW / 2.0
                            p.drawLine(
                                QPointF(rect.x(), y1),
                                QPointF(
                                    rect.x() + rect.width(),
                                    y1,
                                ),
                            )
                    elif orientation == Qt.Orientation.Vertical:
                        if areas & Qt.ToolBarArea.LeftToolBarArea:
                            x1 = (
                                rect.x()
                                + rect.width()
                                - lineW / 2.0
                            )
                            p.drawLine(
                                QPointF(x1, rect.y()),
                                QPointF(
                                    x1,
                                    rect.y() + rect.height(),
                                ),
                            )
                        if areas & Qt.ToolBarArea.RightToolBarArea:
                            x1 = rect.x() + lineW / 2.0
                            p.drawLine(
                                QPointF(x1, rect.y()),
                                QPointF(
                                    x1,
                                    rect.y() + rect.height(),
                                ),
                            )
            return

        if pe == PE.PE_PanelLineEdit:
            if isinstance(
                opt, QtWidgets.QStyleOptionFrame
            ):
                parentWidget = (
                    w.parentWidget() if w else None
                )
                parentParent = (
                    parentWidget.parentWidget()
                    if parentWidget
                    else None
                )
                isTabCellEditor = parentParent and isinstance(
                    parentParent.parentWidget()
                    if parentParent
                    else None,
                    QAbstractItemView,
                )
                isComboBoxLineEdit = isinstance(
                    parentWidget, QComboBox
                )
                isPlainTextEdit = isinstance(
                    w, QPlainTextEdit
                )
                isPlainQPlainTextEdit = (
                    isPlainTextEdit
                    and w.frameShadow()
                    == QFrame.Shadow.Plain
                )
                isPlainLineEdit = (
                    not isComboBoxLineEdit
                    and not isPlainTextEdit
                    and opt.lineWidth == 0
                )
                isPlain = (
                    isPlainQPlainTextEdit or isPlainLineEdit
                )

                radiusF = float(theme.borderRadius)
                radiuses = RadiusesF(radiusF)
                if (
                    isPlain
                    or isTabCellEditor
                    or (
                        w
                        and w.metaObject().className()
                        == "QExpandingLineEdit"
                    )
                ):
                    radiuses = RadiusesF(0.0)
                elif isinstance(
                    parentWidget, QAbstractSpinBox
                ) or isinstance(parentWidget, QComboBox):
                    radiuses = RadiusesF(
                        radiusF, 0.0, 0.0, radiusF
                    )

                # Fix: State_Sunken is always true for QLineEdit
                fixedState = (opt.state & ~State.State_Sunken)

                rect = opt.rect
                status = self.widgetStatus(w)
                mouse = getMouseState(fixedState)
                focus = getFocusState(opt.state)
                bgColor = self.textFieldBackgroundColor(
                    mouse, status
                )
                borderColor = self.textFieldBorderColor(
                    mouse, focus, status
                )
                borderW = theme.borderWidth

                drawRoundedRect(p, rect, bgColor, radiuses)
                if not isPlainLineEdit:
                    drawRoundedRectBorder(
                        p,
                        rect,
                        borderColor,
                        borderW,
                        radiuses,
                    )
                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing, False
                )
            return

        if pe in (
            PE.PE_IndicatorArrowDown,
            PE.PE_IndicatorArrowUp,
            PE.PE_IndicatorArrowLeft,
            PE.PE_IndicatorArrowRight,
        ):
            return super().drawPrimitive(pe, opt, p, w)

        if pe == PE.PE_IndicatorBranch:
            if isinstance(
                opt, QtWidgets.QStyleOptionViewItem
            ):
                if opt.state & State.State_Children:
                    isOpen = bool(
                        opt.state & State.State_Open
                    )
                    indicatorSize = theme.iconSize
                    hShift = theme.spacing // 4
                    indicatorRect = QRect(
                        QPoint(
                            hShift
                            + opt.rect.x()
                            + (
                                opt.rect.width()
                                - indicatorSize.width()
                            )
                            // 2,
                            opt.rect.y()
                            + (
                                opt.rect.height()
                                - indicatorSize.height()
                            )
                            // 2,
                        ),
                        indicatorSize,
                    )
                    mouse = getMouseState(opt.state)
                    selection = getSelectionState(opt.state)
                    active = getActiveState(opt.state)
                    widgetHasFocus = (
                        w.hasFocus() if w else False
                    )
                    focus = (
                        FocusState.Focused
                        if widgetHasFocus
                        and selection
                        == SelectionState.Selected
                        else FocusState.NotFocused
                    )
                    fgColor = self.listItemForegroundColor(
                        mouse, selection, focus, active
                    )
                    p.setRenderHint(
                        QPainter.RenderHint.Antialiasing, True
                    )
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(
                        QPen(
                            fgColor,
                            iconPenWidth,
                            Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap,
                        )
                    )
                    drawTreeViewIndicator(
                        indicatorRect, p, isOpen
                    )
            return

        if pe == PE.PE_IndicatorItemViewItemCheck:
            if isinstance(
                opt, QtWidgets.QStyleOptionViewItem
            ):
                checkState = getCheckState(opt.checkState)
                progress = (
                    0.0
                    if checkState == CheckState.NotChecked
                    else 1.0
                )
                mouse = getMouseState(opt.state)
                selected = getSelectionState(opt.state)
                active = getActiveState(opt.state)
                fgColor = (
                    self.listItemCheckButtonForegroundColor(
                        mouse, checkState, selected, active
                    )
                )
                bgColor = (
                    self.listItemCheckButtonBackgroundColor(
                        mouse, checkState, selected, active
                    )
                )
                brdColor = (
                    self.listItemCheckButtonBorderColor(
                        mouse, checkState, selected, active
                    )
                )
                radius = theme.checkBoxBorderRadius
                borderW = theme.borderWidth
                indicatorSize = max(
                    opt.rect.width(), opt.rect.height()
                )
                indicatorX = opt.rect.x() + (
                    opt.rect.width() - indicatorSize
                )
                indicatorY = opt.rect.y() + (
                    opt.rect.height() - indicatorSize
                )
                indicatorRect = QRect(
                    indicatorX,
                    indicatorY,
                    indicatorSize,
                    indicatorSize,
                )
                drawCheckButton(
                    p,
                    indicatorRect,
                    radius,
                    bgColor,
                    brdColor,
                    fgColor,
                    borderW,
                    progress,
                    checkState,
                )
            return

        if pe in (
            PE.PE_IndicatorCheckBox,
            PE.PE_IndicatorRadioButton,
        ):
            if isinstance(
                opt, QtWidgets.QStyleOptionButton
            ):
                checkState = getCheckState(opt.state)
                mouse = getMouseState(opt.state)
                bgColor = self.checkButtonBackgroundColor(
                    mouse, checkState
                )
                fgColor = self.checkButtonForegroundColor(
                    mouse, checkState
                )
                borderColor = self.checkButtonBorderColor(
                    mouse,
                    getFocusState(opt.state),
                    checkState,
                )
                borderW = theme.borderWidth

                indicatorSize = max(
                    opt.rect.width(), opt.rect.height()
                )
                indicatorX = opt.rect.x() + (
                    opt.rect.width() - indicatorSize
                )
                indicatorY = opt.rect.y() + (
                    opt.rect.height() - indicatorSize
                )
                indicatorRect = QRect(
                    indicatorX,
                    indicatorY,
                    indicatorSize,
                    indicatorSize,
                )

                progress = (
                    0.0
                    if checkState == CheckState.NotChecked
                    else 1.0
                )

                isRadio = pe == PE.PE_IndicatorRadioButton
                if isRadio:
                    drawRadioButton(
                        p,
                        indicatorRect,
                        bgColor,
                        borderColor,
                        fgColor,
                        borderW,
                        progress,
                    )
                else:
                    radius = theme.checkBoxBorderRadius
                    drawCheckButton(
                        p,
                        indicatorRect,
                        radius,
                        bgColor,
                        borderColor,
                        fgColor,
                        borderW,
                        progress,
                        checkState,
                    )
            return

        if pe == PE.PE_IndicatorHeaderArrow:
            if isinstance(
                opt, QtWidgets.QStyleOptionHeader
            ):
                SortInd = (
                    QtWidgets.QStyleOptionHeader.SortIndicator
                )
                indicatorType = opt.sortIndicator
                mouse = getMouseState(opt.state)
                checked = getCheckState(opt.state)
                fgColor = self.tableHeaderFgColor(
                    mouse, checked
                )
                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing, True
                )
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(
                    QPen(
                        fgColor,
                        1.001,
                        Qt.PenStyle.SolidLine,
                        Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin,
                    )
                )
                if indicatorType == SortInd.SortDown:
                    drawArrowUp(opt.rect, p)
                elif indicatorType == SortInd.SortUp:
                    drawArrowDown(opt.rect, p)
            return

        if pe == PE.PE_IndicatorToolBarSeparator:
            rect = opt.rect
            color = self.toolBarSeparatorColor()
            horizontal = bool(
                opt.state & State.State_Horizontal
            )
            lineW = theme.borderWidth
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(
                QPen(
                    color,
                    lineW,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.FlatCap,
                )
            )
            if horizontal:
                x = rect.x() + (rect.width() - lineW) / 2.0
                y1 = float(rect.y())
                y2 = float(rect.y() + rect.height())
                p.drawLine(QPointF(x, y1), QPointF(x, y2))
            else:
                y = rect.y() + (rect.height() - lineW) / 2.0
                x1 = float(rect.x())
                x2 = float(rect.x() + rect.width())
                p.drawLine(QPointF(x1, y), QPointF(x2, y))
            return

        if pe == PE.PE_PanelTipLabel:
            bgColor = self.toolTipBackgroundColor()
            borderColor = self.toolTipBorderColor()
            borderW = theme.borderWidth
            p.setRenderHint(
                QPainter.RenderHint.Antialiasing, True
            )
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(bgColor)
            p.drawRoundedRect(opt.rect, 0.0, 0.0)
            drawRoundedRectBorder(
                p, opt.rect, borderColor, borderW, 0.0
            )
            return

        if pe == PE.PE_IndicatorTabTear:
            tabBar = (
                w
                if isinstance(w, QTabBar)
                else None
            )
            documentMode = (
                tabBar.documentMode() if tabBar else False
            )
            rect = opt.rect
            shadowW = theme.spacing * 3
            startPos = QPointF(rect.topLeft())
            endPos = QPointF(rect.topLeft()) + QPointF(
                float(shadowW), 0.0
            )
            gradient = QLinearGradient(startPos, endPos)
            startColor = self.tabBarShadowColor()
            endColor = theme.shadowColorTransparent
            gradient.setColorAt(0.0, startColor)
            gradient.setColorAt(1.0, endColor)
            radius = theme.borderRadius * 1.5
            backup = p.compositionMode()
            p.setCompositionMode(
                QPainter.CompositionMode.CompositionMode_Multiply
            )
            drawRoundedRect(
                p,
                rect,
                QBrush(gradient),
                RadiusesF(radius, 0.0, 0.0, 0.0)
                if not documentMode
                else RadiusesF(0.0),
            )
            p.setCompositionMode(backup)
            return

        if pe == PE.PE_IndicatorTabTearRight:
            tabBar = (
                w
                if isinstance(w, QTabBar)
                else None
            )
            documentMode = (
                tabBar.documentMode() if tabBar else False
            )
            rect = opt.rect
            scrollButtonsW = (
                theme.controlHeightMedium * 2
                + theme.spacing * 3
            )
            shadowW = theme.spacing * 3
            startPos = QPointF(rect.topLeft())
            endPos = QPointF(rect.topLeft()) + QPointF(
                float(shadowW), 0.0
            )
            gradient = QLinearGradient(startPos, endPos)
            startColor = theme.shadowColorTransparent
            endColor = self.tabBarShadowColor()
            gradient.setColorAt(0.0, startColor)
            gradient.setColorAt(1.0, endColor)
            backup = p.compositionMode()
            p.setCompositionMode(
                QPainter.CompositionMode.CompositionMode_Multiply
            )
            radius = theme.borderRadius * 1.5
            drawRoundedRect(
                p,
                rect,
                QBrush(gradient),
                RadiusesF(0.0, radius, 0.0, 0.0)
                if not documentMode
                else RadiusesF(0.0),
            )
            p.setCompositionMode(backup)

            mouse = getMouseState(opt.state)
            tabBarBgColor = self.tabBarBackgroundColor(mouse)
            filledRect = QRect(
                rect.x() + rect.width() - scrollButtonsW,
                rect.y(),
                scrollButtonsW,
                rect.height(),
            )
            drawRoundedRect(
                p,
                filledRect,
                tabBarBgColor,
                RadiusesF(0.0, radius, 0.0, 0.0)
                if not documentMode
                else RadiusesF(0.0),
            )
            return

        if pe == PE.PE_PanelItemViewItem:
            if isinstance(
                opt, QtWidgets.QStyleOptionViewItem
            ):
                rect = opt.rect
                row = opt.index.row()
                column = opt.index.column()
                mouse = getMouseState(opt.state)
                selection = getSelectionState(opt.state)
                widgetHasFocus = (
                    w.hasFocus() if w else False
                )
                focus = (
                    FocusState.Focused
                    if widgetHasFocus
                    and selection
                    == SelectionState.Selected
                    else FocusState.NotFocused
                )
                active = getActiveState(opt.state)
                color = self.listItemBackgroundColor(
                    mouse,
                    selection,
                    focus,
                    active,
                    opt.index,
                    w,
                )
                p.fillRect(rect, color)

                # Left border for first column in table
                if column == 0 and isinstance(w, QTableView):
                    if (
                        w.showGrid()
                        and w.verticalHeader().isHidden()
                    ):
                        lineW = theme.borderWidth
                        lp1 = QPointF(
                            rect.x() + lineW * 0.5, rect.y()
                        )
                        lp2 = QPointF(
                            rect.x() + lineW * 0.5,
                            rect.y() + rect.height(),
                        )
                        lineColor = self.tableLineColor()
                        p.setRenderHint(
                            QPainter.RenderHint.Antialiasing,
                            False,
                        )
                        p.setPen(QPen(lineColor, lineW))
                        p.drawLine(lp1, lp2)

                # Top border for first row in table
                if row == 0 and isinstance(w, QTableView):
                    if (
                        w.showGrid()
                        and w.horizontalHeader().isHidden()
                    ):
                        lineW = theme.borderWidth
                        lp1 = QPointF(
                            rect.x(),
                            rect.y() + lineW * 0.5,
                        )
                        lp2 = QPointF(
                            rect.x() + rect.width(),
                            rect.y() + lineW * 0.5,
                        )
                        lineColor = self.tableLineColor()
                        p.setRenderHint(
                            QPainter.RenderHint.Antialiasing,
                            False,
                        )
                        p.setPen(QPen(lineColor, lineW))
                        p.drawLine(lp1, lp2)

                isTable = isinstance(w, QTableView)
                if isTable and row < 0:
                    return
            return

        if pe == PE.PE_PanelItemViewRow:
            if isinstance(
                opt, QtWidgets.QStyleOptionViewItem
            ):
                alternate = getAlternateState(opt.features)
                mouse = (
                    MouseState.Normal
                    if opt.state & State.State_Enabled
                    else MouseState.Disabled
                )
                color = self.listItemRowBackgroundColor(
                    mouse, alternate
                )
                p.fillRect(opt.rect, color)

                popup = (
                    w.parentWidget() if w else None
                )
                isComboPopup = popup and popup.inherits(
                    "QComboBoxPrivateContainer"
                )
                if not isComboPopup:
                    self.drawPrimitive(
                        PE.PE_PanelItemViewItem, opt, p, w
                    )
            return

        if pe == PE.PE_PanelStatusBar:
            bgColor = self.statusBarBackgroundColor()
            borderColor = self.statusBarBorderColor()
            borderW = theme.borderWidth
            p.fillRect(opt.rect, bgColor)
            lineRect = QRect(
                opt.rect.x(),
                opt.rect.y(),
                opt.rect.width(),
                borderW,
            )
            p.fillRect(lineRect, borderColor)
            return

        if pe == PE.PE_IndicatorTabClose:
            button = (
                w
                if isinstance(w, QAbstractButton)
                else None
            )
            if button:
                tabBar = (
                    w.parentWidget()
                    if isinstance(
                        w.parentWidget(), QTabBar
                    )
                    else None
                )
                if tabBar:
                    rect = opt.rect
                    tabIndex = tabBar.tabAt(
                        w.mapToParent(rect.center())
                    )
                    tabSelected = bool(
                        opt.state & State.State_Selected
                    )
                    tabHovered = False
                    if tabBar.underMouse():
                        mousePos = tabBar.mapFromGlobal(
                            QCursor.pos()
                        )
                        mouseTab = tabBar.tabAt(mousePos)
                        tabHovered = tabIndex == mouseTab
                    pressedBtns = (
                        QGuiApplication.mouseButtons()
                    )
                    tabBarPressed = (
                        pressedBtns != Qt.MouseButton.NoButton
                        and not button.isDown()
                    )
                    visible = (
                        not tabBarPressed and tabHovered
                    ) or tabSelected

                    radius = float(rect.height()) / 2.0
                    mouse = getTabItemMouseState(
                        opt.state, tabHovered
                    )
                    selected = getSelectionState(opt.state)
                    bgColor = (
                        self.tabCloseButtonBackgroundColor(
                            mouse, selected
                        )
                    )
                    p.setRenderHint(
                        QPainter.RenderHint.Antialiasing, True
                    )
                    p.setPen(Qt.PenStyle.NoPen)
                    p.setBrush(bgColor)
                    p.drawRoundedRect(
                        QRectF(rect), radius, radius
                    )

                    fgColor = (
                        self.tabCloseButtonForegroundColor(
                            mouse, selected
                        )
                    )
                    p.setPen(
                        QPen(
                            fgColor,
                            iconPenWidth,
                            Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.FlatCap,
                            Qt.PenJoinStyle.RoundJoin,
                        )
                    )
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    iconSize = theme.iconSize
                    closeRect = QRect(
                        rect.x()
                        + (rect.width() - iconSize.width())
                        // 2,
                        rect.y()
                        + (
                            rect.height()
                            - iconSize.height()
                        )
                        // 2,
                        iconSize.width(),
                        iconSize.height(),
                    )
                    drawCloseIndicator(closeRect, p)
            return

        if pe == PE.PE_PanelMenu:
            radius = theme.borderRadius
            bgColor = self.menuBackgroundColor()
            borderColor = self.menuBorderColor()
            borderW = theme.borderWidth
            p.setRenderHint(
                QPainter.RenderHint.Antialiasing, True
            )
            totalRect = opt.rect
            shadowPadding = self.pixelMetric(
                PM.PM_MenuPanelWidth
            )
            frameRect = totalRect.marginsRemoved(
                QMargins(
                    shadowPadding,
                    shadowPadding,
                    shadowPadding,
                    shadowPadding,
                )
            )
            dropShadowRadius = theme.spacing
            dropShadowOffsetY = shadowPadding // 3
            dropShadowPixmap = getDropShadowPixmap(
                frameRect.size(),
                radius,
                dropShadowRadius,
                theme.shadowColor1,
            )
            dropShadowX = (
                frameRect.x()
                + (
                    frameRect.width()
                    - dropShadowPixmap.width()
                )
                // 2
            )
            dropShadowY = (
                frameRect.y()
                + (
                    frameRect.height()
                    - dropShadowPixmap.height()
                )
                // 2
                + dropShadowOffsetY
            )
            backup = p.compositionMode()
            p.setCompositionMode(
                QPainter.CompositionMode.CompositionMode_Multiply
            )
            p.drawPixmap(
                dropShadowX, dropShadowY, dropShadowPixmap
            )
            p.setCompositionMode(backup)
            halfBW = borderW / 2.0
            bgFrameRect = QRectF(frameRect).marginsRemoved(
                QMarginsF(halfBW, halfBW, halfBW, halfBW)
            )
            drawRoundedRect(p, bgFrameRect, bgColor, radius)
            drawRoundedRectBorder(
                p, frameRect, borderColor, borderW, radius
            )
            return

        if pe == PE.PE_Widget:
            return super().drawPrimitive(pe, opt, p, w)

        # Default: delegate to QCommonStyle
        super().drawPrimitive(pe, opt, p, w)

    # ================================================================
    # drawControl
    # ================================================================

    def drawControl(self, ce, opt, p, w=None):
        theme = self._theme

        if ce == CE.CE_PushButton:
            if isinstance(
                opt, QtWidgets.QStyleOptionButton
            ):
                self.drawControl(
                    CE.CE_PushButtonBevel, opt, p, w
                )
                optFg = QtWidgets.QStyleOptionButton(opt)
                optFg.rect = self.subElementRect(
                    SE.SE_PushButtonContents, opt, w
                )
                self.drawControl(
                    CE.CE_PushButtonLabel, optFg, p, w
                )
            return

        if ce == CE.CE_PushButtonBevel:
            if isinstance(
                opt, QtWidgets.QStyleOptionButton
            ):
                optBg = QtWidgets.QStyleOptionButton(opt)
                optBg.rect = self.subElementRect(
                    SE.SE_PushButtonBevel, opt, w
                )
                self.drawPrimitive(
                    PE.PE_FrameButtonBevel, optBg, p, w
                )
            return

        if ce == CE.CE_PushButtonLabel:
            if isinstance(
                opt, QtWidgets.QStyleOptionButton
            ):
                mouse = getMouseState(opt.state)
                isDefault = bool(
                    opt.features
                    & QtWidgets.QStyleOptionButton.ButtonFeature.DefaultButton
                )
                role = getColorRole(opt.state, isDefault)
                fgColor = self.buttonForegroundColor(
                    mouse, role
                )
                indicatorSize = self.pixelMetric(
                    PM.PM_MenuButtonIndicator, opt, w
                )
                spacing = theme.spacing
                hasMenu = bool(
                    opt.features
                    & QtWidgets.QStyleOptionButton.ButtonFeature.HasMenu
                )
                centered = not hasMenu
                checked = getCheckState(opt.state)
                pixmap = getPixmap(
                    opt.icon, opt.iconSize, mouse, checked, w
                )
                colorizedPixmap = self.getColorizedPixmap(
                    pixmap,
                    self.autoIconColor(w),
                    fgColor,
                    fgColor,
                )
                pixmapPR = colorizedPixmap.devicePixelRatio()
                iconW = (
                    0
                    if colorizedPixmap.isNull()
                    else int(
                        colorizedPixmap.width() / pixmapPR
                    )
                )
                textW = textWidth(
                    opt.fontMetrics, opt.text
                )
                iconSpacing = (
                    spacing
                    if iconW > 0
                    and opt.text
                    and textW > 0
                    else 0
                )
                fgRect = (
                    opt.rect.marginsRemoved(
                        QMargins(
                            0,
                            0,
                            indicatorSize + spacing,
                            0,
                        )
                    )
                    if hasMenu
                    else opt.rect
                )
                contentW = (
                    min(
                        fgRect.width(),
                        iconW + iconSpacing + textW,
                    )
                    if centered
                    else fgRect.width()
                )
                contentX = (
                    fgRect.x()
                    + (fgRect.width() - contentW) // 2
                    if centered
                    else fgRect.x()
                )
                availableW = contentW
                availableX = contentX
                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing
                )

                # Icon
                if iconW > 0:
                    pmW = (
                        int(
                            colorizedPixmap.width()
                            / pixmapPR
                        )
                        if pixmapPR
                        else 0
                    )
                    pmH = (
                        int(
                            colorizedPixmap.height()
                            / pixmapPR
                        )
                        if pixmapPR
                        else 0
                    )
                    pmX = (
                        contentX
                        + (contentW - pmW) // 2
                        if textW == 0 and not hasMenu
                        else contentX
                    )
                    pmY = (
                        opt.rect.y()
                        + (opt.rect.height() - pmH) // 2
                    )
                    pmRect = QRect(pmX, pmY, pmW, pmH)
                    availableW -= pmW + iconSpacing
                    availableX += pmW + iconSpacing
                    p.drawPixmap(pmRect, colorizedPixmap)

                # Text
                if availableW > 0 and textW > 0:
                    elidedText = (
                        opt.fontMetrics.elidedText(
                            opt.text,
                            Qt.TextElideMode.ElideRight,
                            availableW,
                            Qt.TextFlag.TextSingleLine,
                        )
                    )
                    elidedW = textWidth(
                        opt.fontMetrics, elidedText
                    )
                    textRect = QRect(
                        availableX,
                        opt.rect.y(),
                        elidedW,
                        opt.rect.height(),
                    )
                    textFlags = int(
                        Qt.AlignmentFlag.AlignVCenter
                        | Qt.AlignmentFlag.AlignBaseline
                        | Qt.TextFlag.TextSingleLine
                        | Qt.TextFlag.TextHideMnemonic
                    )
                    if iconW == 0:
                        textFlags |= int(
                            Qt.AlignmentFlag.AlignHCenter
                        )
                    else:
                        textFlags |= int(
                            Qt.AlignmentFlag.AlignLeft
                        )
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(fgColor)
                    p.drawText(
                        textRect, textFlags, elidedText
                    )

                # Arrow (if menu)
                if hasMenu:
                    indW = indicatorSize
                    indH = indicatorSize
                    indX = (
                        opt.rect.x()
                        + opt.rect.width()
                        - indW
                    )
                    indY = (
                        opt.rect.y()
                        + (opt.rect.height() - indH) // 2
                    )
                    indRect = QRect(indX, indY, indW, indH)
                    path = getMenuIndicatorPath(indRect)
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(
                        QPen(
                            fgColor,
                            iconPenWidth,
                            Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap,
                            Qt.PenJoinStyle.RoundJoin,
                        )
                    )
                    p.drawPath(path)
            return

        if ce in (CE.CE_RadioButton, CE.CE_CheckBox):
            if isinstance(
                opt, QtWidgets.QStyleOptionButton
            ):
                isRadio = ce == CE.CE_RadioButton
                optInd = QtWidgets.QStyleOptionButton(opt)
                optInd.rect = self.subElementRect(
                    SE.SE_RadioButtonIndicator
                    if isRadio
                    else SE.SE_CheckBoxIndicator,
                    opt,
                    w,
                )
                self.drawPrimitive(
                    PE.PE_IndicatorRadioButton
                    if isRadio
                    else PE.PE_IndicatorCheckBox,
                    optInd,
                    p,
                    w,
                )
                optLabel = QtWidgets.QStyleOptionButton(opt)
                optLabel.rect = self.subElementRect(
                    SE.SE_RadioButtonContents
                    if isRadio
                    else SE.SE_CheckBoxContents,
                    opt,
                    w,
                )
                self.drawControl(
                    CE.CE_RadioButtonLabel
                    if isRadio
                    else CE.CE_CheckBoxLabel,
                    optLabel,
                    p,
                    w,
                )
            return

        if ce in (
            CE.CE_CheckBoxLabel,
            CE.CE_RadioButtonLabel,
        ):
            if isinstance(
                opt, QtWidgets.QStyleOptionButton
            ):
                mouse = getMouseState(opt.state)
                fgColor = self.labelForegroundColor(
                    mouse, w
                )
                spacing = theme.spacing
                checked = getCheckState(opt.state)
                pixmap = getPixmap(
                    opt.icon, opt.iconSize, mouse, checked, w
                )
                colorizedPixmap = self.getColorizedPixmap(
                    pixmap,
                    self.autoIconColor(w),
                    fgColor,
                    fgColor,
                )
                pixmapPR = colorizedPixmap.devicePixelRatio()
                iconW = (
                    0
                    if colorizedPixmap.isNull()
                    else int(
                        colorizedPixmap.width() / pixmapPR
                    )
                )
                iconSpacing = spacing if iconW > 0 else 0
                availableW = opt.rect.width()
                availableX = opt.rect.x()
                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing
                )

                if iconW > 0:
                    pmW = (
                        int(
                            colorizedPixmap.width()
                            / pixmapPR
                        )
                        if pixmapPR
                        else 0
                    )
                    pmH = (
                        int(
                            colorizedPixmap.height()
                            / pixmapPR
                        )
                        if pixmapPR
                        else 0
                    )
                    pmX = opt.rect.x()
                    pmY = (
                        opt.rect.y()
                        + (opt.rect.height() - pmH) // 2
                    )
                    pmRect = QRect(pmX, pmY, pmW, pmH)
                    availableW -= pmW + iconSpacing
                    availableX += pmW + iconSpacing
                    p.drawPixmap(pmRect, colorizedPixmap)

                if availableW > 0 and opt.text:
                    elidedText = (
                        opt.fontMetrics.elidedText(
                            opt.text,
                            Qt.TextElideMode.ElideRight,
                            availableW,
                            Qt.TextFlag.TextSingleLine,
                        )
                    )
                    textRect = QRect(
                        availableX,
                        opt.rect.y(),
                        availableW,
                        opt.rect.height(),
                    )
                    textFlags = int(
                        Qt.AlignmentFlag.AlignVCenter
                        | Qt.AlignmentFlag.AlignBaseline
                        | Qt.TextFlag.TextSingleLine
                        | Qt.AlignmentFlag.AlignLeft
                        | Qt.TextFlag.TextHideMnemonic
                    )
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(fgColor)
                    p.drawText(
                        textRect, textFlags, elidedText
                    )
            return

        if ce == CE.CE_TabBarTab:
            if isinstance(
                opt, QtWidgets.QStyleOptionTab
            ):
                padding = _tabExtraPadding(theme, opt)
                tabBgOpt = QtWidgets.QStyleOptionTab(opt)
                tabBgOpt.rect = (
                    tabBgOpt.rect.marginsRemoved(padding)
                )
                self.drawControl(
                    CE.CE_TabBarTabShape, tabBgOpt, p, w
                )
                tabFgOpt = QtWidgets.QStyleOptionTab(opt)
                labelRect = self.subElementRect(
                    SE.SE_TabBarTabText, opt, w
                )
                tabFgOpt.rect = labelRect
                self.drawControl(
                    CE.CE_TabBarTabLabel, tabFgOpt, p, w
                )
            return

        if ce == CE.CE_TabBarTabShape:
            if isinstance(
                opt, QtWidgets.QStyleOptionTab
            ):
                mouse = getMouseState(opt.state)
                selection = getSelectionState(opt.state)
                mouseOverTab = mouse in (
                    MouseState.Hovered,
                    MouseState.Pressed,
                )
                mousePressed = mouse == MouseState.Pressed
                tabIsSelected = (
                    selection == SelectionState.Selected
                )

                tabBar = (
                    w
                    if isinstance(w, QTabBar)
                    else None
                )
                if tabBar:
                    cursorPos = tabBar.mapFromGlobal(
                        QCursor.pos()
                    )
                    spacing = theme.spacing
                    buttonsVisible = (
                        _areTabBarScrollButtonsVisible(
                            tabBar
                        )
                    )
                    buttonsW = (
                        theme.controlHeightMedium * 2
                        + spacing * 3
                        if buttonsVisible
                        else 0
                    )
                    mouseOverButtons = (
                        cursorPos.x()
                        > tabBar.width() - buttonsW
                    )
                else:
                    mouseOverButtons = False

                drawShape = tabIsSelected or (
                    not mouseOverButtons and mouseOverTab
                )
                drawShadow = (
                    tabIsSelected and not mousePressed
                )
                if drawShape:
                    radius = theme.borderRadius
                    bgColor = self.tabBackgroundColor(
                        mouse, selection
                    )
                    radiuses = (
                        RadiusesF(
                            radius, radius, radius, radius
                        )
                        if tabIsSelected
                        else RadiusesF(
                            radius, radius, 0.0, 0.0
                        )
                    )
                    drawTab(
                        p,
                        opt.rect,
                        radiuses,
                        bgColor,
                        drawShadow,
                        theme.shadowColor2,
                    )
            return

        if ce == CE.CE_TabBarTabLabel:
            if isinstance(
                opt, QtWidgets.QStyleOptionTab
            ):
                shape = opt.shape
                isVertical = shape in (
                    QTabBar.Shape.RoundedEast,
                    QTabBar.Shape.RoundedWest,
                    QTabBar.Shape.TriangularEast,
                    QTabBar.Shape.TriangularWest,
                )
                if isVertical:
                    return

                rect = opt.rect
                mouse = getMouseState(opt.state)
                selection = getSelectionState(opt.state)
                fgColor = self.tabForegroundColor(
                    mouse, selection
                )
                spacing = theme.spacing
                icon = opt.icon
                iconSize = (
                    QSize(0, 0)
                    if icon.isNull()
                    else opt.iconSize
                )
                fm = opt.fontMetrics
                textAvailW = rect.width() - (
                    0
                    if iconSize.isEmpty()
                    else iconSize.width() + spacing
                )
                elidedText = fm.elidedText(
                    opt.text,
                    Qt.TextElideMode.ElideMiddle,
                    textAvailW,
                    Qt.TextFlag.TextSingleLine,
                )
                # The ellipsis character
                hasText = elidedText != "\u2026"
                textColor = self.tabForegroundColor(
                    mouse, selection
                )

                availableW = rect.width()
                availableX = rect.x()

                if not iconSize.isEmpty():
                    checked = (
                        CheckState.Checked
                        if selection
                        == SelectionState.Selected
                        else CheckState.NotChecked
                    )
                    pixmap = getPixmap(
                        icon, iconSize, mouse, checked, w
                    )
                    colorizedPixmap = (
                        self.getColorizedPixmap(
                            pixmap,
                            self.autoIconColor(w),
                            fgColor,
                            textColor,
                        )
                    )
                    pr = colorizedPixmap.devicePixelRatio()
                    pmW = (
                        int(
                            colorizedPixmap.width() / pr
                        )
                        if pr
                        else 0
                    )
                    pmH = (
                        int(
                            colorizedPixmap.height() / pr
                        )
                        if pr
                        else 0
                    )
                    pmX = (
                        availableX
                        if hasText
                        else rect.x()
                        + (rect.width() - pmW) // 2
                    )
                    pmY = (
                        rect.y()
                        + (rect.height() - pmH) // 2
                    )
                    pmRect = QRect(pmX, pmY, pmW, pmH)
                    availableW -= pmW + spacing
                    availableX += pmW + spacing
                    p.drawPixmap(pmRect, colorizedPixmap)

                if availableW > 0 and hasText:
                    textRect = QRect(
                        availableX,
                        rect.y(),
                        availableW,
                        rect.height(),
                    )
                    textFlags = int(
                        Qt.AlignmentFlag.AlignVCenter
                        | Qt.AlignmentFlag.AlignBaseline
                        | Qt.TextFlag.TextSingleLine
                        | Qt.TextFlag.TextHideMnemonic
                        | Qt.AlignmentFlag.AlignLeft
                    )
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(textColor)
                    p.drawText(
                        textRect, textFlags, elidedText
                    )
            return

        if ce == CE.CE_ProgressBar:
            if isinstance(
                opt, QtWidgets.QStyleOptionProgressBar
            ):
                optGroove = (
                    QtWidgets.QStyleOptionProgressBar(opt)
                )
                optGroove.rect = self.subElementRect(
                    SE.SE_ProgressBarGroove, opt, w
                )
                self.drawControl(
                    CE.CE_ProgressBarGroove, optGroove, p, w
                )
                optContent = (
                    QtWidgets.QStyleOptionProgressBar(opt)
                )
                optContent.rect = self.subElementRect(
                    SE.SE_ProgressBarContents, opt, w
                )
                self.drawControl(
                    CE.CE_ProgressBarContents,
                    optContent,
                    p,
                    w,
                )
                if opt.textVisible:
                    optText = (
                        QtWidgets.QStyleOptionProgressBar(
                            opt
                        )
                    )
                    optText.rect = self.subElementRect(
                        SE.SE_ProgressBarLabel, opt, w
                    )
                    self.drawControl(
                        CE.CE_ProgressBarLabel,
                        optText,
                        p,
                        w,
                    )
            return

        if ce == CE.CE_ProgressBarGroove:
            if isinstance(
                opt, QtWidgets.QStyleOptionProgressBar
            ):
                radius = opt.rect.height() / 2.0
                mouse = getMouseState(opt.state)
                color = self.progressBarGrooveColor(mouse)
                drawRoundedRect(
                    p, opt.rect, color, radius
                )
            return

        if ce == CE.CE_ProgressBarContents:
            if isinstance(
                opt, QtWidgets.QStyleOptionProgressBar
            ):
                radius = opt.rect.height() / 2.0
                mouse = getMouseState(opt.state)
                color = self.progressBarValueColor(mouse)
                indeterminate = (
                    opt.maximum == 0 and opt.minimum == 0
                )
                if indeterminate:
                    # Simple static indeterminate bar
                    valueRectW = int(
                        opt.rect.width() * 0.25
                    )
                    valueRectX = (
                        opt.rect.x()
                        + (opt.rect.width() - valueRectW)
                        // 2
                    )
                    valueRect = QRectF(
                        valueRectX,
                        opt.rect.y(),
                        valueRectW,
                        opt.rect.height(),
                    )
                    p.setPen(Qt.PenStyle.NoPen)
                    p.setBrush(color)
                    p.drawRoundedRect(valueRect, 3, 3)
                else:
                    drawProgressBarValueRect(
                        p,
                        opt.rect,
                        color,
                        opt.minimum,
                        opt.maximum,
                        opt.progress,
                        radius,
                        opt.invertedAppearance,
                    )
            return

        if ce == CE.CE_ProgressBarLabel:
            if isinstance(
                opt, QtWidgets.QStyleOptionProgressBar
            ):
                mouse = getMouseState(opt.state)
                color = self.labelForegroundColor(mouse, w)
                textFlags = int(
                    Qt.AlignmentFlag.AlignVCenter
                    | Qt.AlignmentFlag.AlignBaseline
                    | Qt.TextFlag.TextSingleLine
                    | Qt.AlignmentFlag.AlignRight
                    | Qt.TextFlag.TextHideMnemonic
                )
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(color)
                p.drawText(
                    opt.rect, textFlags, opt.text
                )
            return

        if ce == CE.CE_MenuItem:
            if isinstance(
                opt, QtWidgets.QStyleOptionMenuItem
            ):
                MenuItemType = (
                    QtWidgets.QStyleOptionMenuItem.MenuItemType
                )
                if (
                    opt.menuItemType
                    == MenuItemType.Separator
                ):
                    color = self.menuSeparatorColor()
                    rect = opt.rect.marginsRemoved(
                        QMargins(0, 0, 0, 0)
                    )
                    sepThickness = theme.borderWidth
                    drawMenuSeparator(
                        p, rect, color, sepThickness
                    )
                elif opt.menuItemType in (
                    MenuItemType.Normal,
                    MenuItemType.SubMenu,
                ):
                    mouse = getMenuItemMouseState(
                        opt.state
                    )

                    # Background
                    bgRect = opt.rect
                    bgColor = self.menuItemBackgroundColor(
                        mouse
                    )
                    menuItemRadius = (
                        theme.menuItemBorderRadius
                    )
                    p.setRenderHint(
                        QPainter.RenderHint.Antialiasing,
                        True,
                    )
                    p.setPen(Qt.PenStyle.NoPen)
                    p.setBrush(bgColor)
                    p.drawRoundedRect(
                        QRectF(bgRect),
                        menuItemRadius,
                        menuItemRadius,
                    )

                    # Foreground
                    spacing = theme.spacing
                    fgColor = (
                        self.menuItemForegroundColor(mouse)
                    )
                    menuHasCheckable = (
                        opt.menuHasCheckableItems
                    )
                    checkable = (
                        opt.checkType
                        != QtWidgets.QStyleOptionMenuItem.CheckType.NotCheckable
                    )
                    checkState = (
                        CheckState.Checked
                        if opt.checked
                        else CheckState.NotChecked
                    )
                    arrowW = theme.iconSize.width()
                    hPadding = theme.spacing
                    fgRect = bgRect.marginsRemoved(
                        QMargins(hPadding, 0, hPadding, 0)
                    )
                    label, shortcut = (
                        getMenuLabelAndShortcut(opt.text)
                    )
                    useMnemonic = self.styleHint(
                        SH.SH_UnderlineShortcut, opt, w
                    )
                    parent = (
                        w.parentWidget() if w else None
                    )
                    hasFocus = (
                        w and w.hasFocus()
                    ) or (parent and parent.hasFocus())
                    hasSubMenu = (
                        opt.menuItemType
                        == MenuItemType.SubMenu
                    )
                    showMnemonic = hasFocus
                    availableW = fgRect.width() - (
                        arrowW + spacing
                        if hasSubMenu
                        else 0
                    )
                    availableX = fgRect.x()

                    # Check
                    if menuHasCheckable or checkable:
                        checkBoxSize = theme.iconSize
                        if checkable:
                            cbX = availableX
                            cbY = (
                                fgRect.y()
                                + (
                                    fgRect.height()
                                    - checkBoxSize.height()
                                )
                                // 2
                            )
                            cbRect = QRect(
                                QPoint(cbX, cbY),
                                checkBoxSize,
                            )
                            isRadio = (
                                opt.checkType
                                == QtWidgets.QStyleOptionMenuItem.CheckType.Exclusive
                            )
                            progress = (
                                1.0
                                if checkState
                                == CheckState.Checked
                                else 0.0
                            )
                            borderW = theme.borderWidth
                            selected = getSelectionState(
                                opt.state
                            )
                            active = getActiveState(
                                opt.state
                            )
                            boxFg = self.listItemCheckButtonForegroundColor(
                                mouse,
                                checkState,
                                selected,
                                active,
                            )
                            boxBg = self.listItemCheckButtonBackgroundColor(
                                mouse,
                                checkState,
                                selected,
                                active,
                            )
                            boxBrd = self.listItemCheckButtonBorderColor(
                                mouse,
                                checkState,
                                selected,
                                active,
                            )
                            if isRadio:
                                drawRadioButton(
                                    p,
                                    cbRect,
                                    boxBg,
                                    boxBrd,
                                    boxFg,
                                    borderW,
                                    progress,
                                )
                            else:
                                drawCheckButton(
                                    p,
                                    cbRect,
                                    theme.checkBoxBorderRadius,
                                    boxBg,
                                    boxBrd,
                                    boxFg,
                                    borderW,
                                    progress,
                                    checkState,
                                )

                        taken = (
                            checkBoxSize.width() + spacing
                        )
                        availableW -= taken
                        availableX += taken

                    # Icon
                    showIcons = not QtCore.QCoreApplication.testAttribute(
                        Qt.ApplicationAttribute.AA_DontShowIconsInMenus
                    )
                    iconSpace = (
                        opt.maxIconWidth + spacing
                        if showIcons
                        and opt.maxIconWidth > 0
                        else 0
                    )
                    pixmap = getPixmap(
                        opt.icon,
                        theme.iconSize,
                        mouse,
                        checkState,
                        w,
                    )
                    if not pixmap.isNull():
                        colorizedPixmap = (
                            self.getColorizedPixmap(
                                pixmap,
                                self.autoIconColor(w),
                                fgColor,
                                fgColor,
                            )
                        )
                        pr = (
                            colorizedPixmap.devicePixelRatio()
                        )
                        pmW = (
                            int(
                                colorizedPixmap.width()
                                / pr
                            )
                            if pr
                            else 0
                        )
                        pmH = (
                            int(
                                colorizedPixmap.height()
                                / pr
                            )
                            if pr
                            else 0
                        )
                        pmX = availableX
                        pmY = (
                            fgRect.y()
                            + (fgRect.height() - pmH) // 2
                        )
                        pmRect = QRect(
                            pmX, pmY, pmW, pmH
                        )
                        p.drawPixmap(
                            pmRect, colorizedPixmap
                        )
                    availableW -= iconSpace
                    availableX += iconSpace

                    # Shortcut text
                    if shortcut:
                        fm = opt.fontMetrics
                        shortcutW = fm.boundingRect(
                            opt.rect,
                            int(
                                Qt.AlignmentFlag.AlignRight
                            ),
                            shortcut,
                        ).width()
                        if availableW > shortcutW:
                            shortcutX = (
                                fgRect.x()
                                + fgRect.width()
                                - shortcutW
                            )
                            shortcutRect = QRect(
                                shortcutX,
                                fgRect.y(),
                                shortcutW,
                                fgRect.height(),
                            )
                            shortcutFlags = int(
                                Qt.AlignmentFlag.AlignVCenter
                                | Qt.AlignmentFlag.AlignBaseline
                                | Qt.TextFlag.TextSingleLine
                                | Qt.AlignmentFlag.AlignRight
                                | Qt.TextFlag.TextHideMnemonic
                            )
                            shortcutColor = self.menuItemSecondaryForegroundColor(
                                mouse
                            )
                            p.setPen(shortcutColor)
                            p.drawText(
                                shortcutRect,
                                shortcutFlags,
                                shortcut,
                            )
                            taken = shortcutW + spacing * 2
                            availableW -= taken

                    # Text
                    if label:
                        fm = opt.fontMetrics
                        elidedText = fm.elidedText(
                            label,
                            Qt.TextElideMode.ElideRight,
                            availableW,
                            Qt.TextFlag.TextSingleLine,
                        )
                        textRect = QRect(
                            availableX,
                            fgRect.y(),
                            availableW,
                            fgRect.height(),
                        )
                        textFlags = int(
                            Qt.AlignmentFlag.AlignVCenter
                            | Qt.AlignmentFlag.AlignBaseline
                            | Qt.TextFlag.TextSingleLine
                            | Qt.TextFlag.TextShowMnemonic
                            | Qt.AlignmentFlag.AlignLeft
                        )
                        if not showMnemonic:
                            textFlags |= int(
                                Qt.TextFlag.TextHideMnemonic
                            )
                        p.setPen(fgColor)
                        p.drawText(
                            textRect,
                            textFlags,
                            elidedText,
                        )

                    # Sub-menu indicator
                    if hasSubMenu:
                        arrowSize = theme.iconSize
                        arrowRightM = spacing
                        aX = (
                            bgRect.x()
                            + bgRect.width()
                            - arrowSize.width()
                            - arrowRightM
                        )
                        aY = (
                            bgRect.y()
                            + (
                                bgRect.height()
                                - arrowSize.height()
                            )
                            // 2
                        )
                        arrowRect = QRect(
                            aX,
                            aY,
                            arrowSize.width(),
                            arrowSize.height(),
                        )
                        p.setBrush(Qt.BrushStyle.NoBrush)
                        p.setPen(
                            QPen(
                                fgColor,
                                iconPenWidth,
                                Qt.PenStyle.SolidLine,
                                Qt.PenCapStyle.RoundCap,
                                Qt.PenJoinStyle.RoundJoin,
                            )
                        )
                        drawSubMenuIndicator(arrowRect, p)
            return

        if ce == CE.CE_MenuScroller:
            if isinstance(
                opt, QtWidgets.QStyleOptionMenuItem
            ):
                mouse = getMenuItemMouseState(opt.state)
                bgColor = self.menuItemBackgroundColor(mouse)
                radius = theme.menuItemBorderRadius
                drawRoundedRect(
                    p, opt.rect, bgColor, radius
                )
                isDown = bool(
                    opt.state & State.State_DownArrow
                )
                fgColor = self.menuItemForegroundColor(
                    mouse
                )
                iconSize = theme.iconSize
                iconX = (
                    opt.rect.x()
                    + (opt.rect.width() - iconSize.width())
                    // 2
                )
                iconY = (
                    opt.rect.y()
                    + (
                        opt.rect.height()
                        - iconSize.height()
                    )
                    // 2
                )
                iconRect = QRect(
                    QPoint(iconX, iconY), iconSize
                )
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(fgColor)
                yTranslate = (
                    QPoint(0, iconSize.height() // 4)
                    if isDown
                    else QPoint(0, -iconSize.height() // 4)
                )
                if isDown:
                    drawArrowDown(
                        iconRect.translated(yTranslate), p
                    )
                else:
                    drawArrowUp(
                        iconRect.translated(yTranslate), p
                    )
            return

        if ce in (
            CE.CE_MenuVMargin,
            CE.CE_MenuHMargin,
            CE.CE_MenuEmptyArea,
        ):
            return

        if ce == CE.CE_MenuBarItem:
            if isinstance(
                opt, QtWidgets.QStyleOptionMenuItem
            ):
                barBgColor = self.menuBarBackgroundColor()
                p.fillRect(opt.rect, barBgColor)

                mouse = getMenuItemMouseState(opt.state)
                selected = getSelectionState(opt.state)
                bgColor = (
                    self.menuBarItemBackgroundColor(
                        mouse, selected
                    )
                )
                fgColor = (
                    self.menuBarItemForegroundColor(
                        mouse, selected
                    )
                )
                textFlags = int(
                    Qt.AlignmentFlag.AlignVCenter
                    | Qt.AlignmentFlag.AlignBaseline
                    | Qt.TextFlag.TextSingleLine
                    | Qt.AlignmentFlag.AlignHCenter
                )
                if self.styleHint(
                    SH.SH_UnderlineShortcut, opt, w
                ):
                    textFlags |= int(
                        Qt.TextFlag.TextShowMnemonic
                    )
                if w and not w.hasFocus():
                    textFlags |= int(
                        Qt.TextFlag.TextHideMnemonic
                    )
                radius = theme.menuBarItemBorderRadius
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(bgColor)
                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing, True
                )
                p.drawRoundedRect(
                    QRectF(opt.rect), radius, radius
                )
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(fgColor)
                p.drawText(
                    opt.rect, textFlags, opt.text
                )
            return

        if ce == CE.CE_MenuBarEmptyArea:
            bgColor = self.menuBarBackgroundColor()
            p.fillRect(opt.rect, bgColor)
            return

        if ce == CE.CE_ToolButtonLabel:
            if isinstance(
                opt, QtWidgets.QStyleOptionToolButton
            ):
                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing
                )
                rect = opt.rect
                icon = opt.icon

                buttonState = opt.state

                isExtBtn = (
                    w
                    and w.objectName()
                    == "qt_toolbar_ext_button"
                )
                if isExtBtn:
                    buttonState = buttonState & ~State.State_On

                iconSize = (
                    QSize(0, 0)
                    if icon.isNull()
                    else opt.iconSize
                )
                fm = opt.fontMetrics
                buttonStyle = opt.toolButtonStyle
                showText = (
                    buttonStyle
                    != Qt.ToolButtonStyle.ToolButtonIconOnly
                )
                showIcon = (
                    buttonStyle
                    != Qt.ToolButtonStyle.ToolButtonTextOnly
                )
                mouse = getToolButtonMouseState(buttonState)
                role = getColorRole(buttonState, False)
                checked = getCheckState(buttonState)
                fgColor = self.toolButtonForegroundColor(
                    mouse, role
                )
                spacing = theme.spacing
                hasMenu = bool(
                    opt.features
                    & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.HasMenu
                )
                leftPad = (
                    spacing * 2
                    if buttonStyle
                    == Qt.ToolButtonStyle.ToolButtonTextOnly
                    else spacing
                )
                hasIcon = showIcon and not iconSize.isEmpty()
                hasText = showText and bool(opt.text)
                rightPad = (
                    spacing * 2
                    if not hasMenu
                    and buttonStyle
                    in (
                        Qt.ToolButtonStyle.ToolButtonTextOnly,
                        Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
                    )
                    else spacing
                )
                fgRect = rect.adjusted(
                    leftPad, 0, -rightPad, 0
                )
                centered = not hasMenu
                textW = fm.boundingRect(
                    opt.rect,
                    int(Qt.AlignmentFlag.AlignCenter),
                    opt.text,
                ).width()
                contentW = (
                    min(
                        fgRect.width(),
                        iconSize.width() + spacing + textW,
                    )
                    if centered
                    else fgRect.width()
                )
                contentX = (
                    fgRect.x()
                    + (fgRect.width() - contentW) // 2
                    if centered
                    else fgRect.x()
                )
                availableW = contentW
                availableX = contentX

                if hasIcon:
                    pixmap = getPixmap(
                        icon, iconSize, mouse, checked, w
                    )
                    colorizedPixmap = (
                        self.getColorizedPixmap(
                            pixmap,
                            self.autoIconColor(w),
                            fgColor,
                            fgColor,
                        )
                    )
                    pr = colorizedPixmap.devicePixelRatio()
                    pmW = (
                        int(
                            colorizedPixmap.width() / pr
                        )
                        if pr
                        else 0
                    )
                    pmH = (
                        int(
                            colorizedPixmap.height() / pr
                        )
                        if pr
                        else 0
                    )
                    iconOnly = (
                        buttonStyle
                        == Qt.ToolButtonStyle.ToolButtonIconOnly
                    )
                    pmX = (
                        availableX
                        + (availableW - pmW) // 2
                        if iconOnly
                        else availableX
                    )
                    pmY = (
                        rect.y()
                        + (rect.height() - pmH) // 2
                    )
                    pmRect = QRect(pmX, pmY, pmW, pmH)
                    availableW -= pmW + spacing
                    availableX += pmW + spacing
                    p.drawPixmap(pmRect, colorizedPixmap)

                if hasText and availableW > 0:
                    elidedText = fm.elidedText(
                        opt.text,
                        Qt.TextElideMode.ElideRight,
                        availableW,
                        Qt.TextFlag.TextSingleLine,
                    )
                    elidedW = fm.boundingRect(
                        opt.rect,
                        int(Qt.AlignmentFlag.AlignCenter),
                        elidedText,
                    ).width()
                    textRect = QRect(
                        availableX,
                        fgRect.y(),
                        elidedW,
                        fgRect.height(),
                    )
                    textFlags = int(
                        Qt.AlignmentFlag.AlignVCenter
                        | Qt.AlignmentFlag.AlignBaseline
                        | Qt.TextFlag.TextSingleLine
                        | Qt.TextFlag.TextHideMnemonic
                    )
                    if iconSize.isEmpty() or not showIcon:
                        textFlags |= int(
                            Qt.AlignmentFlag.AlignHCenter
                        )
                    else:
                        textFlags |= int(
                            Qt.AlignmentFlag.AlignLeft
                        )
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(fgColor)
                    p.drawText(
                        textRect, textFlags, elidedText
                    )
            return

        if ce == CE.CE_Header:
            if isinstance(
                opt, QtWidgets.QStyleOptionHeader
            ):
                self.drawControl(
                    CE.CE_HeaderSection, opt, p, w
                )
                optLabel = QtWidgets.QStyleOptionHeader(opt)
                optLabel.rect = self.subElementRect(
                    SE.SE_HeaderLabel, opt, w
                )
                if optLabel.rect.isValid():
                    self.drawControl(
                        CE.CE_HeaderLabel, optLabel, p, w
                    )
                if (
                    opt.sortIndicator
                    != QtWidgets.QStyleOptionHeader.SortIndicator.None_
                ):
                    optInd = QtWidgets.QStyleOptionHeader(opt)
                    optInd.rect = self.subElementRect(
                        SE.SE_HeaderArrow, opt, w
                    )
                    self.drawPrimitive(
                        PE.PE_IndicatorHeaderArrow,
                        optInd,
                        p,
                        w,
                    )
            return

        if ce == CE.CE_HeaderSection:
            if isinstance(
                opt, QtWidgets.QStyleOptionHeader
            ):
                wParent = (
                    w.parentWidget() if w else None
                )
                tableView = (
                    wParent
                    if isinstance(wParent, QTableView)
                    else None
                )
                treeView = (
                    wParent
                    if isinstance(wParent, QTreeView)
                    else None
                )
                horizontalHeader = (
                    tableView.horizontalHeader()
                    if tableView
                    else (
                        treeView.header()
                        if treeView
                        else None
                    )
                )
                verticalHeader = (
                    tableView.verticalHeader()
                    if tableView
                    else None
                )
                isVertical = (
                    opt.orientation == Qt.Orientation.Vertical
                )
                isHorizontal = (
                    opt.orientation
                    == Qt.Orientation.Horizontal
                )
                rect = opt.rect
                SectionPos = (
                    QtWidgets.QStyleOptionHeader.SectionPosition
                )
                shadow = (
                    tableView.frameShadow()
                    if tableView
                    else (
                        treeView.frameShadow()
                        if treeView
                        else QFrame.Shadow.Sunken
                    )
                )
                drawExtBorders = (
                    shadow != QFrame.Shadow.Plain
                )
                mouse = getMouseState(opt.state)
                checked = getCheckState(opt.state)
                bgColor = self.tableHeaderBgColor(
                    mouse, checked
                )
                p.fillRect(rect, bgColor)
                lineColor = self.tableLineColor()
                lineW = theme.borderWidth
                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing, False
                )
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(QPen(lineColor, lineW))

                drawTop = (
                    drawExtBorders
                    or (
                        isVertical
                        and opt.position
                        == SectionPos.Beginning
                    )
                    or (
                        isHorizontal
                        and opt.position
                        != SectionPos.Beginning
                    )
                )
                if drawTop:
                    hHdrHidden = (
                        horizontalHeader.isHidden()
                        if horizontalHeader
                        else True
                    )
                    if isHorizontal or (
                        hHdrHidden
                        and opt.position
                        == SectionPos.Beginning
                    ):
                        p.drawLine(
                            QPointF(
                                rect.x(),
                                rect.y() + lineW * 0.5,
                            ),
                            QPointF(
                                rect.x() + rect.width(),
                                rect.y() + lineW * 0.5,
                            ),
                        )

                drawRight = (
                    drawExtBorders
                    or isVertical
                    or (
                        isHorizontal
                        and opt.position == SectionPos.End
                    )
                )
                if drawRight:
                    p.drawLine(
                        QPointF(
                            rect.x()
                            + rect.width()
                            - lineW * 0.5,
                            rect.y(),
                        ),
                        QPointF(
                            rect.x()
                            + rect.width()
                            - lineW * 0.5,
                            rect.y() + rect.height(),
                        ),
                    )

                drawBottom = (
                    drawExtBorders
                    or (
                        isVertical
                        and opt.position != SectionPos.End
                    )
                    or isHorizontal
                )
                if drawBottom:
                    p.drawLine(
                        QPointF(
                            rect.x(),
                            rect.y()
                            + rect.height()
                            - lineW * 0.5,
                        ),
                        QPointF(
                            rect.x() + rect.width(),
                            rect.y()
                            + rect.height()
                            - lineW * 0.5,
                        ),
                    )

                drawLeft = (
                    drawExtBorders
                    or (
                        isHorizontal
                        and opt.position
                        == SectionPos.Beginning
                    )
                )
                if drawLeft:
                    vHdrHidden = (
                        verticalHeader.isHidden()
                        if verticalHeader
                        else True
                    )
                    if (
                        isVertical
                        or (
                            isHorizontal
                            and opt.position
                            == SectionPos.OnlyOneSection
                        )
                        or (
                            vHdrHidden
                            and opt.position
                            == SectionPos.Beginning
                        )
                    ):
                        p.drawLine(
                            QPointF(
                                rect.x() + lineW * 0.5,
                                rect.y(),
                            ),
                            QPointF(
                                rect.x() + lineW * 0.5,
                                rect.y() + rect.height(),
                            ),
                        )
            return

        if ce == CE.CE_HeaderLabel:
            if isinstance(
                opt, QtWidgets.QStyleOptionHeader
            ):
                rect = opt.rect
                iconExtent = self.pixelMetric(
                    PM.PM_SmallIconSize, opt
                )
                spacing = theme.spacing
                SortInd = (
                    QtWidgets.QStyleOptionHeader.SortIndicator
                )
                hasArrow = (
                    opt.sortIndicator != SortInd.None_
                )
                arrowSpace = spacing // 2 + iconExtent
                maxLabelX = (
                    rect.x() + rect.width() - arrowSpace
                    if hasArrow
                    else rect.x() + rect.width()
                )
                headerAlignment = opt.textAlignment
                text = opt.text
                headerSelected = bool(
                    opt.state & State.State_On
                )
                font = QFont(p.font())
                if headerSelected:
                    font.setBold(True)
                p.setFont(font)
                fm = QFontMetrics(font)
                availableW = rect.width()
                icon = opt.icon
                hasIcon = not icon.isNull()
                iconSpace = (
                    spacing + iconExtent
                    if hasIcon
                    else 0
                )
                textAvailW = availableW - iconSpace - (
                    arrowSpace
                    if hasArrow
                    and headerAlignment
                    & Qt.AlignmentFlag.AlignRight
                    else 0
                )
                textTheoW = fm.size(
                    Qt.TextFlag.TextSingleLine, text
                ).width()
                textW = min(textTheoW, textAvailW)
                labelW = textW + (
                    iconSpace if hasIcon else 0
                )
                labelY = rect.y()
                labelH = rect.height()
                labelX = rect.x()
                if (
                    headerAlignment
                    & Qt.AlignmentFlag.AlignRight
                ):
                    labelX = (
                        rect.x()
                        + rect.width()
                        - labelW
                        - (
                            arrowSpace
                            if hasArrow
                            and headerAlignment
                            & Qt.AlignmentFlag.AlignRight
                            else 0
                        )
                    )
                elif (
                    headerAlignment
                    & Qt.AlignmentFlag.AlignHCenter
                ):
                    labelX = (
                        rect.x()
                        + (rect.width() - labelW) // 2
                    )

                mouse = getMouseState(opt.state)
                checked = getCheckState(opt.state)
                fgColor = self.tableHeaderFgColor(
                    mouse, checked
                )

                if hasIcon and availableW > iconExtent:
                    iconX = labelX
                    iconY = (
                        labelY
                        + (labelH - iconExtent) // 2
                    )
                    iconRect = QRect(
                        iconX, iconY, iconExtent, iconExtent
                    )
                    if (
                        not hasArrow
                        or iconRect.right() <= maxLabelX
                    ):
                        p.drawPixmap(
                            iconRect,
                            icon.pixmap(
                                QSize(iconExtent, iconExtent)
                            ),
                        )

                if textW > 0:
                    textX = labelX + iconSpace
                    textRect = QRect(
                        textX, labelY, textW, labelH
                    )
                    if (
                        hasArrow
                        and textRect.right() > maxLabelX
                    ):
                        textRect.setRight(
                            min(maxLabelX, textRect.right())
                        )
                    elidedText = fm.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        textRect.width(),
                        Qt.TextFlag.TextSingleLine,
                    )
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(fgColor)
                    textHAlign = (
                        Qt.AlignmentFlag.AlignRight
                        if headerAlignment
                        & Qt.AlignmentFlag.AlignRight
                        and textTheoW < textAvailW
                        else Qt.AlignmentFlag.AlignLeft
                    )
                    textFlags = int(
                        Qt.AlignmentFlag.AlignVCenter
                        | Qt.TextFlag.TextSingleLine
                        | textHAlign
                    )
                    p.drawText(
                        textRect, textFlags, elidedText
                    )
            return

        if ce == CE.CE_HeaderEmptyArea:
            bgColor = self.tableHeaderBgColor(
                MouseState.Normal, CheckState.NotChecked
            )
            p.fillRect(opt.rect, bgColor)
            return

        if ce == CE.CE_Splitter:
            maxThk = 2
            minThk = 1
            rect = opt.rect
            mouse = getMouseState(opt.state)
            lineColor = self.splitterColor(mouse)
            isHorizontal = bool(
                opt.state & State.State_Horizontal
            )
            raw = (
                rect.width()
                if isHorizontal
                else rect.height()
            )
            lineThk = max(minThk, min(maxThk, raw))
            lineW = (
                lineThk if isHorizontal else rect.width()
            )
            lineH = (
                rect.height()
                if isHorizontal
                else lineThk
            )
            lineX = (
                rect.x()
                + (rect.width() - lineThk) // 2
                if isHorizontal
                else rect.x()
            )
            lineY = (
                rect.y()
                if isHorizontal
                else rect.y()
                + (rect.height() - lineThk) // 2
            )
            lineRect = QRect(lineX, lineY, lineW, lineH)
            p.fillRect(lineRect, lineColor)
            return

        if ce == CE.CE_FocusFrame:
            focusFrame = (
                w
                if isinstance(w, QFocusFrame)
                else None
            )
            if focusFrame:
                monitoredWidget = focusFrame.widget()
                hasFocus = (
                    monitoredWidget.hasFocus()
                    if monitoredWidget
                    else False
                )
                borderW = theme.focusBorderWidth
                optFocus = QtWidgets.QStyleOptionFocusRect()
                optFocus.rect = opt.rect
                optFocus.state = (
                    (opt.state & ~State.State_HasFocus)
                    | (
                        State.State_HasFocus
                        if hasFocus
                        else State(0)
                    )
                )
                radiuses = RadiusesF(theme.borderRadius)

                if isinstance(
                    monitoredWidget, QPushButton
                ):
                    optBtn = QtWidgets.QStyleOptionButton()
                    optBtn.initFrom(monitoredWidget)
                    optFocus.rect = self.subElementRect(
                        SE.SE_PushButtonFocusRect,
                        optBtn,
                        monitoredWidget,
                    )
                    radiuses = RadiusesF(
                        theme.borderRadius
                    )
                elif isinstance(
                    monitoredWidget, QToolButton
                ):
                    optTB = (
                        QtWidgets.QStyleOptionToolButton()
                    )
                    optTB.initFrom(monitoredWidget)
                    optFocus.rect = self.subElementRect(
                        SE.SE_PushButtonFocusRect,
                        optTB,
                        monitoredWidget,
                    )
                    radiuses = RadiusesF(
                        theme.borderRadius
                    )
                elif isinstance(
                    monitoredWidget, QCheckBox
                ) or isinstance(
                    monitoredWidget, QRadioButton
                ):
                    optBtn = QtWidgets.QStyleOptionButton()
                    optBtn.initFrom(monitoredWidget)
                    isCB = isinstance(
                        monitoredWidget, QCheckBox
                    )
                    se = (
                        SE.SE_CheckBoxFocusRect
                        if isCB
                        else SE.SE_RadioButtonFocusRect
                    )
                    optFocus.rect = self.subElementRect(
                        se, optBtn, monitoredWidget
                    )
                    radiuses = RadiusesF(
                        theme.checkBoxBorderRadius
                        if isCB
                        else theme.radioButtonBorderRadius
                    )
                elif isinstance(
                    monitoredWidget, QComboBox
                ):
                    radiuses = RadiusesF(
                        theme.borderRadius
                    )
                elif isinstance(
                    monitoredWidget, QGroupBox
                ):
                    radiuses = RadiusesF(
                        theme.borderRadius
                    )
                elif isinstance(
                    monitoredWidget, QSlider
                ):
                    optSlider = (
                        QtWidgets.QStyleOptionSlider()
                    )
                    optSlider.initFrom(monitoredWidget)
                    optFocus.rect = self.subControlRect(
                        CC.CC_Slider,
                        optSlider,
                        SC.SC_SliderHandle,
                        monitoredWidget,
                    )
                    radiuses = RadiusesF(
                        optFocus.rect.height() / 2.0
                    )
                elif isinstance(
                    monitoredWidget, QDial
                ):
                    optDial = QtWidgets.QStyleOptionSlider()
                    optDial.initFrom(monitoredWidget)
                    optFocus.rect = self.subControlRect(
                        CC.CC_Dial,
                        optDial,
                        SC.SC_DialHandle,
                        monitoredWidget,
                    )
                    radiuses = RadiusesF(
                        optFocus.rect.height() / 2.0
                    )
                elif isinstance(
                    monitoredWidget, QAbstractSpinBox
                ):
                    radiuses = RadiusesF(
                        theme.borderRadius
                    )
                elif isinstance(
                    monitoredWidget, QLineEdit
                ):
                    parentW = (
                        monitoredWidget.parentWidget()
                    )
                    if isinstance(parentW, QAbstractSpinBox):
                        radiuses = RadiusesF(
                            theme.borderRadius
                        )
                    elif isinstance(parentW, QComboBox):
                        radiuses = RadiusesF(
                            theme.borderRadius, 0.0,
                            0.0, theme.borderRadius,
                        )
                    else:
                        radiuses = RadiusesF(
                            theme.borderRadius
                        )

                optFocus.radiuses = radiuses
                self.drawPrimitive(
                    PE.PE_FrameFocusRect,
                    optFocus,
                    p,
                    monitoredWidget,
                )
            return

        # Default: delegate to QCommonStyle
        super().drawControl(ce, opt, p, w)

    # ================================================================
    # drawComplexControl
    # ================================================================

    def drawComplexControl(self, cc, opt, p, w=None):
        theme = self._theme

        # CC_SpinBox
        if cc == CC.CC_SpinBox:
            if isinstance(
                opt, QtWidgets.QStyleOptionSpinBox
            ):
                parentWidget = (
                    w.parentWidget() if w else None
                )
                isTabCellEditor = (
                    parentWidget is not None
                    and isinstance(
                        parentWidget.parentWidget()
                        if parentWidget
                        else None,
                        QAbstractItemView,
                    )
                )

                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing, True
                )
                spinBoxEnabled = bool(
                    opt.state & State.State_Enabled
                )
                noButtons = (
                    opt.buttonSymbols
                    == QAbstractSpinBox.ButtonSymbols.NoButtons
                )
                if not noButtons:
                    radius = float(theme.borderRadius)

                    # Up button
                    upBtnRect = self.subControlRect(
                        cc, opt, SC.SC_SpinBoxUp, w
                    )
                    if upBtnRect.isValid():
                        upActive = bool(
                            opt.activeSubControls
                            & SC.SC_SpinBoxUp
                        )
                        upRadiuses = (
                            RadiusesF(0.0)
                            if isTabCellEditor
                            else RadiusesF(
                                0.0, radius, 0.0, 0.0
                            )
                        )
                        upPath = getMultipleRadiusesRectPath(
                            upBtnRect, upRadiuses
                        )
                        upEnabled = spinBoxEnabled and bool(
                            opt.stepEnabled
                            & QAbstractSpinBox.StepEnabledFlag.StepUpEnabled
                        )
                        upHovered = upActive
                        upPressed = upActive and bool(
                            opt.state & State.State_Sunken
                        )
                        upMouse = getMouseState(
                            upPressed, upHovered, upEnabled
                        )
                        upBgColor = (
                            self.spinBoxButtonBackgroundColor(
                                upMouse
                            )
                        )
                        p.setPen(Qt.PenStyle.NoPen)
                        p.setBrush(upBgColor)
                        p.drawPath(upPath)

                        # Up icon
                        fgColor = (
                            self.spinBoxButtonForegroundColor(
                                upMouse
                            )
                        )
                        iconSz = theme.iconSize / 2
                        translateY = theme.borderWidth
                        p.setPen(
                            QPen(
                                fgColor,
                                iconPenWidth,
                                Qt.PenStyle.SolidLine,
                                Qt.PenCapStyle.FlatCap,
                            )
                        )
                        p.setBrush(Qt.BrushStyle.NoBrush)
                        drawSpinBoxArrowIndicator(
                            upBtnRect.translated(
                                0, translateY
                            ),
                            p,
                            opt.buttonSymbols,
                            SC.SC_SpinBoxUp,
                            iconSz,
                        )

                    # Down button
                    downBtnRect = self.subControlRect(
                        cc, opt, SC.SC_SpinBoxDown, w
                    )
                    if downBtnRect.isValid():
                        downActive = bool(
                            opt.activeSubControls
                            & SC.SC_SpinBoxDown
                        )
                        downRadiuses = RadiusesF(
                            0.0, 0.0, radius, 0.0
                        )
                        downPath = (
                            getMultipleRadiusesRectPath(
                                downBtnRect, downRadiuses
                            )
                        )
                        downEnabled = (
                            spinBoxEnabled
                            and bool(
                                opt.stepEnabled
                                & QAbstractSpinBox.StepEnabledFlag.StepDownEnabled
                            )
                        )
                        downHovered = downActive
                        downPressed = downActive and bool(
                            opt.state & State.State_Sunken
                        )
                        downMouse = getMouseState(
                            downPressed,
                            downHovered,
                            downEnabled,
                        )
                        downBgColor = (
                            self.spinBoxButtonBackgroundColor(
                                downMouse
                            )
                        )
                        p.setPen(Qt.PenStyle.NoPen)
                        p.setBrush(downBgColor)
                        p.drawPath(downPath)

                        # Down icon
                        fgColor = (
                            self.spinBoxButtonForegroundColor(
                                downMouse
                            )
                        )
                        iconSz = theme.iconSize / 2
                        p.setPen(
                            QPen(
                                fgColor,
                                iconPenWidth,
                                Qt.PenStyle.SolidLine,
                                Qt.PenCapStyle.FlatCap,
                            )
                        )
                        p.setBrush(Qt.BrushStyle.NoBrush)
                        drawSpinBoxArrowIndicator(
                            downBtnRect,
                            p,
                            opt.buttonSymbols,
                            SC.SC_SpinBoxDown,
                            iconSz,
                        )
            return

        # CC_ComboBox
        if cc == CC.CC_ComboBox:
            if isinstance(
                opt, QtWidgets.QStyleOptionComboBox
            ):
                if opt.editable:
                    arrowBtnRect = self.subControlRect(
                        CC.CC_ComboBox,
                        opt,
                        SC.SC_ComboBoxArrow,
                        w,
                    )
                    buttonOpt = (
                        QtWidgets.QStyleOptionButton()
                    )
                    buttonOpt.rect = arrowBtnRect
                    buttonOpt.fontMetrics = opt.fontMetrics
                    buttonOpt.palette = opt.palette
                    buttonOpt.state = (
                        opt.state & ~State.State_On
                    )
                    if not opt.frame:
                        buttonOpt.features = (
                            QtWidgets.QStyleOptionButton.ButtonFeature.Flat
                        )
                    buttonOpt.radiuses = RadiusesF(
                        0.0, theme.borderRadius
                    )
                    self.drawControl(
                        CE.CE_PushButtonBevel,
                        buttonOpt,
                        p,
                        w,
                    )

                    # Arrow indicator
                    mouse = getMouseState(opt.state)
                    fgColor = self.comboBoxForegroundColor(
                        mouse
                    )
                    indicatorSize = theme.iconSize
                    indicatorX = arrowBtnRect.x() + (
                        arrowBtnRect.width()
                        - indicatorSize.width()
                    ) // 2
                    indicatorY = arrowBtnRect.y() + (
                        arrowBtnRect.height()
                        - indicatorSize.height()
                    ) // 2
                    indicatorRect = QRect(
                        QPoint(indicatorX, indicatorY),
                        indicatorSize,
                    )

                    if isinstance(w, QDateTimeEdit):
                        pixelRatio = getPixelRatio(w)
                        icon = self.standardIconExt(
                            self.StandardPixmapExt.SP_Calendar,
                            indicatorSize * pixelRatio,
                        )
                        drawIcon(
                            indicatorRect,
                            p,
                            icon,
                            mouse,
                            CheckState.Checked,
                            w,
                            True,
                            fgColor,
                        )
                    else:
                        p.setBrush(Qt.BrushStyle.NoBrush)
                        p.setPen(
                            QPen(
                                fgColor,
                                iconPenWidth,
                                Qt.PenStyle.SolidLine,
                                Qt.PenCapStyle.FlatCap,
                            )
                        )
                        drawComboBoxIndicator(
                            indicatorRect, p
                        )
                else:
                    parentWidget = (
                        w.parentWidget() if w else None
                    )
                    isTabCellEditor = (
                        parentWidget is not None
                        and isinstance(
                            parentWidget.parentWidget()
                            if parentWidget
                            else None,
                            QAbstractItemView,
                        )
                    )
                    buttonOpt = (
                        QtWidgets.QStyleOptionButton()
                    )
                    buttonOpt.rect = opt.rect
                    buttonOpt.fontMetrics = opt.fontMetrics
                    buttonOpt.palette = opt.palette
                    buttonOpt.state = (
                        opt.state & ~State.State_On
                    )
                    if not opt.frame:
                        buttonOpt.features = (
                            QtWidgets.QStyleOptionButton.ButtonFeature.Flat
                        )
                    buttonOpt.radiuses = RadiusesF(
                        0.0
                        if isTabCellEditor
                        else theme.borderRadius
                    )
                    self.drawControl(
                        CE.CE_PushButtonBevel,
                        buttonOpt,
                        p,
                        w,
                    )
            return

        # CC_ScrollBar
        if cc == CC.CC_ScrollBar:
            if isinstance(
                opt, QtWidgets.QStyleOptionSlider
            ):
                mouse = getMouseState(opt.state)
                horizontal = (
                    opt.orientation
                    == Qt.Orientation.Horizontal
                )
                thickness = float(
                    self.getScrollBarThickness(mouse)
                )
                scrollBarMargin = theme.scrollBarMargin

                # Groove
                grooveRect = self.subControlRect(
                    CC.CC_ScrollBar,
                    opt,
                    SC.SC_ScrollBarGroove,
                    w,
                )
                if horizontal:
                    currentGrooveRect = QRectF(
                        grooveRect.x(),
                        grooveRect.y()
                        + grooveRect.height()
                        - thickness,
                        grooveRect.width(),
                        thickness,
                    )
                else:
                    currentGrooveRect = QRectF(
                        grooveRect.x()
                        + grooveRect.width()
                        - thickness,
                        grooveRect.y(),
                        thickness,
                        grooveRect.height(),
                    )

                grooveColor = self.scrollBarGrooveColor(
                    mouse
                )
                if scrollBarMargin <= 0:
                    grooveRadius = 0.0
                elif horizontal:
                    grooveRadius = (
                        currentGrooveRect.height() / 2.0
                    )
                else:
                    grooveRadius = (
                        currentGrooveRect.width() / 2.0
                    )
                p.setRenderHint(
                    QPainter.RenderHint.Antialiasing, True
                )
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(grooveColor)
                p.drawRoundedRect(
                    currentGrooveRect,
                    grooveRadius,
                    grooveRadius,
                )

                # Handle
                handleRect = self.subControlRect(
                    CC.CC_ScrollBar,
                    opt,
                    SC.SC_ScrollBarSlider,
                    w,
                )
                if not handleRect.isEmpty():
                    if horizontal:
                        currentHandleRect = QRectF(
                            handleRect.x(),
                            handleRect.y()
                            + handleRect.height()
                            - thickness,
                            handleRect.width(),
                            thickness,
                        )
                    else:
                        currentHandleRect = QRectF(
                            handleRect.x()
                            + handleRect.width()
                            - thickness,
                            handleRect.y(),
                            thickness,
                            handleRect.height(),
                        )
                    handleMouse = getScrollBarHandleState(
                        opt.state, opt.activeSubControls
                    )
                    handleColor = (
                        self.scrollBarHandleColor(
                            handleMouse
                        )
                    )
                    handleRadius = (
                        currentHandleRect.height() / 2.0
                        if horizontal
                        else currentHandleRect.width()
                        / 2.0
                    )
                    p.setBrush(handleColor)
                    p.drawRoundedRect(
                        currentHandleRect,
                        handleRadius,
                        handleRadius,
                    )
            return

        # CC_Slider
        if cc == CC.CC_Slider:
            if isinstance(
                opt, QtWidgets.QStyleOptionSlider
            ):
                slMin = opt.minimum
                slMax = opt.maximum
                widgetMouse = getMouseState(opt.state)
                mouse = (
                    MouseState.Disabled
                    if widgetMouse == MouseState.Disabled
                    else MouseState.Normal
                )
                # No animation; use sliderPosition directly
                currentProgress = float(
                    opt.sliderPosition
                )
                handleRect = self.subControlRect(
                    CC.CC_Slider, opt, SC.SC_SliderHandle, w
                )
                disabled = mouse == MouseState.Disabled

                # Tickmarks
                if (
                    opt.subControls & SC.SC_SliderTickmarks
                    and opt.tickPosition
                    != QSlider.TickPosition.NoTicks
                ):
                    tickmarksRect = self.subControlRect(
                        cc, opt, SC.SC_SliderTickmarks, w
                    )
                    tickThickness = theme.sliderTickThickness
                    tickColor = self.sliderTickColor(mouse)
                    if disabled:
                        p.save()
                        clipRegion = QRegion(tickmarksRect)
                        clipRegion = clipRegion.subtracted(
                            handleRect.adjusted(1, 0, -1, 0)
                        )
                        p.setClipRegion(clipRegion)
                    drawSliderTickMarks(
                        p,
                        tickmarksRect,
                        tickColor,
                        slMin,
                        slMax,
                        opt.tickInterval,
                        tickThickness,
                        opt.singleStep,
                        opt.pageStep,
                    )
                    if disabled:
                        p.restore()

                # Groove and value
                grooveRect = self.subControlRect(
                    cc, opt, SC.SC_SliderGroove, w
                )
                if (
                    opt.subControls & SC.SC_SliderGroove
                    and grooveRect.isValid()
                ):
                    grooveColor = self.sliderGrooveColor(
                        mouse
                    )
                    valueColor = self.sliderValueColor(mouse)
                    radius = grooveRect.height() / 2.0
                    if disabled:
                        p.save()
                        clipRegion = QRegion(grooveRect)
                        clipRegion = clipRegion.subtracted(
                            handleRect.adjusted(1, 0, -1, 0)
                        )
                        p.setClipRegion(clipRegion)
                    drawRoundedRect(
                        p, grooveRect, grooveColor, radius
                    )
                    if disabled:
                        p.restore()
                    valueRect = grooveRect.adjusted(
                        0,
                        0,
                        -handleRect.width() + 1,
                        0,
                    )
                    drawProgressBarValueRect(
                        p,
                        valueRect,
                        valueColor,
                        slMin,
                        slMax,
                        currentProgress,
                        radius,
                    )

                # Handle
                if (
                    opt.subControls & SC.SC_SliderHandle
                    and handleRect.isValid()
                ):
                    handleMouse = (
                        widgetMouse
                        if opt.activeSubControls
                        == SC.SC_SliderHandle
                        else mouse
                    )
                    handleBgColor = self.sliderHandleColor(
                        handleMouse
                    )
                    p.setRenderHint(
                        QPainter.RenderHint.Antialiasing,
                        True,
                    )
                    # Skip drop shadow for simplicity
                    p.setPen(Qt.PenStyle.NoPen)
                    p.setBrush(handleBgColor)
                    p.drawEllipse(handleRect)
            return

        # CC_ToolButton
        if cc == CC.CC_ToolButton:
            if isinstance(
                opt, QtWidgets.QStyleOptionToolButton
            ):
                hasMenu = bool(
                    opt.features
                    & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.HasMenu
                )
                menuOnSep = hasMenu and bool(
                    opt.features
                    & QtWidgets.QStyleOptionToolButton.ToolButtonFeature.MenuButtonPopup
                )
                isMouseOver = bool(
                    opt.state & State.State_MouseOver
                )
                isPressed = bool(
                    opt.state & State.State_Sunken
                )
                parentTabBar = None
                if w and w.parentWidget():
                    pw = w.parentWidget()
                    if isinstance(pw, QTabBar):
                        parentTabBar = pw
                isTabBarScrollButton = (
                    parentTabBar is not None
                    and opt.arrowType
                    != Qt.ArrowType.NoArrow
                )
                radius = theme.borderRadius
                buttonActive = bool(
                    opt.activeSubControls
                    & SC.SC_ToolButton
                )
                menuButtonActive = menuOnSep and bool(
                    opt.activeSubControls
                    & SC.SC_ToolButtonMenu
                )
                mouse = getMouseState(opt.state)
                buttonRect = self.subControlRect(
                    CC.CC_ToolButton,
                    opt,
                    SC.SC_ToolButton,
                    w,
                )
                menuButtonRect = self.subControlRect(
                    CC.CC_ToolButton,
                    opt,
                    SC.SC_ToolButtonMenu,
                    w,
                )

                # Tweak the button state
                buttonState = opt.state
                if menuOnSep:
                    if (
                        isMouseOver and buttonActive
                    ) or (isPressed and menuButtonActive):
                        buttonState = (
                            buttonState
                            | State.State_MouseOver
                        )
                    else:
                        buttonState = (
                            buttonState
                            & ~State.State_MouseOver
                        )
                    if isPressed and buttonActive:
                        buttonState = (
                            buttonState
                            | State.State_Sunken
                        )
                    else:
                        buttonState = (
                            buttonState
                            & ~State.State_Sunken
                        )
                    if isMouseOver and menuButtonActive:
                        buttonState = (
                            buttonState
                            | State.State_Raised
                        )
                    else:
                        buttonState = (
                            buttonState
                            & ~State.State_Raised
                        )

                # Main button
                buttonOpt = (
                    QtWidgets.QStyleOptionToolButton(opt)
                )
                buttonOpt.state = buttonState

                if isTabBarScrollButton:
                    buttonOpt.state = (
                        buttonOpt.state | State.State_Raised
                    )
                    isLeftButton = (
                        opt.arrowType
                        == Qt.ArrowType.LeftArrow
                    )
                    tabBarState = (
                        MouseState.Normal
                        if parentTabBar.isEnabled()
                        else MouseState.Disabled
                    )
                    bgColor = self.tabBarBackgroundColor(
                        tabBarState
                    )
                    if (
                        parentTabBar.documentMode()
                        or isLeftButton
                    ):
                        p.fillRect(opt.rect, bgColor)
                    else:
                        bgRadius = (
                            theme.borderRadius * 1.5
                        )
                        drawRoundedRect(
                            p,
                            opt.rect,
                            bgColor,
                            RadiusesF(
                                0.0, bgRadius, 0.0, 0.0
                            ),
                        )
                    spacing = theme.spacing
                    buttonSize = QSize(
                        theme.controlHeightMedium,
                        theme.controlHeightMedium,
                    )
                    if isLeftButton:
                        buttonX = (
                            buttonRect.x()
                            + buttonRect.width()
                            - buttonSize.width()
                            - spacing // 2
                        )
                    else:
                        buttonX = (
                            buttonRect.x() + spacing // 2
                        )
                    buttonY = buttonRect.y() + (
                        buttonRect.height()
                        - buttonSize.height()
                    ) // 2
                    buttonOpt.rect = QRect(
                        QPoint(buttonX, buttonY),
                        buttonSize,
                    )
                    stdIcon = (
                        QStyle.StandardPixmap.SP_ArrowLeft
                        if isLeftButton
                        else QStyle.StandardPixmap.SP_ArrowRight
                    )
                    buttonOpt.icon = self.standardIcon(
                        stdIcon, buttonOpt, w
                    )
                    self.drawPrimitive(
                        PE.PE_PanelButtonTool,
                        buttonOpt,
                        p,
                        w,
                    )
                    self.drawControl(
                        CE.CE_ToolButtonLabel,
                        buttonOpt,
                        p,
                        w,
                    )
                else:
                    buttonOpt.rect = (
                        buttonRect
                        if menuOnSep
                        else opt.rect
                    )
                    self.drawPrimitive(
                        PE.PE_PanelButtonTool,
                        buttonOpt,
                        p,
                        w,
                    )
                    buttonOpt.rect = buttonRect
                    self.drawControl(
                        CE.CE_ToolButtonLabel,
                        buttonOpt,
                        p,
                        w,
                    )

                # Menu arrow (separate button)
                if menuOnSep:
                    menuBtnRadiuses = (
                        RadiusesF(
                            0.0, radius, radius, 0.0
                        )
                        if hasMenu
                        else RadiusesF()
                    )
                    menuButtonState = opt.state
                    if (
                        isMouseOver and menuButtonActive
                    ) or (isPressed and buttonActive):
                        menuButtonState = (
                            menuButtonState
                            | State.State_MouseOver
                        )
                    else:
                        menuButtonState = (
                            menuButtonState
                            & ~State.State_MouseOver
                        )
                    if isPressed and menuButtonActive:
                        menuButtonState = (
                            menuButtonState
                            | State.State_Sunken
                        )
                    else:
                        menuButtonState = (
                            menuButtonState
                            & ~State.State_Sunken
                        )
                    if isMouseOver and buttonActive:
                        menuButtonState = (
                            menuButtonState
                            | State.State_Raised
                        )
                    else:
                        menuButtonState = (
                            menuButtonState
                            & ~State.State_Raised
                        )
                    # Background
                    menuBtnMouse = (
                        getToolButtonMouseState(
                            menuButtonState
                        )
                    )
                    role = getColorRole(opt.state, False)
                    bgColor = (
                        self.toolButtonBackgroundColor(
                            menuBtnMouse, role
                        )
                    )
                    drawRoundedRect(
                        p,
                        menuButtonRect,
                        bgColor,
                        menuBtnRadiuses,
                    )
                    # Line
                    lineW = theme.borderWidth
                    lineColor = (
                        self.toolButtonSeparatorColor(
                            mouse, role
                        )
                    )
                    lineX = (
                        buttonRect.x()
                        + buttonRect.width()
                        - lineW / 2.0
                    )
                    lineY1 = float(buttonRect.y())
                    lineY2 = float(
                        buttonRect.y()
                        + buttonRect.height()
                    )
                    p.setBrush(Qt.BrushStyle.NoBrush)
                    p.setPen(
                        QPen(
                            lineColor,
                            lineW,
                            Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.FlatCap,
                        )
                    )
                    p.drawLine(
                        QPointF(lineX, lineY1),
                        QPointF(lineX, lineY2),
                    )
                    # Arrow
                    arrowSize = theme.iconSize
                    arrowX = menuButtonRect.x() + (
                        menuButtonRect.width()
                        - arrowSize.width()
                    ) // 2
                    arrowY = menuButtonRect.y() + (
                        menuButtonRect.height()
                        - arrowSize.height()
                    ) // 2
                    arrowRect = QRect(
                        arrowX,
                        arrowY,
                        arrowSize.width(),
                        arrowSize.height(),
                    )
                    arrowColor = (
                        self.toolButtonForegroundColor(
                            menuBtnMouse, role
                        )
                    )
                    path = getMenuIndicatorPath(arrowRect)
                    p.setPen(
                        QPen(
                            arrowColor,
                            iconPenWidth,
                            Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap,
                        )
                    )
                    p.drawPath(path)
                elif hasMenu:
                    spacing = theme.spacing
                    arrowSize = theme.iconSize
                    arrowX = (
                        menuButtonRect.x()
                        + (
                            menuButtonRect.width()
                            - arrowSize.width()
                        )
                        // 2
                        - spacing
                    )
                    arrowY = menuButtonRect.y() + (
                        menuButtonRect.height()
                        - arrowSize.height()
                    ) // 2
                    arrowRect = QRect(
                        arrowX,
                        arrowY,
                        arrowSize.width(),
                        arrowSize.height(),
                    )
                    arrowColor = (
                        self.toolButtonForegroundColor(
                            mouse,
                            getColorRole(opt.state, False),
                        )
                    )
                    path = getMenuIndicatorPath(arrowRect)
                    p.setPen(
                        QPen(
                            arrowColor,
                            iconPenWidth,
                            Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap,
                        )
                    )
                    p.drawPath(path)
            return

        # CC_Dial
        if cc == CC.CC_Dial:
            if isinstance(
                opt, QtWidgets.QStyleOptionSlider
            ):
                dMin = opt.minimum
                dMax = opt.maximum
                mouse = getMouseState(opt.state)
                currentProgress = float(
                    opt.sliderPosition
                )

                # Tickmarks
                if opt.subControls & SC.SC_DialTickmarks:
                    tickmarksRect = self.subControlRect(
                        cc, opt, SC.SC_DialTickmarks, w
                    )
                    tickThickness = theme.dialMarkThickness
                    tickColor = self.dialTickColor(mouse)
                    tickLength = theme.dialTickLength
                    minArcLength = int(
                        opt.notchTarget * 2
                    )
                    drawDialTickMarks(
                        p,
                        tickmarksRect,
                        tickColor,
                        dMin,
                        dMax,
                        tickThickness,
                        tickLength,
                        opt.singleStep,
                        opt.pageStep,
                        minArcLength,
                    )

                # Dial shape
                dialRect = self.subControlRect(
                    cc, opt, SC.SC_DialGroove, w
                )
                bgColor = self.dialBackgroundColor(mouse)
                handleColor = self.dialHandleColor(mouse)
                grooveColor = self.dialGrooveColor(mouse)
                valueColor = self.dialValueColor(mouse)
                markColor = self.dialMarkColor(mouse)
                drawDial(
                    p,
                    dialRect,
                    dMin,
                    dMax,
                    currentProgress,
                    bgColor,
                    handleColor,
                    grooveColor,
                    valueColor,
                    markColor,
                    theme.dialGrooveThickness,
                    theme.dialMarkLength,
                    theme.dialMarkThickness,
                )
            return

        # CC_GroupBox
        if cc == CC.CC_GroupBox:
            if isinstance(
                opt, QtWidgets.QStyleOptionGroupBox
            ):
                # Checkbox
                if opt.subControls & SC.SC_GroupBoxCheckBox:
                    checkBoxRect = self.subControlRect(
                        CC.CC_GroupBox,
                        opt,
                        SC.SC_GroupBoxCheckBox,
                        w,
                    )
                    checkBoxOpt = (
                        QtWidgets.QStyleOptionButton()
                    )
                    checkBoxOpt.rect = checkBoxRect
                    checkBoxOpt.state = opt.state
                    checkBoxOpt.palette = opt.palette
                    self.drawPrimitive(
                        PE.PE_IndicatorCheckBox,
                        checkBoxOpt,
                        p,
                        w,
                    )

                # Title
                if opt.subControls & SC.SC_GroupBoxLabel:
                    textRect = self.subControlRect(
                        CC.CC_GroupBox,
                        opt,
                        SC.SC_GroupBoxLabel,
                        w,
                    )
                    font = theme.fontH5
                    fm = QFontMetrics(font)
                    elidedText = fm.elidedText(
                        opt.text,
                        Qt.TextElideMode.ElideRight,
                        textRect.width(),
                        Qt.TextFlag.TextSingleLine,
                    )
                    mouse = getMouseState(opt.state)
                    textColor = self.groupBoxTitleColor(
                        mouse, w
                    )
                    textFlags = (
                        Qt.AlignmentFlag.AlignVCenter
                        | Qt.AlignmentFlag.AlignBaseline
                        | Qt.TextFlag.TextSingleLine
                        | Qt.AlignmentFlag.AlignLeft
                        | Qt.TextFlag.TextHideMnemonic
                    )
                    p.setFont(font)
                    p.setPen(textColor)
                    p.setRenderHint(
                        QPainter.RenderHint.Antialiasing,
                        True,
                    )
                    p.drawText(
                        textRect,
                        int(textFlags),
                        elidedText,
                    )

                # Frame
                hasFrame = not bool(
                    opt.features
                    & QtWidgets.QStyleOptionFrame.FrameFeature.Flat
                )
                if hasFrame:
                    frameRect = self.subControlRect(
                        CC.CC_GroupBox,
                        opt,
                        SC.SC_GroupBoxFrame,
                        w,
                    )
                    frameOpt = QtWidgets.QStyleOptionFrame()
                    frameOpt.rect = frameRect
                    frameOpt.features = opt.features
                    frameOpt.state = opt.state
                    frameOpt.palette = opt.palette
                    checked = getCheckState(opt.state)
                    if (
                        checked == CheckState.NotChecked
                        and opt.subControls
                        & SC.SC_GroupBoxCheckBox
                    ):
                        frameOpt.state = (
                            frameOpt.state
                            & ~State.State_Enabled
                        )
                    self.drawPrimitive(
                        PE.PE_FrameGroupBox,
                        frameOpt,
                        p,
                        w,
                    )
            return

        # CC_TitleBar / CC_MdiControls: fall through

        # Default: delegate to QCommonStyle
        super().drawComplexControl(cc, opt, p, w)

    # ================================================================
    # standardIcon / standardPixmap / generatedIconPixmap
    # ================================================================

    def standardIcon(self, sp, opt=None, w=None):
        return super().standardIcon(sp, opt, w)

    def standardPixmap(self, sp, opt=None, w=None):
        return super().standardPixmap(sp, opt, w)

    def generatedIconPixmap(self, mode, pixmap, opt):
        return super().generatedIconPixmap(mode, pixmap, opt)
