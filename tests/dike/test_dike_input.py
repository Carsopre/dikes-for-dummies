import math
from typing import Any

import pytest

from dikesfordummies.dike.dike_input import DikeInput


class TestDikeInput:
    def test_initialize(self):
        _input = DikeInput()
        assert isinstance(_input, DikeInput)
        assert math.isnan(_input.buiten_maaiveld)
        assert math.isnan(_input.buiten_talud)
        assert math.isnan(_input.buiten_berm_hoogte)
        assert math.isnan(_input.buiten_berm_breedte)
        assert math.isnan(_input.kruin_hoogte)
        assert math.isnan(_input.kruin_breedte)
        assert math.isnan(_input.binnen_talud)
        assert math.isnan(_input.binnen_berm_hoogte)
        assert math.isnan(_input.binnen_berm_breedte)
        assert math.isnan(_input.binnen_maaiveld)

    def test_from_list(self):
        # 1. Define test data.
        _test_dict = dict(
            buiten_maaiveld=0,
            buiten_talud=3,
            buiten_berm_hoogte=0,
            buiten_berm_breedte=0,
            kruin_hoogte=6,
            kruin_breedte=5,
            binnen_talud=3,
            binnen_berm_hoogte=0,
            binnen_berm_breedte=0,
            binnen_maaiveld=0,
        )

        # 2. Run test
        _input = DikeInput.from_list(list(_test_dict.values()))

        # 3. Verify results
        assert _input.__dict__ == _test_dict

    @pytest.mark.parametrize(
        "values",
        [
            pytest.param([], id="Empty list"),
            pytest.param(list(range(11)), id="11 elements"),
            pytest.param(list(range(9)), id="9 elements"),
        ],
    )
    def test_from_list_no_values_raises(self, values: Any):
        _len_values = 0
        if values:
            _len_values = len(values)
        _exp_error = f"Expected 10 values, {_len_values} provided"

        with pytest.raises(ValueError) as exc_err:
            DikeInput.from_list(values)
        assert str(exc_err.value) == _exp_error
