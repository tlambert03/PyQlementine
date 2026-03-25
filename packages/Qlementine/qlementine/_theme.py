"""Theme and ThemeMeta classes."""

from __future__ import annotations

from qlementine._qt import QtCore, QtGui
from qlementine.utils._color import (
    colorWithAlpha,
    getColorSourceOver,
    toHexRGBA,
    tryGetColorFromVariant,
)
from qlementine.utils._font import pixelSizeToPointSize

QColor = QtGui.QColor
QFont = QtGui.QFont
QFontDatabase = QtGui.QFontDatabase
QPalette = QtGui.QPalette
QGuiApplication = QtGui.QGuiApplication
QJsonDocument = QtCore.QJsonDocument
QSize = QtCore.QSize

__all__ = ["Theme", "ThemeMeta"]


class ThemeMeta:
    """Metadata about a Qlementine Theme."""

    __slots__ = ("name", "version", "author")

    def __init__(self) -> None:
        self.name: str = ""
        self.version: str = ""
        self.author: str = ""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ThemeMeta):
            return NotImplemented
        return (
            self.name == other.name
            and self.version == other.version
            and self.author == other.author
        )

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, ThemeMeta):
            return NotImplemented
        return not self.__eq__(other)


def _rgba(argb32: int) -> QColor:
    """Create QColor from 0xAARRGGBB value (matching QRgba64::fromArgb32)."""
    return QColor.fromRgba(argb32 & 0xFFFFFFFF)


