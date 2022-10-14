from __future__ import annotations

import math
from typing import List, Tuple

from shapely.geometry import Point


class DikeProfile:

    characteristic_points: List[Point]

    def __init__(self) -> None:
        self.characteristic_points = []

    @property
    def height(self) -> float:
        """
        The greatest `y coordinate` in the `characteristic_points` (`List[Point]`).

        Returns:
            float: Highest y coordinate of the dike.
        """
        if not self.characteristic_points:
            return math.nan
        return max([p.y for p in self.characteristic_points])

    @property
    def width(self) -> float:
        """
        The greatest `x coordinate` in the `characteristic_points` (`List[Point]`).

        Returns:
            float: Highest x coordinate of the dike.
        """
        if not self.characteristic_points:
            return math.nan
        return self.characteristic_points[-1].x

    @classmethod
    def from_tuple_list(cls, tuple_list: List[Tuple[float, float]]) -> DikeProfile:
        """
        Initializes a `DikeProfile` with the given `tuple_list` mapped into a `List[Point]` representing the `characteristic_points` property.

        Args:
            tuple_list (List[Tuple[float, float]]): List of float tuples representing the characteristic points.

        Raises:
            ValueError: When no `tuple_list` is given.

        Returns:
            DikeProfile: Instance with valid `characteristic points`.
        """
        if not tuple_list:
            raise ValueError("tuple_list argument required.")
        _dike = cls()
        _dike.set_points_from_tuples(tuple_list)
        return _dike
