from typing import Type

import pytest
from shapely.geometry import Point

from dikesfordummies.dike.dike_input import DikeInput
from dikesfordummies.dike.dike_profile import DikeProfile
from dikesfordummies.dike.dike_profile_builder import DikeProfileBuilder
from dikesfordummies.dike.dike_profile_protocol import DikeProfileProtocol
from dikesfordummies.dike.dike_reinforcement_profile import DikeReinforcementProfile


class TestDikeProfileBuilder:
    def test_initialize(self):
        _builder = DikeProfileBuilder()
        assert isinstance(_builder, DikeProfileBuilder)
        assert not _builder.dike_input
        assert not _builder.dike_type

    def test_from_input(self):
        # 1. Define test data.
        _input = DikeInput()

        # 2. Run test
        _builder = DikeProfileBuilder.from_input(_input)

        # 3. Verify expectations
        assert isinstance(_builder, DikeProfileBuilder)
        assert _builder.dike_input == _input

    def test_given_no_dike_input_when_build_then_raises(self):
        with pytest.raises(ValueError) as exc_err:
            DikeProfileBuilder().build()

        assert str(exc_err.value) == "Input Profile should be provided."

    @pytest.mark.parametrize(
        "dike_type", [pytest.param(DikeProfile), pytest.param(DikeReinforcementProfile)]
    )
    def test_given_valid_dike_input_when_build_then_raises(
        self, dike_type: Type[DikeProfileProtocol]
    ):
        _builder = DikeProfileBuilder()
        _builder.dike_type = dike_type
        _input = DikeInput()
        _input.buiten_maaiveld = 0
        _input.buiten_talud = 3
        _input.buiten_berm_hoogte = 0
        _input.buiten_berm_breedte = 0
        _input.kruin_hoogte = 6
        _input.kruin_breedte = 5
        _input.binnen_talud = 3
        _input.binnen_berm_hoogte = 0
        _input.binnen_berm_breedte = 0
        _input.binnen_maaiveld = 0
        _builder.dike_input = _input

        # 2. Run test
        _dike_profile = _builder.build()

        # 3. Verify final expectations.
        assert isinstance(_dike_profile, dike_type)
        assert isinstance(_dike_profile, DikeProfileProtocol)
        assert len(_dike_profile.characteristic_points) == 8
        assert all(isinstance(_p, Point) for _p in _dike_profile.characteristic_points)
