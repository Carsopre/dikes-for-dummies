from __future__ import annotations

from typing import List

from shapely.geometry import Point

from dikesfordummies.dike.dike_input import DikeInput
from dikesfordummies.dike.dike_profile import DikeProfile


class DikeProfileBuilder:
    """
    Class responsible of building a valid `DikeProfile` with a given `DikeInput`.

    Raises:
        ValueError: When trying to `build` without a valid `DikeInput`.

    Returns:
        DikeProfileBuilder: Builder.
    """

    dike_input: DikeInput

    def __init__(self) -> None:
        self.dike_input = None

    def _build_waterside(self) -> List[Point]:
        _p4 = Point(0, self.dike_input.kruin_hoogte)
        _p3_x = _p4.x - (
            (self.dike_input.kruin_hoogte - self.dike_input.buiten_berm_hoogte)
            * self.dike_input.buiten_talud
        )
        _p3 = Point(_p3_x, self.dike_input.buiten_berm_hoogte)
        _p2_x = _p3.x - self.dike_input.buiten_berm_breedte
        _p2 = Point(_p2_x, self.dike_input.buiten_berm_hoogte)
        _p1_x = _p2.x - (
            (self.dike_input.buiten_berm_hoogte - self.dike_input.buiten_maaiveld)
            * self.dike_input.buiten_talud
        )
        _p1 = Point(_p1_x, self.dike_input.buiten_maaiveld)
        return [_p1, _p2, _p3, _p4]

    def _build_polderside(self) -> List[Point]:
        _x_p5 = self.dike_input.kruin_breedte
        _p5 = Point(_x_p5, self.dike_input.kruin_hoogte)
        _x_p6 = _p5.x + (
            (self.dike_input.kruin_hoogte - self.dike_input.binnen_berm_hoogte)
            * self.dike_input.binnen_talud
        )
        _p6 = Point(_x_p6, self.dike_input.binnen_berm_hoogte)
        _x_p7 = _p6.x + self.dike_input.binnen_berm_breedte
        _p7 = Point(_x_p7, self.dike_input.binnen_berm_hoogte)
        _x_p8 = _p7.x + (
            (self.dike_input.binnen_berm_hoogte - self.dike_input.binnen_maaiveld)
            * self.dike_input.binnen_talud
        )
        _p8 = Point(_x_p8, self.dike_input.binnen_maaiveld)
        return [_p5, _p6, _p7, _p8]

    def build(self) -> DikeProfile:
        """
        Builds a `DikeProfile` based on the given `DikeInput`.

        Raises:
            ValueError: When the `DikeInput` is not given.

        Returns:
            DikeProfile: Valid instantiated DikeProfile.
        """
        if not self.dike_input:
            raise ValueError("Input Profile should be provided.")

        _dike_points: List[Point] = []
        _waterside = self._build_waterside()
        _polderside = self._build_polderside()
        _dike_points.extend(_waterside)
        _dike_points.extend(_polderside)
        _dike = DikeProfile()
        _dike.characteristic_points = _dike_points
        return _dike

    @classmethod
    def from_input(cls, dike_input: DikeInput) -> DikeProfileBuilder:
        """
        Initializes a `DikeProfileBuilder' with a valid `DikeInput` as `dike_input` parameter.

        Args:
            dike_input (DikeInput): Dike input to be set to the instance of the builder.

        Returns:
            DikeProfileBuilder: Valid instance of a DikeProfileBuilder instance.
        """
        _builder = cls()
        _builder.dike_input = dike_input
        return _builder