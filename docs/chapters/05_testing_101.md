# Chapter 05. Testing 101
Catching up? Just run the following command in your command line:
```bash
conda env create -f environment.yml
conda activate dikes-for-dummies_env
poetry install
```
You can follow the contents of this chapter now :)

## Intro
We are now going to start writing tests to either verify our current implementations but also to start doing some Test Driven Development.

If you installed the package (`poetry install`) you should have already [pytest](https://docs.pytest.org/en/7.1.x/), otherwise add it to your .toml like follows:
```
poetry add pytest --dev
```

## Pre-conditions.
Pytest will automatically detect your tests under the following conditions:
- they are in the tests directory.
- test files start with test_ prefix.
- test methods start with prefix test_

## Building the test structure.
Like in many other things in Python, there is not just one way to do this. However, my recommendation is to have a test directory under your root project, at the same level of your package, in our case it should look now like this:
```
\dikes-for-dummies
    \docs
    \dikesfordummies
        \dike
            __init__.py
            dike_profile.py
            dike_reinforcement_input.py
            dike_reinforcement_profile.py
        __init__.py
    \tests
        __init__.py
    environment.yml
    pyproject.toml
    README.md
    LICENSE
```

As we build up tests in our package I like to 'mirror' the structure in the code directory, so it's easier to understand what is actually being covered. So something like:

```
\dikes-for-dummies
    \docs
    \dikesfordummies
        \dike
            __init__.py
            dike_profile.py
            dike_reinforcement_input.py
            dike_reinforcement_profile.py
        __init__.py
    \tests
        \dike
            __init__.py
            test_dike_profile.py
            test_dike_reinforcement_input.py
            test_dike_reinforcement_profile.py
        __init__.py
        test_acceptance.py
    environment.yml
    pyproject.toml
    README.md
    LICENSE
```

## Creating a test
We have pytest and a file already in the tests directory. But now we miss tests, let's write one to verify the DikeProfile class:

```python
import math

from dikesfordummies.dike.dike_profile import DikeProfile


def test_initiate_dikeprofile():
    _dike = DikeProfile()
    assert isinstance(_dike, DikeProfile)
    assert not _dike.characteristic_points
    assert math.isnan(_dike.height)
    assert math.isnan(_dike.width)
```
If everything is in order the test explorer should be displaying now this test to run or debug. 

In case it is not being display, it is a good occasion to check the python output console and check what might be causing the error. 

>Because of Python not being compiled, discovering tests is (in occasions) the best way to ensure your solution is _problem free_.

It is also possible to run the tests via command line:

```
poetry run pytest -V
```

You could also encapsulate the test in a class (my preferred choice).

```python
import math

from dikesfordummies.dike.dike_profile import DikeProfile

class TestDikeProfile:

    def test_initiate_dikeprofile(self):
        _dike = DikeProfile()
        assert isinstance(_dike, DikeProfile)
        assert not _dike.characteristic_points
        assert math.isnan(_dike.height)
        assert math.isnan(_dike.width)
```

### Verifying risen errors:
Of course we can also test that an error is risen:
```python
def test_given_no_tuple_list_when_from_tuple_list_then_raises():
    _expected_err = "tuple_list argument required."
    with pytest.raises(ValueError) as exc_err:
        DikeProfile.from_tuple_list(None)
    assert str(exc_err.value) == _expected_err
```

### Adding multiple cases.
By now, you should be wondering how to apply DRY to your tests. For instance, in the previous section, we could have also given an empty list (`[]`) because python operator `not` will also consider it as if it was `None` value. 

We will be using `pytest.mark.parametrize` and `pytest.param` for this:
```python
@pytest.mark.parametrize(
    "list_value",
    [pytest.param(None, id="None value"), pytest.param([], id="Empty list")]
)
def test_given_no_tuple_list_when_from_tuple_list_then_raises(list_value: Any):
    _expected_err = "tuple_list argument required."
    with pytest.raises(ValueError) as exc_err:
        DikeProfile.from_tuple_list(list_value)
    assert str(exc_err.value) == _expected_err
```

Our test suite should now detect multiple test cases for this test and allow us to run them either individually or all together.

This feature allow us for many possibilities. For instance:
```python
@pytest.mark.parametrize("a", [(1), (2), (3)])
@pytest.mark.parametrize("b", [(4), (5), (6)])
def test_dummy_multi_parameter(a: float, b: float):
    assert (a / b) <= 0.75
```
We will have a total of 9 cases, because all possibilities will be crossed.

> You can verify exact float values with pytest.approx(expected_value, tolerance)

Furthermore, pytest allows you to decide which tests to execute and whic note. for instance by using the custom decorator `@pytest.mark.acceptancetest` and running the specific command `pytest -v -m acceptancetest` we will only run the tests with said decorator.

We can also skip tests if, for instance, we do not wish to run them under certain conditions with `@pytest.mark.skipif()`: 
```python
import os

@pytest.mark.skipif(
    os.platform.system().lower() != "linux", reason="Only Linux supported"
)
def test_only_run_this_test_in_linux():
    pass
```

Of course, we can create our own markers to stay _DRY_:
```python
import platform

only_linux = pytest.mark.skipif(
    platform.system().lower() != "linux", reason="Only Linux supported"
)

@only_linux
def test_a_test_for_linux():
    pass

@only_linux
def test_another_for_linx():
    pass
```

### Using fixtures.
Pytest also allows us for tear up / tear down fixtures. These are broad, so we will just see a few common examples.
- Providing a common object across the test suite.
    ```python
    @pytest.fixture(scope="function", autouse=False)
    def base_dikeprofile():
        _dike = DikeProfile()
        _dike.characteristic_points = list(map(Point, zip(range(0, 4), range(0, 4))))
        assert len(_dike.characteristic_points) == 4
        assert _dike.width == _dike.height == 3


    def test_using_a_fixture(base_dikeprofile: DikeProfile):
        assert isinstance(base_dikeprofile, DikeProfile)
    ```
- Providing initial data and cleaning it up afterwards.
    ```python
    @pytest.fixture(scope="module")
    def base_output_dir():
        _test_results = Path(__file__).parent / "test_results"
        _test_suite_results = _test_results / "acceptance_tests"
        _test_suite_results.mkdir(parents=True, exist_ok=True)

        # Give data to the test.
        yield _test_suite_results

        # This code executes after the test ends
        if _test_suite_results.is_dir():
            shutil.rmtree(_test_suite_results, ignore_errors=True)


    def test_using_a_fixture(base_output_dir: Path, request: pytest.FixtureRequest):
        this_test_results = base_output_dir / request.node.name
        this_test_results.mkdir(parents=True)
        pytest.fail("This is a dumb test")
    ```

## Workflows on GitHub
Yoy may find multiple solutions by googling this, but our most common pipeline in Python is something similar to this:

```yml
name: ci-on-push-and-autoformat
on:
  pull_request:
    types: [opened, synchronize, reopened]
  push:
    branches:
      - master
jobs:

  CI:
    if: "!startsWith(github.event.head_commit.message, 'bump:')"
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.10']
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    permissions: write-all
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v1
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run image
        uses: abatilo/actions-poetry@v2.0.0
        with:
          poetry-version: 1.1.8
      - name: Cache Poetry virtualenv
        uses: actions/cache@v1
        id: cache
        with:
          path: ~/.virtualenvs
          key: venv-${{ matrix.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}
          restore-keys: |
            venv-${{ matrix.os }}-${{ matrix.python-version }}-

      - name: Set Poetry config
        run: |
          poetry config virtualenvs.in-project false
          poetry config virtualenvs.path ~/.virtualenvs

      - name: Install Dependencies
        run: poetry install
        if: steps.cache.outputs.cache-hit != 'true'

      - name: Test with pytest
        run: |
          poetry run pytest --cov=dikesfordummies --cov-report xml:coverage-reports/coverage-dikesfordummies-src.xml --junitxml=xunit-reports/xunit-result-dikesfordummies-src.xml
          poetry run coverage xml -i

      - name: Autoformat code if the check fails
        if: ${{ (matrix.os == 'ubuntu-latest') && (matrix.python-version == 3.10) }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Needed to get PR information, if any
        run: |
          poetry run isort .
          poetry run black .
          git config --global user.name '${{ github.actor }}'
          git config --global user.email '${{ github.actor }}@users.noreply.github.com'
          git remote set-url origin https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/$GITHUB_REPOSITORY
          git checkout $GITHUB_HEAD_REF
          git commit -am "autoformat: isort & black" && git push || true

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        if: ${{ (matrix.os == 'ubuntu-latest') && (matrix.python-version == 3.10) }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Needed to get PR information, if any
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

> You need to save the above content as a .yml file in the .github/workflows/ directory.

This pipeline will be executed during (any) pull-request and will ensure of several things:
- The poetry installation works
- The tests (all of them) are run correctly.
- If the tests are all succesful:
    - We will verify and format all the python files in our project.
    - We will run a SonarCloud Scan (Follow the steps in the admin page of SonarCloud)

In addition, thanks to [commitizen](https://commitizen-tools.github.io/commitizen/) we can also add a step to 'bump' the package version and create new entries of the changelog. However, it is also possible as a manual step:
`cz bump --changelog`.

## Summary
Although there is still much more to see, we have seen enough resources to create our own test suite and execute it either in a GitHub workflow, or in a TeamCity step. 

Now it is time to create tests and searching for more ways of providing quality to your tool.