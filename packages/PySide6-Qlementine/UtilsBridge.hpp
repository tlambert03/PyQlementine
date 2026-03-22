// UtilsBridge.hpp — Wrapper class exposing qlementine free functions as static
// methods so that shiboken6 can generate correct bindings.  Shiboken has a
// known limitation where namespace-level free functions produce broken
// overload-resolution code.  Static methods on a class are handled correctly.
//
// Every method simply forwards to the real free function.

#pragma once

#include <QPainterPath>
#include <oclero/qlementine/style/QlementineStyle.hpp>
#include <oclero/qlementine/utils/BadgeUtils.hpp>
#include <oclero/qlementine/utils/ColorUtils.hpp>
#include <oclero/qlementine/utils/FontUtils.hpp>
#include <oclero/qlementine/utils/GeometryUtils.hpp>
#include <oclero/qlementine/utils/IconUtils.hpp>
#include <oclero/qlementine/utils/ImageUtils.hpp>
#include <oclero/qlementine/utils/LayoutUtils.hpp>
#include <oclero/qlementine/utils/MenuUtils.hpp>
#include <oclero/qlementine/utils/PrimitiveUtils.hpp>
#include <oclero/qlementine/utils/StateUtils.hpp>
#include <oclero/qlementine/utils/StyleUtils.hpp>
#include <oclero/qlementine/utils/WidgetUtils.hpp>

namespace oclero::qlementine {

class UtilsBridge {
public:
    // ---- appStyle (from QlementineStyle.hpp) ----
    static QlementineStyle* appStyle() {
        return oclero::qlementine::appStyle();
    }

    // ---- BadgeUtils ----
    static void drawStatusBadge(QPainter* p, const QRect& rect,
        StatusBadge statusBadge, StatusBadgeSize size, const Theme& theme) {
        oclero::qlementine::drawStatusBadge(p, rect, statusBadge, size, theme);
    }

    // ---- ColorUtils ----
    static double getContrastRatio(const QColor& c1, const QColor& c2) {
        return oclero::qlementine::getContrastRatio(c1, c2);
    }
    static QColor colorWithAlphaF(const QColor& color, qreal alpha) {
        return oclero::qlementine::colorWithAlphaF(color, alpha);
    }
    static QColor colorWithAlpha(const QColor& color, int alpha) {
        return oclero::qlementine::colorWithAlpha(color, alpha);
    }
    static QColor getColorSourceOver(const QColor& bg, const QColor& fg) {
        return oclero::qlementine::getColorSourceOver(bg, fg);
    }
    static QString toHexRGB(const QColor& color) {
        return oclero::qlementine::toHexRGB(color);
    }
    static QString toHexRGBA(const QColor& color) {
        return oclero::qlementine::toHexRGBA(color);
    }

    // ---- FontUtils ----
    static double pointSizeToPixelSize(double pointSize, double dpi) {
        return oclero::qlementine::pointSizeToPixelSize(pointSize, dpi);
    }
    static double pixelSizeToPointSize(double pixelSize, double dpi) {
        return oclero::qlementine::pixelSizeToPointSize(pixelSize, dpi);
    }
    static int textWidth(const QFontMetrics& fm, const QString& text) {
        return oclero::qlementine::textWidth(fm, text);
    }

    // ---- GeometryUtils ----
    static bool isPointInRoundedRect(const QPointF& point,
        const QRectF& rect, qreal cornerRadius) {
        return oclero::qlementine::isPointInRoundedRect(point, rect, cornerRadius);
    }

    // ---- IconUtils ----
    static QIcon makeIconFromSvg(const QString& svgPath, const QSize& size) {
        return oclero::qlementine::makeIconFromSvg(svgPath, size);
    }
    static QIcon makeIconFromSvg(const QString& svgPath,
        const IconTheme& iconTheme, const QSize& size = QSize(16, 16)) {
        return oclero::qlementine::makeIconFromSvg(svgPath, iconTheme, size);
    }

