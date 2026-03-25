"""RadiusesF - per-corner border radius specification."""

from __future__ import annotations

__all__ = ["RadiusesF"]


class RadiusesF:
    """Per-corner border radius specification."""

    __slots__ = ("topLeft", "topRight", "bottomRight", "bottomLeft")

    def __init__(
        self,
        top_left_or_uniform: float = 0.0,
        top_right: float | None = None,
        bottom_right: float | None = None,
        bottom_left: float | None = None,
    ) -> None:
        if top_right is None:
            # Uniform radius
            self.topLeft = top_left_or_uniform
            self.topRight = top_left_or_uniform
            self.bottomRight = top_left_or_uniform
            self.bottomLeft = top_left_or_uniform
        else:
            self.topLeft = top_left_or_uniform
            self.topRight = top_right
            self.bottomRight = bottom_right if bottom_right is not None else 0.0
            self.bottomLeft = bottom_left if bottom_left is not None else 0.0

    def hasSameRadius(self) -> bool:
        return (
            self.topLeft == self.topRight
            and self.topRight == self.bottomRight
            and self.bottomRight == self.bottomLeft
        )

    def hasDifferentRadius(self) -> bool:
        return not self.hasSameRadius()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RadiusesF):
            return NotImplemented
        return (
            self.topLeft == other.topLeft
            and self.topRight == other.topRight
            and self.bottomRight == other.bottomRight
            and self.bottomLeft == other.bottomLeft
        )

    def __add__(self, other: float | int) -> RadiusesF:
        return RadiusesF(
            self.topLeft + other,
            self.topRight + other,
            self.bottomRight + other,
            self.bottomLeft + other,
        )

    def __radd__(self, other: float | int) -> RadiusesF:
        return self.__add__(other)

    def __repr__(self) -> str:
        return (
            f"RadiusesF({self.topLeft}, {self.topRight}, "
            f"{self.bottomRight}, {self.bottomLeft})"
        )
