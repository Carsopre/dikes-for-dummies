import pytest

from dikesfordummies.dike.dike_profile_protocol import DikeProfileProtocol


class TestDikeProfileProtocol:
    def test_initialize(self):
        with pytest.raises(TypeError):
            DikeProfileProtocol()
