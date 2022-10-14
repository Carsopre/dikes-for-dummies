from dikesfordummies.dike.dike_profile import DikeProfile
from dikesfordummies.dike.dike_reinforcement_profile import DikeReinforcementProfile


class TestDikeReinforcementProfile:

    def test_initialize(self):
        _profile = DikeReinforcementProfile()
        assert isinstance(_profile, DikeReinforcementProfile)
        assert isinstance(_profile, DikeProfile)
        assert issubclass(DikeReinforcementProfile, DikeReinforcementProfile)
        assert str(_profile) == "Reinforced Profile"
    