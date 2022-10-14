import math

from dikesfordummies.dike.dike_reinforcement_input import DikeReinforcementInput


class TestDikeReinforcementInput:
    def test_initialize(self):
        _input = DikeReinforcementInput()
        assert isinstance(_input, DikeReinforcementInput)
        assert math.isnan(_input.width)
        assert math.isnan(_input.height)
