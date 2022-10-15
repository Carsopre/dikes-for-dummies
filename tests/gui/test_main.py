import shutil

import pytest

from dikesfordummies.gui.main import MainWindow
from tests import test_results


class TestMainWindow:
    def test_gui(self, request: pytest.FixtureRequest):
        # 1. Define test data.
        _mw = MainWindow(parent=None)
        _test_dir = test_results / request.node.name
        shutil.rmtree(_test_dir, ignore_errors=True)

        # 2. Run test.
        _mw._output_dir = _test_dir
        _mw._plot_profile()

        # 3. Verify expectations
        assert _test_dir.is_dir()
        assert any(_test_dir.glob("*.png"))