    // ---- ImageUtils ----
    static QImage colorizeImage(const QPixmap& input, const QColor& color) {
        return oclero::qlementine::colorizeImage(input, color);
    }
    static QPixmap colorizePixmap(const QPixmap& input, const QColor& color) {
        return oclero::qlementine::colorizePixmap(input, color);
    }
    static QPixmap tintPixmap(const QPixmap& input, const QColor& color) {
        return oclero::qlementine::tintPixmap(input, color);
    }
    static QPixmap getColorizedPixmap(const QPixmap& input, const QColor& color) {
        return oclero::qlementine::getColorizedPixmap(input, color);
    }
    static QPixmap getTintedPixmap(const QPixmap& input, const QColor& color) {
        return oclero::qlementine::getTintedPixmap(input, color);
    }
    static QPixmap getCachedPixmap(const QPixmap& input, const QColor& color,
        ColorizeMode mode) {
        return oclero::qlementine::getCachedPixmap(input, color, mode);
    }
    static QPixmap makePixmapFromSvg(const QString& svgPath, const QSize& size) {
        return oclero::qlementine::makePixmapFromSvg(svgPath, size);
    }
    static QPixmap makePixmapFromSvg(const QString& bgPath,
        const QColor& bgColor, const QString& fgPath, const QColor& fgColor,
        const QSize& size) {
        return oclero::qlementine::makePixmapFromSvg(bgPath, bgColor, fgPath, fgColor, size);
    }
    static QPixmap makeRoundedPixmap(const QPixmap& input, double radius) {
        return oclero::qlementine::makeRoundedPixmap(input, radius);
    }
    static QPixmap makeRoundedPixmap(const QPixmap& input,
        const RadiusesF& radiuses) {
        return oclero::qlementine::makeRoundedPixmap(input, radiuses);
    }
    static QPixmap makeRoundedPixmap(const QPixmap& input,
        double topLeft, double topRight, double bottomRight, double bottomLeft) {
        return oclero::qlementine::makeRoundedPixmap(input, topLeft, topRight, bottomRight, bottomLeft);
    }
    static QPixmap makeFitPixmap(const QPixmap& input, const QSize& size) {
        return oclero::qlementine::makeFitPixmap(input, size);
    }
    static double getImageAspectRatio(const QString& path) {
        return oclero::qlementine::getImageAspectRatio(path);
    }
    static QImage getExtendedImage(const QPixmap& input, int padding) {
        return oclero::qlementine::getExtendedImage(input, padding);
    }
    static QImage getExtendedImage(const QImage& input, int padding) {
        return oclero::qlementine::getExtendedImage(input, padding);
    }
    static QPixmap getBlurredPixmap(const QPixmap& input, double blurRadius) {
        return oclero::qlementine::getBlurredPixmap(input, blurRadius);
    }
    static QPixmap getDropShadowPixmap(const QPixmap& input,
        double blurRadius, const QColor& color = Qt::black) {
        return oclero::qlementine::getDropShadowPixmap(input, blurRadius, color);
    }
    static QPixmap getDropShadowPixmap(const QSize& size,
        double borderRadius, double blurRadius, const QColor& color = Qt::black) {
        return oclero::qlementine::getDropShadowPixmap(size, borderRadius, blurRadius, color);
    }
    static int blurRadiusNecessarySpace(double blurRadius) {
        return oclero::qlementine::blurRadiusNecessarySpace(blurRadius);
    }

    // ---- LayoutUtils ----
    static QMargins getLayoutMargins(const QWidget* widget) {
        return oclero::qlementine::getLayoutMargins(widget);
    }
    static int getLayoutHSpacing(const QWidget* widget) {
        return oclero::qlementine::getLayoutHSpacing(widget);
    }
    static int getLayoutVSpacing(const QWidget* widget) {
        return oclero::qlementine::getLayoutVSpacing(widget);
    }
    static void clearLayout(QLayout* layout) {
        oclero::qlementine::clearLayout(layout);
    }

    // ---- MenuUtils ----
    static QMenu* getTopLevelMenu(QMenu* menu) {
        return oclero::qlementine::getTopLevelMenu(menu);
    }

