from __future__ import annotations

import math
from typing import List


class DikeInput:
    """
    Data structure containing the necessary data to generate Characteristic Points.
    """

    def __init__(self) -> None:
        self.buiten_maaiveld = math.nan
        self.buiten_talud = math.nan
        self.buiten_berm_hoogte = math.nan
        self.buiten_berm_breedte = math.nan
        self.kruin_hoogte = math.nan
        self.kruin_breedte = math.nan
        self.binnen_talud = math.nan
        self.binnen_berm_hoogte = math.nan
        self.binnen_berm_breedte = math.nan
        self.binnen_maaiveld = math.nan

    @classmethod
    def from_list(cls, values: List[float]) -> DikeInput:
        """
        Initializes a `DikeInput` with the given values mapped to the class' parameters.

        Args:
            values (List[float]): Values representing a Dike's profile data.

        Raises:
            ValueError: When the values given do not match the amount expected.

        Returns:
            DikeInput: Instanciated object with set data.
        """
        _input = cls()
        _dike_keys = _input.__dict__.keys()
        if not values or len(values) != len(_dike_keys):
            if not values:
                values = []
            raise ValueError(
                "Expected {} values, {} provided".format(len(_dike_keys), len(values))
            )

        for idx, key in enumerate(_dike_keys):
            _input.__dict__[key] = values[idx]
        return _input
