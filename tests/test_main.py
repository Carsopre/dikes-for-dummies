import shutil

import pytest
from click.testing import CliRunner

from dikesfordummies import main
from tests import test_results


def test_given_valid_input_generates_default_profile(request: pytest.FixtureRequest):
    # 1. Define test data.
    _test_dir = test_results / request.node.name
    _test_file = _test_dir / "profile.png"

    shutil.rmtree(_test_dir, ignore_errors=True)
    _args = ["--outfile", _test_file]

    # 2. Run test.
    _run_result = CliRunner().invoke(main.plot_profile, _args)

    # 3. Verify expectations.
    assert _run_result.exit_code == 0
    assert _test_file.is_file()