    // ---- PrimitiveUtils ----
    static double getPixelRatio(const QWidget* w) {
        return oclero::qlementine::getPixelRatio(w);
    }
    static void drawEllipseBorder(QPainter* p, const QRectF& rect,
        const QColor& color, qreal borderWidth) {
        oclero::qlementine::drawEllipseBorder(p, rect, color, borderWidth);
    }
    static QPainterPath getMultipleRadiusesRectPath(const QRectF& rect,
        const RadiusesF& radiuses) {
        return oclero::qlementine::getMultipleRadiusesRectPath(rect, radiuses);
    }
    static void drawRoundedRect(QPainter* p, const QRectF& rect,
        const QBrush& brush, qreal radius = 0.) {
        oclero::qlementine::drawRoundedRect(p, rect, brush, radius);
    }
    static void drawRoundedRect(QPainter* p, const QRectF& rect,
        const QBrush& brush, const RadiusesF& radiuses) {
        oclero::qlementine::drawRoundedRect(p, rect, brush, radiuses);
    }
    static void drawRoundedRect(QPainter* p, const QRect& rect,
        const QBrush& brush, qreal radius = 0.) {
        oclero::qlementine::drawRoundedRect(p, rect, brush, radius);
    }
    static void drawRoundedRect(QPainter* p, const QRect& rect,
        const QBrush& brush, const RadiusesF& radiuses) {
        oclero::qlementine::drawRoundedRect(p, rect, brush, radiuses);
    }
    static void drawRoundedRectBorder(QPainter* p, const QRectF& rect,
        const QColor& color, qreal borderWidth, qreal radius = 0.) {
        oclero::qlementine::drawRoundedRectBorder(p, rect, color, borderWidth, radius);
    }
    static void drawRoundedRectBorder(QPainter* p, const QRect& rect,
        const QColor& color, qreal borderWidth, qreal radius = 0.) {
        oclero::qlementine::drawRoundedRectBorder(p, rect, color, borderWidth, radius);
    }
    static void drawRoundedRectBorder(QPainter* p, const QRectF& rect,
        const QColor& color, qreal borderWidth, const RadiusesF& radiuses) {
        oclero::qlementine::drawRoundedRectBorder(p, rect, color, borderWidth, radiuses);
    }
    static void drawRoundedRectBorder(QPainter* p, const QRect& rect,
        const QColor& color, qreal borderWidth, const RadiusesF& radiuses) {
        oclero::qlementine::drawRoundedRectBorder(p, rect, color, borderWidth, radiuses);
    }
    static void drawRectBorder(QPainter* p, const QRect& rect,
        const QColor& color, qreal borderWidth) {
        oclero::qlementine::drawRectBorder(p, rect, color, borderWidth);
    }
    static void drawRectBorder(QPainter* p, const QRectF& rect,
        const QColor& color, qreal borderWidth) {
        oclero::qlementine::drawRectBorder(p, rect, color, borderWidth);
    }
    static void drawRoundedTriangle(QPainter* p, const QRectF& rect,
        qreal radius = 0.) {
        oclero::qlementine::drawRoundedTriangle(p, rect, radius);
    }
    static void drawCheckerboard(QPainter* p, const QRectF& rect,
        const QColor& darkColor, const QColor& lightColor, qreal cellWidth) {
        oclero::qlementine::drawCheckerboard(p, rect, darkColor, lightColor, cellWidth);
    }
    static void drawProgressBarValueRect(QPainter* p, const QRect& rect,
        const QColor& color, qreal min, qreal max, qreal value,
        qreal radius = 0., bool inverted = false) {
        oclero::qlementine::drawProgressBarValueRect(p, rect, color, min, max, value, radius, inverted);
    }
    static void drawColorMark(QPainter* p, const QRect& rect,
        const QColor& color, const QColor& borderColor, int borderWidth = 1) {
        oclero::qlementine::drawColorMark(p, rect, color, borderColor, borderWidth);
    }
    static void drawColorMarkBorder(QPainter* p, const QRect& rect,
        const QColor& borderColor, int borderWidth) {
        oclero::qlementine::drawColorMarkBorder(p, rect, borderColor, borderWidth);
    }
    static void drawDebugRect(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawDebugRect(rect, p);
    }
    static QPainterPath getMenuIndicatorPath(const QRect& rect) {
        return oclero::qlementine::getMenuIndicatorPath(rect);
    }
    static void drawComboBoxIndicator(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawComboBoxIndicator(rect, p);
    }
    static void drawCheckBoxIndicator(const QRect& rect, QPainter* p,
        qreal progress = 1.) {
        oclero::qlementine::drawCheckBoxIndicator(rect, p, progress);
    }
    static void drawPartiallyCheckedCheckBoxIndicator(const QRect& rect,
        QPainter* p, qreal progress = 1.) {
        oclero::qlementine::drawPartiallyCheckedCheckBoxIndicator(rect, p, progress);
    }
    static void drawRadioButtonIndicator(const QRect& rect, QPainter* p,
        qreal progress = 1.) {
        oclero::qlementine::drawRadioButtonIndicator(rect, p, progress);
    }
    static void drawSpinBoxArrowIndicator(const QRect& rect, QPainter* p,
        QAbstractSpinBox::ButtonSymbols buttonSymbol,
        QStyle::SubControl subControl, const QSize& iconSize) {
        oclero::qlementine::drawSpinBoxArrowIndicator(rect, p, buttonSymbol, subControl, iconSize);
    }
    static void drawArrowRight(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawArrowRight(rect, p);
    }
    static void drawArrowLeft(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawArrowLeft(rect, p);
    }
    static void drawArrowDown(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawArrowDown(rect, p);
    }
    static void drawArrowUp(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawArrowUp(rect, p);
    }
    static void drawSubMenuIndicator(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawSubMenuIndicator(rect, p);
    }
    static void drawDoubleArrowRightIndicator(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawDoubleArrowRightIndicator(rect, p);
    }
    static void drawToolBarExtensionIndicator(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawToolBarExtensionIndicator(rect, p);
    }
    static void drawCloseIndicator(const QRect& rect, QPainter* p) {
        oclero::qlementine::drawCloseIndicator(rect, p);
    }
    static void drawTreeViewIndicator(const QRect& rect, QPainter* p, bool open) {
        oclero::qlementine::drawTreeViewIndicator(rect, p, open);
    }
    static void drawCalendarIndicator(const QRect& rect, QPainter* p,
        const QColor& color) {
        oclero::qlementine::drawCalendarIndicator(rect, p, color);
    }
    static void drawGripIndicator(const QRect& rect, QPainter* p,
        const QColor& color, Qt::Orientation orientation) {
        oclero::qlementine::drawGripIndicator(rect, p, color, orientation);
    }
    static int getTickInterval(int tickInterval, int singleStep, int pageStep,
        int min, int max, int sliderLength) {
        return oclero::qlementine::getTickInterval(tickInterval, singleStep, pageStep, min, max, sliderLength);
    }
    static void drawSliderTickMarks(QPainter* p, const QRect& tickmarksRect,
        const QColor& tickColor, int min, int max, int interval,
        int tickThickness, int singleStep, int pageStep) {
        oclero::qlementine::drawSliderTickMarks(p, tickmarksRect, tickColor, min, max, interval, tickThickness, singleStep, pageStep);
    }
    static void drawDialTickMarks(QPainter* p, const QRect& tickmarksRect,
        const QColor& tickColor, int min, int max, int tickThickness,
        int tickLength, int singleStep, int pageStep, int minArcLength) {
        oclero::qlementine::drawDialTickMarks(p, tickmarksRect, tickColor, min, max, tickThickness, tickLength, singleStep, pageStep, minArcLength);
    }
    static void drawDial(QPainter* p, const QRect& rect, int min, int max,
        double value, const QColor& bgColor, const QColor& handleColor,
        const QColor& grooveColor, const QColor& valueColor,
        const QColor& markColor, int grooveThickness, int markLength,
        int markThickness) {
        oclero::qlementine::drawDial(p, rect, min, max, value, bgColor, handleColor, grooveColor, valueColor, markColor, grooveThickness, markLength, markThickness);
    }
    static QPainterPath getTabPath(const QRect& rect, const RadiusesF& radiuses) {
        return oclero::qlementine::getTabPath(rect, radiuses);
    }
    static void drawTab(QPainter* p, const QRect& rect,
        const RadiusesF& radiuses, const QColor& bgColor,
        bool drawShadow = false, const QColor& shadowColor = Qt::black) {
        oclero::qlementine::drawTab(p, rect, radiuses, bgColor, drawShadow, shadowColor);
    }
    static void drawTabShadow(QPainter* p, const QRect& rect,
        const RadiusesF& radius, const QColor& color) {
        oclero::qlementine::drawTabShadow(p, rect, radius, color);
    }
    static void drawRadioButton(QPainter* p, const QRect& rect,
        const QColor& bgColor, const QColor& borderColor,
        const QColor& fgColor, qreal borderWidth, qreal progress) {
        oclero::qlementine::drawRadioButton(p, rect, bgColor, borderColor, fgColor, borderWidth, progress);
    }
    static void drawCheckButton(QPainter* p, const QRect& rect, qreal radius,
        const QColor& bgColor, const QColor& borderColor,
        const QColor& fgColor, qreal borderWidth, qreal progress,
        CheckState checkState) {
        oclero::qlementine::drawCheckButton(p, rect, radius, bgColor, borderColor, fgColor, borderWidth, progress, checkState);
    }
    static void drawMenuSeparator(QPainter* p, const QRect& rect,
        const QColor& color, int thickness) {
        oclero::qlementine::drawMenuSeparator(p, rect, color, thickness);
    }
    static void drawElidedMultiLineText(QPainter& p, const QRect& rect,
        const QString& text, const QPaintDevice* paintDevice) {
        oclero::qlementine::drawElidedMultiLineText(p, rect, text, paintDevice);
    }
    static QString removeTrailingWhitespaces(const QString& str) {
        return oclero::qlementine::removeTrailingWhitespaces(str);
    }
    static QString displayedShortcutString(const QKeySequence& shortcut) {
        return oclero::qlementine::displayedShortcutString(shortcut);
    }
    static void drawShortcut(QPainter& p, const QKeySequence& shortcut,
        const QRect& rect, const Theme& theme, bool enabled,
        Qt::Alignment alignment = Qt::AlignLeft | Qt::AlignVCenter) {
        oclero::qlementine::drawShortcut(p, shortcut, rect, theme, enabled, alignment);
    }
    static QSize shortcutSizeHint(const QKeySequence& shortcut, const Theme& theme) {
        return oclero::qlementine::shortcutSizeHint(shortcut, theme);
    }
    static QPixmap getPixmap(const QIcon& icon, const QSize& iconSize,
        MouseState mouse, CheckState checked, const QWidget* widget) {
        return oclero::qlementine::getPixmap(icon, iconSize, mouse, checked, widget);
    }
    static QRect drawIcon(const QRect& rect, QPainter* p, const QIcon& icon,
        MouseState mouse, CheckState checked, const QWidget* widget,
        bool colorize = false, const QColor& color = QColor()) {
        return oclero::qlementine::drawIcon(rect, p, icon, mouse, checked, widget, colorize, color);
    }
    static QPixmap makeClearButtonPixmap(const QSize& size, const QColor& color) {
        return oclero::qlementine::makeClearButtonPixmap(size, color);
    }
    static QPixmap makeCheckPixmap(const QSize& size, const QColor& color) {
        return oclero::qlementine::makeCheckPixmap(size, color);
    }
    static QPixmap makeCalendarPixmap(const QSize& size, const QColor& color) {
        return oclero::qlementine::makeCalendarPixmap(size, color);
    }
    static QPixmap makeDoubleArrowRightPixmap(const QSize& size, const QColor& color) {
        return oclero::qlementine::makeDoubleArrowRightPixmap(size, color);
    }
    static QPixmap makeToolBarExtensionPixmap(const QSize& size, const QColor& color) {
        return oclero::qlementine::makeToolBarExtensionPixmap(size, color);
    }
    static QPixmap makeArrowLeftPixmap(const QSize& size, const QColor& color) {
        return oclero::qlementine::makeArrowLeftPixmap(size, color);
    }
    static QPixmap makeArrowRightPixmap(const QSize& size, const QColor& color) {
        return oclero::qlementine::makeArrowRightPixmap(size, color);
    }
    static QPixmap makeMessageBoxWarningPixmap(const QSize& size,
        const QColor& bgColor, const QColor& fgColor) {
        return oclero::qlementine::makeMessageBoxWarningPixmap(size, bgColor, fgColor);
    }
    static QPixmap makeMessageBoxCriticalPixmap(const QSize& size,
        const QColor& bgColor, const QColor& fgColor) {
        return oclero::qlementine::makeMessageBoxCriticalPixmap(size, bgColor, fgColor);
    }
    static QPixmap makeMessageBoxQuestionPixmap(const QSize& size,
        const QColor& bgColor, const QColor& fgColor) {
        return oclero::qlementine::makeMessageBoxQuestionPixmap(size, bgColor, fgColor);
    }
    static QPixmap makeMessageBoxInformationPixmap(const QSize& size,
        const QColor& bgColor, const QColor& fgColor) {
        return oclero::qlementine::makeMessageBoxInformationPixmap(size, bgColor, fgColor);
    }