class Theme:
    """Color and sizes configuration for a Qlementine Theme."""

    def __init__(self) -> None:
        self.meta = ThemeMeta()

        # --- Colors (defaults match C++ header exactly) ---
        self.backgroundColorMain1 = QColor(0xFFFFFF)
        self.backgroundColorMain2 = QColor(0xF3F3F3)
        self.backgroundColorMain3 = QColor(0xE3E3E3)
        self.backgroundColorMain4 = QColor(0xDCDCDC)
        self.backgroundColorMainTransparent = _rgba(0x00FAFAFA)

        self.backgroundColorWorkspace = QColor(0xB7B7B7)
        self.backgroundColorTabBar = QColor(0xB7B7B7)

        self.neutralColor = QColor(0xE1E1E1)
        self.neutralColorHovered = QColor(0xDADADA)
        self.neutralColorPressed = QColor(0xD2D2D2)
        self.neutralColorDisabled = QColor(0xEEEEEE)
        self.neutralColorTransparent = _rgba(0x00E1E1E1)

        self.focusColor = _rgba(0x6640A9FF)

        self.primaryColor = QColor(0x1890FF)
        self.primaryColorHovered = QColor(0x2C9DFF)
        self.primaryColorPressed = QColor(0x40A9FF)
        self.primaryColorDisabled = QColor(0xD1E9FF)
        self.primaryColorTransparent = _rgba(0x001890FF)

        self.primaryColorForeground = QColor(0xFFFFFF)
        self.primaryColorForegroundHovered = QColor(0xFFFFFF)
        self.primaryColorForegroundPressed = QColor(0xFFFFFF)
        self.primaryColorForegroundDisabled = QColor(0xECF6FF)
        self.primaryColorForegroundTransparent = _rgba(0x00FFFFFF)

        self.primaryAlternativeColor = QColor(0x106EF9)
        self.primaryAlternativeColorHovered = QColor(0x107BFD)
        self.primaryAlternativeColorPressed = QColor(0x108BFD)
        self.primaryAlternativeColorDisabled = QColor(0xA9D6FF)
        self.primaryAlternativeColorTransparent = _rgba(0x001875FF)

        self.secondaryColor = QColor(0x404040)
        self.secondaryColorHovered = QColor(0x333333)
        self.secondaryColorPressed = QColor(0x262626)
        self.secondaryColorDisabled = QColor(0xD4D4D4)
        self.secondaryColorTransparent = _rgba(0x00404040)

        self.secondaryColorForeground = QColor(0xFFFFFF)
        self.secondaryColorForegroundHovered = QColor(0xFFFFFF)
        self.secondaryColorForegroundPressed = QColor(0xFFFFFF)
        self.secondaryColorForegroundDisabled = QColor(0xEDEDED)
        self.secondaryColorForegroundTransparent = _rgba(0x00FFFFFF)

        self.secondaryAlternativeColor = QColor(0x909090)
        self.secondaryAlternativeColorHovered = QColor(0x747474)
        self.secondaryAlternativeColorPressed = QColor(0x828282)
        self.secondaryAlternativeColorDisabled = QColor(0xC3C3C3)
        self.secondaryAlternativeColorTransparent = _rgba(0x00909090)

        self.statusColorSuccess = QColor(0x2BB5A0)
        self.statusColorSuccessHovered = QColor(0x3CBFAB)
        self.statusColorSuccessPressed = QColor(0x4ECDB9)
        self.statusColorSuccessDisabled = QColor(0xD5F0EC)
        self.statusColorInfo = QColor(0x1BA8D5)
        self.statusColorInfoHovered = QColor(0x1EB5E5)
        self.statusColorInfoPressed = QColor(0x29C0F0)
        self.statusColorInfoDisabled = QColor(0xC7EAF5)
        self.statusColorWarning = QColor(0xFBC064)
        self.statusColorWarningHovered = QColor(0xFFCF6C)
        self.statusColorWarningPressed = QColor(0xFFD880)
        self.statusColorWarningDisabled = QColor(0xFEEFD8)
        self.statusColorError = QColor(0xE96B72)
        self.statusColorErrorHovered = QColor(0xF47C83)
        self.statusColorErrorPressed = QColor(0xFF9197)
        self.statusColorErrorDisabled = QColor(0xF9DADC)
        self.statusColorForeground = QColor(0xFFFFFF)
        self.statusColorForegroundHovered = QColor(0xFFFFFF)
        self.statusColorForegroundPressed = QColor(0xFFFFFF)
        self.statusColorForegroundDisabled = _rgba(0x99FFFFFF)

        self.shadowColor1 = _rgba(0x20000000)
        self.shadowColor2 = _rgba(0x40000000)
        self.shadowColor3 = _rgba(0x60000000)
        self.shadowColorTransparent = _rgba(0x00000000)

        self.borderColor = QColor(0xD3D3D3)
        self.borderColorHovered = QColor(0xB3B3B3)
        self.borderColorPressed = QColor(0xA3A3A3)
        self.borderColorDisabled = QColor(0xE9E9E9)
        self.borderColorTransparent = _rgba(0x00D3D3D3)

        self.semiTransparentColor1 = _rgba(0x0000000)
        self.semiTransparentColor2 = _rgba(0x19000000)
        self.semiTransparentColor3 = _rgba(0x21000000)
        self.semiTransparentColor4 = _rgba(0x28000000)
        self.semiTransparentColorTransparent = _rgba(0x00000000)

        # --- Scalar fields ---
        self.useSystemFonts: bool = True

        self.fontSize: int = 12
        self.fontSizeMonospace: int = 13
        self.fontSizeH1: int = 34
        self.fontSizeH2: int = 26
        self.fontSizeH3: int = 22
        self.fontSizeH4: int = 18
        self.fontSizeH5: int = 14
        self.fontSizeS1: int = 10
        self.animationDuration: int = 192
        self.focusAnimationDuration: int = 384
        self.sliderAnimationDuration: int = 96
        self.borderRadius: float = 6.0
        self.checkBoxBorderRadius: float = 4.0
        self.menuItemBorderRadius: float = 4.0
        self.menuBarItemBorderRadius: float = 2.0
        self.borderWidth: int = 1
        self.controlHeightLarge: int = 28
        self.controlHeightMedium: int = 24
        self.controlHeightSmall: int = 16
        self.controlDefaultWidth: int = 96
        self.dialMarkLength: int = 8
        self.dialMarkThickness: int = 2
        self.dialTickLength: int = 4
        self.dialTickSpacing: int = 4
        self.dialGrooveThickness: int = 4
        self.focusBorderWidth: int = 2
        self.iconSize = QSize(16, 16)
        self.iconSizeMedium = QSize(24, 24)
        self.iconSizeLarge = QSize(24, 24)
        self.iconSizeExtraSmall = QSize(12, 12)
        self.sliderTickSize: int = 3
        self.sliderTickSpacing: int = 2
        self.sliderTickThickness: int = 1
        self.sliderGrooveHeight: int = 4
        self.progressBarGrooveHeight: int = 6
        self.spacing: int = 8
        self.scrollBarThicknessFull: int = 12
        self.scrollBarThicknessSmall: int = 6
        self.scrollBarMargin: int = 0
        self.tabBarPaddingTop: int = 4
        self.tabBarTabMaxWidth: int = 0
        self.tabBarTabMinWidth: int = 0

        # --- Fonts & palette ---
        self.fontRegular = QFont()
        self.fontBold = QFont()
        self.fontH1 = QFont()
        self.fontH2 = QFont()
        self.fontH3 = QFont()
        self.fontH4 = QFont()
        self.fontH5 = QFont()
        self.fontCaption = QFont()
        self.fontMonospace = QFont()

        self.palette = QPalette()

        self._initialize_fonts()
        self._initialize_palette()

    # ------------------------------------------------------------------
    # Fonts
    # ------------------------------------------------------------------

    def _initialize_fonts(self) -> None:
        if self.useSystemFonts:
            default_font = QFontDatabase.systemFont(
                QFontDatabase.SystemFont.GeneralFont
            )
            fixed_font = QFontDatabase.systemFont(
                QFontDatabase.SystemFont.FixedFont
            )
            title_font = QFontDatabase.systemFont(
                QFontDatabase.SystemFont.TitleFont
            )
        else:
            default_font = QFont("Inter")
            fixed_font = QFont("Roboto Mono")
            title_font = QFont("Inter Display")

        screen = QGuiApplication.primaryScreen()
        dpi = screen.logicalDotsPerInch() if screen else 96.0

        self.fontRegular = QFont(default_font)
        if self.useSystemFonts:
            self.fontSize = default_font.pointSize()
        else:
            self.fontRegular.setWeight(QFont.Weight.Normal)
            self.fontRegular.setPointSizeF(
                pixelSizeToPointSize(self.fontSize, dpi)
            )

        self.fontBold = QFont(default_font)
        self.fontBold.setWeight(QFont.Weight.Bold)
        if not self.useSystemFonts:
            self.fontBold.setPointSizeF(
                pixelSizeToPointSize(self.fontSize, dpi)
            )

        self.fontH1 = QFont(title_font)
        self.fontH1.setWeight(QFont.Weight.Bold)
        self.fontH1.setPointSizeF(
            pixelSizeToPointSize(self.fontSizeH1, dpi)
        )

        self.fontH2 = QFont(title_font)
        self.fontH2.setWeight(QFont.Weight.Bold)
        self.fontH2.setPointSizeF(
            pixelSizeToPointSize(self.fontSizeH2, dpi)
        )

        self.fontH3 = QFont(title_font)
        self.fontH3.setWeight(QFont.Weight.Bold)
        self.fontH3.setPointSizeF(
            pixelSizeToPointSize(self.fontSizeH3, dpi)
        )

        self.fontH4 = QFont(title_font)
        self.fontH4.setWeight(QFont.Weight.Bold)
        self.fontH4.setPointSizeF(
            pixelSizeToPointSize(self.fontSizeH4, dpi)
        )

        self.fontH5 = QFont(title_font)
        self.fontH5.setWeight(QFont.Weight.Bold)
        self.fontH5.setPointSizeF(
            pixelSizeToPointSize(self.fontSizeH5, dpi)
        )

        self.fontCaption = QFont(default_font)
        if self.useSystemFonts:
            self.fontSizeS1 = default_font.pointSize()
        else:
            self.fontCaption.setWeight(QFont.Weight.Normal)
            self.fontCaption.setPointSizeF(
                pixelSizeToPointSize(self.fontSizeS1, dpi)
            )

        self.fontMonospace = QFont(fixed_font)
        if self.useSystemFonts:
            self.fontSizeMonospace = fixed_font.pointSize()
        else:
            self.fontMonospace.setWeight(QFont.Weight.Normal)
            self.fontMonospace.setPointSizeF(
                pixelSizeToPointSize(self.fontSizeMonospace, dpi)
            )

    # ------------------------------------------------------------------
    # Palette
    # ------------------------------------------------------------------

    def _initialize_palette(self) -> None:
        p = QPalette()
        All = QPalette.ColorGroup.All
        Disabled = QPalette.ColorGroup.Disabled
        Normal = QPalette.ColorGroup.Normal
        Current = QPalette.ColorGroup.Current
        Active = QPalette.ColorGroup.Active

        # Shades
        p.setColor(All, QPalette.ColorRole.Window, self.backgroundColorMain2)
        p.setColor(All, QPalette.ColorRole.Dark, self.backgroundColorMain3)
        p.setColor(All, QPalette.ColorRole.Mid, self.backgroundColorMain3)
        p.setColor(
            All, QPalette.ColorRole.Midlight, self.backgroundColorMain2
        )
        p.setColor(All, QPalette.ColorRole.Light, self.backgroundColorMain2)

        # ItemViews
        item_view_base = self.backgroundColorMain1
        item_view_alternate = getColorSourceOver(
            item_view_base,
            colorWithAlpha(
                self.neutralColorDisabled,
                self.neutralColorDisabled.alpha() // 2,
            ),
        )
        item_view_disabled = getColorSourceOver(
            self.backgroundColorMain1, self.neutralColorDisabled
        )
        p.setColor(All, QPalette.ColorRole.Base, item_view_base)
        p.setColor(Disabled, QPalette.ColorRole.Base, item_view_disabled)
        p.setColor(
            All, QPalette.ColorRole.AlternateBase, item_view_alternate
        )
        p.setColor(
            Disabled, QPalette.ColorRole.AlternateBase, item_view_disabled
        )
        p.setColor(
            All,
            QPalette.ColorRole.NoRole,
            self.backgroundColorMainTransparent,
        )
        p.setColor(
            Disabled,
            QPalette.ColorRole.NoRole,
            self.backgroundColorMainTransparent,
        )

        # Tooltips
        p.setColor(
            All, QPalette.ColorRole.ToolTipBase, self.secondaryColor
        )
        p.setColor(
            All,
            QPalette.ColorRole.ToolTipText,
            self.secondaryColorForeground,
        )

        # Highlight
        p.setColor(All, QPalette.ColorRole.Highlight, self.primaryColor)
        p.setColor(
            Disabled, QPalette.ColorRole.Highlight, self.primaryColorDisabled
        )
        p.setColor(
            All,
            QPalette.ColorRole.HighlightedText,
            self.primaryColorForeground,
        )
        p.setColor(
            Disabled,
            QPalette.ColorRole.HighlightedText,
            self.primaryColorDisabled,
        )

        # Text
        p.setColor(All, QPalette.ColorRole.Text, self.secondaryColor)
        p.setColor(
            Disabled, QPalette.ColorRole.Text, self.secondaryColorDisabled
        )
        p.setColor(
            All, QPalette.ColorRole.WindowText, self.secondaryColor
        )
        p.setColor(
            Disabled,
            QPalette.ColorRole.WindowText,
            self.secondaryColorDisabled,
        )
        p.setColor(
            All,
            QPalette.ColorRole.PlaceholderText,
            self.secondaryColorDisabled,
        )
        p.setColor(
            Disabled,
            QPalette.ColorRole.PlaceholderText,
            self.secondaryColorDisabled,
        )
        p.setColor(All, QPalette.ColorRole.Link, self.primaryColor)
        p.setColor(
            Disabled, QPalette.ColorRole.Link, self.secondaryColorDisabled
        )
        p.setColor(All, QPalette.ColorRole.LinkVisited, self.primaryColor)
        p.setColor(
            Disabled,
            QPalette.ColorRole.LinkVisited,
            self.secondaryColorDisabled,
        )
        p.setColor(
            All,
            QPalette.ColorRole.BrightText,
            self.secondaryAlternativeColor,
        )
        p.setColor(
            Disabled,
            QPalette.ColorRole.BrightText,
            self.secondaryAlternativeColorDisabled,
        )

        # Buttons
        p.setColor(
            All,
            QPalette.ColorRole.ButtonText,
            self.secondaryColorForeground,
        )
        p.setColor(
            Disabled,
            QPalette.ColorRole.ButtonText,
            self.secondaryColorForegroundDisabled,
        )
        p.setColor(All, QPalette.ColorRole.Button, self.neutralColor)
        p.setColor(Normal, QPalette.ColorRole.Button, self.neutralColor)
        p.setColor(
            Current, QPalette.ColorRole.Button, self.neutralColorHovered
        )
        p.setColor(
            Active, QPalette.ColorRole.Button, self.neutralColorPressed
        )
        p.setColor(
            Disabled, QPalette.ColorRole.Button, self.neutralColorDisabled
        )

        self.palette = p

    # ------------------------------------------------------------------
    # JSON serialization
    # ------------------------------------------------------------------

    def toJson(self) -> QJsonDocument:
        """Serialize the theme to a QJsonDocument."""
        import json as _json

        obj: dict = {}

        # Metadata
        obj["meta"] = {
            "name": self.meta.name,
            "version": self.meta.version,
            "author": self.meta.author,
        }

        # Colors
        for name in _COLOR_FIELDS:
            obj[name] = toHexRGBA(getattr(self, name))

        # Bools
        obj["useSystemFonts"] = self.useSystemFonts

        # Ints
        for name in _INT_FIELDS:
            obj[name] = getattr(self, name)

        # Doubles
        for name in _DOUBLE_FIELDS:
            obj[name] = getattr(self, name)

        # Icon sizes serialized as single int (width)
        obj["iconSize"] = self.iconSize.width()
        obj["iconSizeMedium"] = self.iconSizeMedium.width()
        obj["iconSizeLarge"] = self.iconSizeLarge.width()
        obj["iconSizeExtraSmall"] = self.iconSizeExtraSmall.width()

        data = _json.dumps(obj).encode("utf-8")
        return QJsonDocument.fromJson(data)

    # ------------------------------------------------------------------
    # JSON deserialization
    # ------------------------------------------------------------------

    @staticmethod
    def fromJsonPath(path: str) -> Theme:
        """Load a theme from a JSON file. Raises ValueError on failure."""
        import json as _json

        try:
            with open(path, "rb") as f:
                raw = f.read()
        except OSError as e:
            raise ValueError(f"Failed to load theme from '{path}': {e}")

        doc = QJsonDocument.fromJson(raw)
        if doc.isNull():
            raise ValueError(f"Failed to load theme from '{path}'")
        return Theme.fromJsonDoc(doc)

    @staticmethod
    def fromJsonDoc(doc: QJsonDocument) -> Theme:
        """Load a theme from a QJsonDocument. Raises ValueError on failure."""
        import json as _json

        if doc.isNull() or not doc.isObject():
            raise ValueError("Failed to load theme: invalid JSON document")

        raw = bytes(doc.toJson())
        obj = _json.loads(raw)

        if not isinstance(obj, dict) or not obj:
            raise ValueError("Failed to load theme: empty JSON object")

        # Meta is required
        meta_obj = obj.get("meta")
        if not isinstance(meta_obj, dict):
            raise ValueError("Failed to load theme: missing meta")
        for key in ("name", "version", "author"):
            if key not in meta_obj:
                raise ValueError(
                    f"Failed to load theme: missing meta.{key}"
                )

        theme = Theme.__new__(Theme)
        # Initialize with defaults first
        Theme.__init__(theme)

        theme.meta.name = str(meta_obj.get("name", ""))
        theme.meta.version = str(meta_obj.get("version", ""))
        theme.meta.author = str(meta_obj.get("author", ""))

        # Helper: recursive color resolution (one level of indirection)
        def _try_get_color(key: str) -> QColor | None:
            if key not in obj:
                return None
            val = obj[key]
            color = tryGetColorFromVariant(val)
            if color is not None:
                return color
            # Check if value is a reference to another key
            if isinstance(val, str) and val != key and val in obj:
                ref_val = obj[val]
                return tryGetColorFromVariant(ref_val)
            return None

        def _try_get_bool(key: str) -> bool | None:
            if key not in obj:
                return None
            val = obj[key]
            if isinstance(val, str) and val != key and val in obj:
                val = obj[val]
            if isinstance(val, bool):
                return val
            return None

        def _try_get_int(key: str) -> int | None:
            if key not in obj:
                return None
            val = obj[key]
            if isinstance(val, str) and val != key and val in obj:
                val = obj[val]
            if isinstance(val, (int, float)):
                return int(val)
            return None

        def _try_get_double(key: str) -> float | None:
            if key not in obj:
                return None
            val = obj[key]
            if isinstance(val, str) and val != key and val in obj:
                val = obj[val]
            if isinstance(val, (int, float)):
                return float(val)
            return None

        # Parse colors
        for name in _COLOR_FIELDS_FROM_JSON:
            c = _try_get_color(name)
            if c is not None:
                setattr(theme, name, c)

        # Compute transparent variants
        theme.backgroundColorMainTransparent = colorWithAlpha(
            theme.backgroundColorMain1, 0
        )
        theme.neutralColorTransparent = colorWithAlpha(
            theme.neutralColorDisabled, 0
        )
        theme.primaryColorTransparent = colorWithAlpha(
            theme.primaryColor, 0
        )
        theme.primaryColorForegroundTransparent = colorWithAlpha(
            theme.primaryColorForeground, 0
        )
        theme.primaryAlternativeColorTransparent = colorWithAlpha(
            theme.primaryAlternativeColor, 0
        )
        theme.secondaryColorTransparent = colorWithAlpha(
            theme.secondaryColor, 0
        )
        theme.secondaryAlternativeColorTransparent = colorWithAlpha(
            theme.secondaryAlternativeColor, 0
        )
        theme.secondaryColorForegroundTransparent = colorWithAlpha(
            theme.secondaryColorForeground, 0
        )
        theme.semiTransparentColorTransparent = colorWithAlpha(
            theme.semiTransparentColor1, 0
        )
        theme.borderColorTransparent = colorWithAlpha(
            theme.borderColor, 0
        )
        theme.shadowColorTransparent = colorWithAlpha(
            theme.shadowColor1, 0
        )

        # Parse bools
        v = _try_get_bool("useSystemFonts")
        if v is not None:
            theme.useSystemFonts = v

        # Parse ints
        for name in _INT_FIELDS:
            v = _try_get_int(name)
            if v is not None:
                setattr(theme, name, v)

        # Parse doubles
        for name in _DOUBLE_FIELDS:
            v = _try_get_double(name)
            if v is not None:
                setattr(theme, name, v)

        # Icon sizes
        icon_extent = _try_get_int("iconExtent")
        if icon_extent is not None:
            theme.iconSize = QSize(icon_extent, icon_extent)
            w = int(icon_extent * 1.5)
            theme.iconSizeMedium = QSize(w, w)
            theme.iconSizeLarge = QSize(icon_extent * 2, icon_extent * 2)
            w2 = int(icon_extent * 0.75)
            theme.iconSizeExtraSmall = QSize(w2, w2)

        # Clamp tab bar widths
        theme.tabBarTabMaxWidth = max(0, theme.tabBarTabMaxWidth)
        theme.tabBarTabMinWidth = max(0, theme.tabBarTabMinWidth)
        if theme.tabBarTabMinWidth > theme.tabBarTabMaxWidth:
            theme.tabBarTabMinWidth, theme.tabBarTabMaxWidth = (
                theme.tabBarTabMaxWidth,
                theme.tabBarTabMinWidth,
            )

        theme._initialize_fonts()
        theme._initialize_palette()
        return theme

    # ------------------------------------------------------------------
    # Equality
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Theme):
            return NotImplemented
        return (
            self.meta == other.meta
            and self.backgroundColorMain1 == other.backgroundColorMain1
            and self.backgroundColorMain2 == other.backgroundColorMain2
            and self.backgroundColorMain3 == other.backgroundColorMain3
            and self.backgroundColorMain4 == other.backgroundColorMain4
            and self.backgroundColorWorkspace
            == other.backgroundColorWorkspace
            and self.neutralColorDisabled == other.neutralColorDisabled
            and self.neutralColor == other.neutralColor
            and self.neutralColorHovered == other.neutralColorHovered
            and self.neutralColorPressed == other.neutralColorPressed
            and self.focusColor == other.focusColor
            and self.primaryColor == other.primaryColor
            and self.primaryColorHovered == other.primaryColorHovered
            and self.primaryColorPressed == other.primaryColorPressed
            and self.primaryColorDisabled == other.primaryColorDisabled
            and self.primaryColorForeground == other.primaryColorForeground
            and self.primaryColorForegroundHovered
            == other.primaryColorForegroundHovered
            and self.primaryColorForegroundPressed
            == other.primaryColorForegroundPressed
            and self.primaryColorForegroundDisabled
            == other.primaryColorForegroundDisabled
            and self.primaryAlternativeColor
            == other.primaryAlternativeColor
            and self.primaryAlternativeColorHovered
            == other.primaryAlternativeColorHovered
            and self.primaryAlternativeColorPressed
            == other.primaryAlternativeColorPressed
            and self.primaryAlternativeColorDisabled
            == other.primaryAlternativeColorDisabled
            and self.secondaryColor == other.secondaryColor
            and self.secondaryColorHovered == other.secondaryColorHovered
            and self.secondaryColorPressed == other.secondaryColorPressed
            and self.secondaryColorDisabled == other.secondaryColorDisabled
            and self.secondaryAlternativeColor
            == other.secondaryAlternativeColor
            and self.secondaryAlternativeColorHovered
            == other.secondaryAlternativeColorHovered
            and self.secondaryAlternativeColorPressed
            == other.secondaryAlternativeColorPressed
            and self.secondaryAlternativeColorDisabled
            == other.secondaryAlternativeColorDisabled
            and self.secondaryColorForeground
            == other.secondaryColorForeground
            and self.secondaryColorForegroundHovered
            == other.secondaryColorForegroundHovered
            and self.secondaryColorForegroundPressed
            == other.secondaryColorForegroundPressed
            and self.secondaryColorForegroundDisabled
            == other.secondaryColorForegroundDisabled
            and self.statusColorSuccess == other.statusColorSuccess
            and self.statusColorSuccessHovered
            == other.statusColorSuccessHovered
            and self.statusColorSuccessPressed
            == other.statusColorSuccessPressed
            and self.statusColorSuccessDisabled
            == other.statusColorSuccessDisabled
            and self.statusColorInfo == other.statusColorInfo
            and self.statusColorInfoHovered == other.statusColorInfoHovered
            and self.statusColorInfoPressed == other.statusColorInfoPressed
            and self.statusColorInfoDisabled
            == other.statusColorInfoDisabled
            and self.statusColorWarning == other.statusColorWarning
            and self.statusColorWarningHovered
            == other.statusColorWarningHovered
            and self.statusColorWarningPressed
            == other.statusColorWarningPressed
            and self.statusColorWarningDisabled
            == other.statusColorWarningDisabled
            and self.statusColorError == other.statusColorError
            and self.statusColorErrorHovered
            == other.statusColorErrorHovered
            and self.statusColorErrorPressed
            == other.statusColorErrorPressed
            and self.statusColorErrorDisabled
            == other.statusColorErrorDisabled
            and self.statusColorForeground == other.statusColorForeground
            and self.statusColorForegroundHovered
            == other.statusColorForegroundHovered
            and self.statusColorForegroundPressed
            == other.statusColorForegroundPressed
            and self.statusColorForegroundDisabled
            == other.statusColorForegroundDisabled
            and self.shadowColor1 == other.shadowColor1
            and self.shadowColor2 == other.shadowColor2
            and self.shadowColor3 == other.shadowColor3
            and self.borderColor == other.borderColor
            and self.borderColorHovered == other.borderColorHovered
            and self.borderColorPressed == other.borderColorPressed
            and self.borderColorDisabled == other.borderColorDisabled
            and self.useSystemFonts == other.useSystemFonts
            and self.animationDuration == other.animationDuration
            and self.focusAnimationDuration == other.focusAnimationDuration
            and self.sliderAnimationDuration
            == other.sliderAnimationDuration
            and self.borderRadius == other.borderRadius
            and self.checkBoxBorderRadius == other.checkBoxBorderRadius
            and self.menuItemBorderRadius == other.menuItemBorderRadius
            and self.menuBarItemBorderRadius
            == other.menuBarItemBorderRadius
            and self.borderWidth == other.borderWidth
            and self.controlHeightLarge == other.controlHeightLarge
            and self.controlHeightMedium == other.controlHeightMedium
            and self.controlHeightSmall == other.controlHeightSmall
            and self.controlDefaultWidth == other.controlDefaultWidth
            and self.dialMarkLength == other.dialMarkLength
            and self.dialMarkThickness == other.dialMarkThickness
            and self.dialTickLength == other.dialTickLength
            and self.dialTickSpacing == other.dialTickSpacing
            and self.dialGrooveThickness == other.dialGrooveThickness
            and self.focusBorderWidth == other.focusBorderWidth
            and self.iconSize == other.iconSize
            and self.iconSizeMedium == other.iconSizeMedium
            and self.iconSizeLarge == other.iconSizeLarge
            and self.iconSizeExtraSmall == other.iconSizeExtraSmall
            and self.sliderTickSize == other.sliderTickSize
            and self.sliderTickThickness == other.sliderTickThickness
            and self.sliderGrooveHeight == other.sliderGrooveHeight
            and self.progressBarGrooveHeight
            == other.progressBarGrooveHeight
            and self.spacing == other.spacing
            and self.scrollBarThicknessFull == other.scrollBarThicknessFull
            and self.scrollBarThicknessSmall
            == other.scrollBarThicknessSmall
            and self.scrollBarMargin == other.scrollBarMargin
            and self.tabBarPaddingTop == other.tabBarPaddingTop
        )

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Theme):
            return NotImplemented
        return not self.__eq__(other)


