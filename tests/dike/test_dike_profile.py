import math
from typing import Any

import pytest

from dikesfordummies.dike.dike_profile import DikeProfile
from dikesfordummies.dike.dike_profile_protocol import DikeProfileProtocol


class TestDikeProfile:
    def test_initialize(self):
        _dike_profile = DikeProfile()
        assert isinstance(_dike_profile, DikeProfile)
        assert isinstance(_dike_profile, DikeProfileProtocol)
        assert not _dike_profile.characteristic_points
        assert math.isnan(_dike_profile.height)
        assert math.isnan(_dike_profile.width)

    @pytest.mark.parametrize(
        "list_value",
        [pytest.param(None, id="None value"), pytest.param([], id="Empty list")],
    )
    def test_given_no_tuple_list_when_from_tuple_list_then_raises(
        self, list_value: Any
    ):
        _expected_err = "tuple_list argument required."
        with pytest.raises(ValueError) as exc_err:
            DikeProfile.from_tuple_list(list_value)
        assert str(exc_err.value) == _expected_err

    def test_given_tuple_list_when_from_tuple_list_then_returns_profile(self):
        # 1. Define test data.
        _tuple_list = list(zip(range(0, 20, 2), [0, 3, 5, 5, 3, 0]))

        # 2. Run test
        _dike = DikeProfile.from_tuple_list(_tuple_list)

        # 3. Verify expectations
        assert isinstance(_dike, DikeProfile)
        assert isinstance(_dike, DikeProfileProtocol)
        assert len(_dike.characteristic_points) == len(_tuple_list)
        assert all((p.x, p.y) in _tuple_list for p in _dike.characteristic_points)
        assert _dike.height == 5
        assert _dike.width == 10