    // ---- StateUtils ----
    static MouseState getMouseState(QStyle::State const& state) {
        return oclero::qlementine::getMouseState(state);
    }
    static MouseState getMouseState(bool pressed, bool hovered, bool enabled) {
        return oclero::qlementine::getMouseState(pressed, hovered, enabled);
    }
    static MouseState getToolButtonMouseState(QStyle::State const& state) {
        return oclero::qlementine::getToolButtonMouseState(state);
    }
    static MouseState getMenuItemMouseState(QStyle::State const& state) {
        return oclero::qlementine::getMenuItemMouseState(state);
    }
    static MouseState getComboBoxItemMouseState(QStyle::State const& state) {
        return oclero::qlementine::getComboBoxItemMouseState(state);
    }
    static MouseState getTabItemMouseState(QStyle::State const& state, bool tabIsHovered) {
        return oclero::qlementine::getTabItemMouseState(state, tabIsHovered);
    }
    static ColorRole getColorRole(QStyle::State const& state, bool isDefault) {
        return oclero::qlementine::getColorRole(state, isDefault);
    }
    static ColorRole getColorRole(bool checked, bool isDefault) {
        return oclero::qlementine::getColorRole(checked, isDefault);
    }
    static ColorRole getColorRole(CheckState checked) {
        return oclero::qlementine::getColorRole(checked);
    }
    static MouseState getSliderHandleState(QStyle::State const& state,
        QStyle::SubControls activeSubControls) {
        return oclero::qlementine::getSliderHandleState(state, activeSubControls);
    }
    static MouseState getScrollBarHandleState(QStyle::State const& state,
        QStyle::SubControls activeSubControls) {
        return oclero::qlementine::getScrollBarHandleState(state, activeSubControls);
    }
    static FocusState getFocusState(QStyle::State const& state) {
        return oclero::qlementine::getFocusState(state);
    }
    static FocusState getFocusState(bool focused) {
        return oclero::qlementine::getFocusState(focused);
    }
    static CheckState getCheckState(QStyle::State const& state) {
        return oclero::qlementine::getCheckState(state);
    }
    static CheckState getCheckState(Qt::CheckState const& state) {
        return oclero::qlementine::getCheckState(state);
    }
    static CheckState getCheckState(bool checked) {
        return oclero::qlementine::getCheckState(checked);
    }
    static ActiveState getActiveState(QStyle::State const& state) {
        return oclero::qlementine::getActiveState(state);
    }
    static SelectionState getSelectionState(QStyle::State const& state) {
        return oclero::qlementine::getSelectionState(state);
    }
    static AlternateState getAlternateState(
        QStyleOptionViewItem::ViewItemFeatures const& state) {
        return oclero::qlementine::getAlternateState(state);
    }
    static QStyle::State getState(bool enabled, bool hover, bool pressed) {
        return oclero::qlementine::getState(enabled, hover, pressed);
    }
    static QIcon::Mode getIconMode(MouseState mouse) {
        return oclero::qlementine::getIconMode(mouse);
    }
    static QIcon::State getIconState(CheckState checked) {
        return oclero::qlementine::getIconState(checked);
    }
    static QPalette::ColorGroup getPaletteColorGroup(
        QStyle::State const& state) {
        return oclero::qlementine::getPaletteColorGroup(state);
    }
    static QPalette::ColorGroup getPaletteColorGroup(MouseState mouse) {
        return oclero::qlementine::getPaletteColorGroup(mouse);
    }
    static QString mouseStateToString(MouseState state) {
        return oclero::qlementine::mouseStateToString(state);
    }
    static QString focusStateToString(FocusState state) {
        return oclero::qlementine::focusStateToString(state);
    }
    static QString activeStateToString(ActiveState state) {
        return oclero::qlementine::activeStateToString(state);
    }
    static QString selectionStateToString(SelectionState state) {
        return oclero::qlementine::selectionStateToString(state);
    }
    static QString checkStateToString(CheckState state) {
        return oclero::qlementine::checkStateToString(state);
    }
    static QString printState(QStyle::State const& state) {
        return oclero::qlementine::printState(state);
    }