# ------------------------------------------------------------------
# Field name lists for serialization
# ------------------------------------------------------------------

_COLOR_FIELDS_FROM_JSON = [
    "backgroundColorMain1",
    "backgroundColorMain2",
    "backgroundColorMain3",
    "backgroundColorMain4",
    "backgroundColorWorkspace",
    "backgroundColorTabBar",
    "neutralColorDisabled",
    "neutralColor",
    "neutralColorHovered",
    "neutralColorPressed",
    "focusColor",
    "primaryColor",
    "primaryColorHovered",
    "primaryColorPressed",
    "primaryColorDisabled",
    "primaryColorForeground",
    "primaryColorForegroundHovered",
    "primaryColorForegroundPressed",
    "primaryColorForegroundDisabled",
    "primaryAlternativeColor",
    "primaryAlternativeColorHovered",
    "primaryAlternativeColorPressed",
    "primaryAlternativeColorDisabled",
    "secondaryColor",
    "secondaryColorHovered",
    "secondaryColorPressed",
    "secondaryColorDisabled",
    "secondaryAlternativeColor",
    "secondaryAlternativeColorHovered",
    "secondaryAlternativeColorPressed",
    "secondaryAlternativeColorDisabled",
    "secondaryColorForeground",
    "secondaryColorForegroundHovered",
    "secondaryColorForegroundPressed",
    "secondaryColorForegroundDisabled",
    "semiTransparentColor1",
    "semiTransparentColor2",
    "semiTransparentColor3",
    "semiTransparentColor4",
    "statusColorSuccess",
    "statusColorSuccessHovered",
    "statusColorSuccessPressed",
    "statusColorSuccessDisabled",
    "statusColorInfo",
    "statusColorInfoHovered",
    "statusColorInfoPressed",
    "statusColorInfoDisabled",
    "statusColorWarning",
    "statusColorWarningHovered",
    "statusColorWarningPressed",
    "statusColorWarningDisabled",
    "statusColorError",
    "statusColorErrorHovered",
    "statusColorErrorPressed",
    "statusColorErrorDisabled",
    "statusColorForeground",
    "statusColorForegroundHovered",
    "statusColorForegroundPressed",
    "statusColorForegroundDisabled",
    "shadowColor1",
    "shadowColor2",
    "shadowColor3",
    "borderColor",
    "borderColorHovered",
    "borderColorPressed",
    "borderColorDisabled",
]

