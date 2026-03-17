"""Pure-Python dataclasses mirroring oclero::qlementine::Theme."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    QSizeLike: TypeAlias = tuple[int, int]
    QColorLike: TypeAlias = int | str | tuple[int, int, int] | tuple[int, int, int, int]


@dataclass
class ThemeMeta:
    """Metadata about a Qlementine Theme."""

    name: str = ""
    version: str = ""
    author: str = ""


@dataclass
class Theme:
    """Color and sizes configuration for a Qlementine Theme."""

    meta: ThemeMeta = field(default_factory=ThemeMeta)

    background_color_main1: Any = 0xFFFFFF  # TODO: QColor
    background_color_main2: Any = 0xF3F3F3  # TODO: QColor
    background_color_main3: Any = 0xE3E3E3  # TODO: QColor
    background_color_main4: Any = 0xDCDCDC  # TODO: QColor
    background_color_main_transparent: Any = 0x00FAFAFA  # TODO: QColor (argb32)

    background_color_workspace: Any = 0xB7B7B7  # TODO: QColor
    background_color_tab_bar: Any = 0xB7B7B7  # TODO: QColor

    neutral_color: Any = 0xE1E1E1  # TODO: QColor
    neutral_color_hovered: Any = 0xDADADA  # TODO: QColor
    neutral_color_pressed: Any = 0xD2D2D2  # TODO: QColor
    neutral_color_disabled: Any = 0xEEEEEE  # TODO: QColor
    neutral_color_transparent: Any = 0x00E1E1E1  # TODO: QColor (argb32)

    focus_color: Any = 0x6640A9FF  # TODO: QColor (argb32)

    primary_color: Any = 0x1890FF  # TODO: QColor
    primary_color_hovered: Any = 0x2C9DFF  # TODO: QColor
    primary_color_pressed: Any = 0x40A9FF  # TODO: QColor
    primary_color_disabled: Any = 0xD1E9FF  # TODO: QColor
    primary_color_transparent: Any = 0x001890FF  # TODO: QColor (argb32)

    primary_color_foreground: Any = 0xFFFFFF  # TODO: QColor
    primary_color_foreground_hovered: Any = 0xFFFFFF  # TODO: QColor
    primary_color_foreground_pressed: Any = 0xFFFFFF  # TODO: QColor
    primary_color_foreground_disabled: Any = 0xECF6FF  # TODO: QColor
    primary_color_foreground_transparent: Any = 0x00FFFFFF  # TODO: QColor (argb32)

    primary_alternative_color: Any = 0x106EF9  # TODO: QColor
    primary_alternative_color_hovered: Any = 0x107BFD  # TODO: QColor
    primary_alternative_color_pressed: Any = 0x108BFD  # TODO: QColor
    primary_alternative_color_disabled: Any = 0xA9D6FF  # TODO: QColor
    primary_alternative_color_transparent: Any = 0x001875FF  # TODO: QColor (argb32)

    secondary_color: Any = 0x404040  # TODO: QColor
    secondary_color_hovered: Any = 0x333333  # TODO: QColor
    secondary_color_pressed: Any = 0x262626  # TODO: QColor
    secondary_color_disabled: Any = 0xD4D4D4  # TODO: QColor
    secondary_color_transparent: Any = 0x00404040  # TODO: QColor (argb32)

    secondary_color_foreground: Any = 0xFFFFFF  # TODO: QColor
    secondary_color_foreground_hovered: Any = 0xFFFFFF  # TODO: QColor
    secondary_color_foreground_pressed: Any = 0xFFFFFF  # TODO: QColor
    secondary_color_foreground_disabled: Any = 0xEDEDED  # TODO: QColor
    secondary_color_foreground_transparent: Any = 0x00FFFFFF  # TODO: QColor (argb32)

    secondary_alternative_color: Any = 0x909090  # TODO: QColor
    secondary_alternative_color_hovered: Any = 0x747474  # TODO: QColor
    secondary_alternative_color_pressed: Any = 0x828282  # TODO: QColor
    secondary_alternative_color_disabled: Any = 0xC3C3C3  # TODO: QColor
    secondary_alternative_color_transparent: Any = 0x00909090  # TODO: QColor (argb32)

    status_color_success: Any = 0x2BB5A0  # TODO: QColor
    status_color_success_hovered: Any = 0x3CBFAB  # TODO: QColor
    status_color_success_pressed: Any = 0x4ECDB9  # TODO: QColor
    status_color_success_disabled: Any = 0xD5F0EC  # TODO: QColor

    status_color_info: Any = 0x1BA8D5  # TODO: QColor
    status_color_info_hovered: Any = 0x1EB5E5  # TODO: QColor
    status_color_info_pressed: Any = 0x29C0F0  # TODO: QColor
    status_color_info_disabled: Any = 0xC7EAF5  # TODO: QColor

    status_color_warning: Any = 0xFBC064  # TODO: QColor
    status_color_warning_hovered: Any = 0xFFCF6C  # TODO: QColor
    status_color_warning_pressed: Any = 0xFFD880  # TODO: QColor
    status_color_warning_disabled: Any = 0xFEEFD8  # TODO: QColor

    status_color_error: Any = 0xE96B72  # TODO: QColor
    status_color_error_hovered: Any = 0xF47C83  # TODO: QColor
    status_color_error_pressed: Any = 0xFF9197  # TODO: QColor
    status_color_error_disabled: Any = 0xF9DADC  # TODO: QColor

    status_color_foreground: Any = 0xFFFFFF  # TODO: QColor
    status_color_foreground_hovered: Any = 0xFFFFFF  # TODO: QColor
    status_color_foreground_pressed: Any = 0xFFFFFF  # TODO: QColor
    status_color_foreground_disabled: Any = 0x99FFFFFF  # TODO: QColor (argb32)

    shadow_color1: Any = 0x20000000  # TODO: QColor (argb32)
    shadow_color2: Any = 0x40000000  # TODO: QColor (argb32)
    shadow_color3: Any = 0x60000000  # TODO: QColor (argb32)
    shadow_color_transparent: Any = 0x00000000  # TODO: QColor (argb32)

    border_color: Any = 0xD3D3D3  # TODO: QColor
    border_color_hovered: Any = 0xB3B3B3  # TODO: QColor
    border_color_pressed: Any = 0xA3A3A3  # TODO: QColor
    border_color_disabled: Any = 0xE9E9E9  # TODO: QColor
    border_color_transparent: Any = 0x00D3D3D3  # TODO: QColor (argb32)

    semi_transparent_color1: Any = 0x00000000  # TODO: QColor (argb32)
    semi_transparent_color2: Any = 0x19000000  # TODO: QColor (argb32)
    semi_transparent_color3: Any = 0x21000000  # TODO: QColor (argb32)
    semi_transparent_color4: Any = 0x28000000  # TODO: QColor (argb32)
    semi_transparent_color_transparent: Any = 0x00000000  # TODO: QColor (argb32)

    use_system_fonts: bool = False

    font_size: int = 12
    font_size_monospace: int = 13
    font_size_h1: int = 34
    font_size_h2: int = 26
    font_size_h3: int = 22
    font_size_h4: int = 18
    font_size_h5: int = 14
    font_size_s1: int = 10

    animation_duration: int = 192
    focus_animation_duration: int = 384
    slider_animation_duration: int = 96

    border_radius: float = 6.0
    check_box_border_radius: float = 4.0
    menu_item_border_radius: float = 4.0
    menu_bar_item_border_radius: float = 2.0
    border_width: int = 1

    control_height_large: int = 28
    control_height_medium: int = 24
    control_height_small: int = 16
    control_default_width: int = 96

    dial_mark_length: int = 8
    dial_mark_thickness: int = 2
    dial_tick_length: int = 4
    dial_tick_spacing: int = 4
    dial_groove_thickness: int = 4

    focus_border_width: int = 2

    icon_size: QSizeLike = (16, 16)
    icon_size_medium: QSizeLike = (24, 24)
    icon_size_large: QSizeLike = (24, 24)
    icon_size_extra_small: QSizeLike = (12, 12)

    slider_tick_size: int = 3
    slider_tick_spacing: int = 2
    slider_tick_thickness: int = 1
    slider_groove_height: int = 4

    progress_bar_groove_height: int = 6
    spacing: int = 8

    scroll_bar_thickness_full: int = 12
    scroll_bar_thickness_small: int = 6
    scroll_bar_margin: int = 0

    tab_bar_padding_top: int = 4
    tab_bar_tab_max_width: int = 0
    tab_bar_tab_min_width: int = 0

    font_regular: Any = None  # TODO: QFont
    font_bold: Any = None  # TODO: QFont
    font_h1: Any = None  # TODO: QFont
    font_h2: Any = None  # TODO: QFont
    font_h3: Any = None  # TODO: QFont
    font_h4: Any = None  # TODO: QFont
    font_h5: Any = None  # TODO: QFont
    font_caption: Any = None  # TODO: QFont
    font_monospace: Any = None  # TODO: QFont

    palette: Any = None  # TODO: QPalette