    // ---- StyleUtils ----
    static bool shouldHaveHoverEvents(const QWidget* w) {
        return oclero::qlementine::shouldHaveHoverEvents(w);
    }
    static bool shouldHaveMouseTracking(const QWidget* w) {
        return oclero::qlementine::shouldHaveMouseTracking(w);
    }
    static bool shouldHaveBoldFont(const QWidget* w) {
        return oclero::qlementine::shouldHaveBoldFont(w);
    }
    static bool shouldHaveExternalFocusFrame(const QWidget* w) {
        return oclero::qlementine::shouldHaveExternalFocusFrame(w);
    }
    static bool shouldHaveTabFocus(const QWidget* w) {
        return oclero::qlementine::shouldHaveTabFocus(w);
    }
    static bool shouldNotBeVerticallyCompressed(const QWidget* w) {
        return oclero::qlementine::shouldNotBeVerticallyCompressed(w);
    }
    static bool shouldNotHaveWheelEvents(const QWidget* w) {
        return oclero::qlementine::shouldNotHaveWheelEvents(w);
    }
    static int getTabIndex(const QStyleOptionTab* optTab, const QWidget* parentWidget) {
        return oclero::qlementine::getTabIndex(optTab, parentWidget);
    }
    static int getTabCount(const QWidget* parentWidget) {
        return oclero::qlementine::getTabCount(parentWidget);
    }

    // ---- WidgetUtils ----
    static QWidget* makeVerticalLine(QWidget* parentWidget, int maxHeight = -1) {
        return oclero::qlementine::makeVerticalLine(parentWidget, maxHeight);
    }
    static QWidget* makeHorizontalLine(QWidget* parentWidget, int maxWidth = -1) {
        return oclero::qlementine::makeHorizontalLine(parentWidget, maxWidth);
    }
    static void centerWidget(QWidget* widget, QWidget* host = nullptr) {
        oclero::qlementine::centerWidget(widget, host);
    }
    static qreal getDpi(const QWidget* widget) {
        return oclero::qlementine::getDpi(widget);
    }
    static QWindow* getWindow(const QWidget* widget) {
        return oclero::qlementine::getWindow(widget);
    }
    static void clearFocus(QWidget* widget, bool recursive) {
        oclero::qlementine::clearFocus(widget, recursive);
    }
};

} // namespace oclero::qlementine