# toJson serializes these color fields (including transparent variants)
_COLOR_FIELDS = _COLOR_FIELDS_FROM_JSON + [
    "backgroundColorMainTransparent",
    "neutralColorTransparent",
    "primaryColorTransparent",
    "primaryColorForegroundTransparent",
    "primaryAlternativeColorTransparent",
    "secondaryColorTransparent",
    "secondaryAlternativeColorTransparent",
    "secondaryColorForegroundTransparent",
    "semiTransparentColorTransparent",
    "shadowColorTransparent",
    "borderColorTransparent",
]

_INT_FIELDS = [
    "fontSize",
    "fontSizeMonospace",
    "fontSizeH1",
    "fontSizeH2",
    "fontSizeH3",
    "fontSizeH4",
    "fontSizeH5",
    "fontSizeS1",
    "animationDuration",
    "focusAnimationDuration",
    "sliderAnimationDuration",
    "borderWidth",
    "controlHeightLarge",
    "controlHeightMedium",
    "controlHeightSmall",
    "controlDefaultWidth",
    "dialMarkLength",
    "dialMarkThickness",
    "dialTickLength",
    "dialTickSpacing",
    "dialGrooveThickness",
    "focusBorderWidth",
    "sliderTickSize",
    "sliderTickSpacing",
    "sliderTickThickness",
    "sliderGrooveHeight",
    "progressBarGrooveHeight",
    "spacing",
    "scrollBarThicknessFull",
    "scrollBarThicknessSmall",
    "scrollBarMargin",
    "tabBarPaddingTop",
    "tabBarTabMaxWidth",
    "tabBarTabMinWidth",
]

_DOUBLE_FIELDS = [
    "borderRadius",
    "checkBoxBorderRadius",
    "menuItemBorderRadius",
    "menuBarItemBorderRadius",
]
