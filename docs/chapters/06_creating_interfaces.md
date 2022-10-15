# Chapter 06. Creating interfaces.
Catching up? Just run the following command in your command line:
```
conda env create -f environment.yml
conda activate dikes-for-dummies_env
poetry install
```

You can follow the contents of this chapter now :)

## Intro
It is time to work on an interface that provides an end user access to our tool when using it from command line, or later as an .exe.

We will just focus on two options.
* CLI - like, using the [click](https://click.palletsprojects.com/en/8.1.x/) library.
* GUI - like, using the [QT](https://www.qt.io/qt-for-python) library.

Other option would be to make an API, but we will not cover it here.

## Know your audience.
We have talked about this before, let's check again the potential uses of this package and its requirements:

| Usage / Requirements | Endpoints | Built | 
| ---   | :---: | :---: |
| Sandbox | - | - |
| Library | - | - |
| CLI | x | (Not necessarily) |
| API | x | (Running as a service) |
| GUI | x | x |

As we can see, endpoints are required for anything where the user is not 'coding'. Therefore it is a good idea to create our own internal application interface so that the endpoints can easilly call the required workflows.

It is recommended to leave your `core` functionality as a separate library. This will allow you to develop separate interfaces that __uses / imports__ your package. Allowing for better separation of concerns.

Of course if you just want to build a GUI or an API from the very beginning you could just go ahead and split everything in the project tree.

## Application workflows.

As mentioned, when not working in a 'sandbox' we need to provide certain workflows (or user cases) that provide an endpoint to the user. This endpoint can be later used by an CLI, API or GUI.

We will just define in a file a workflow that given some (optional) input will display or save a profile geometry. This workflow will work as an example for building a CLI or a GUI in the following steps.

```python
from pathlib import Path
from typing import List, Optional

from dikesfordummies import dike_plot
from dikesfordummies.dike.dike_input import DikeInput
from dikesfordummies.dike.dike_profile_builder import DikeProfileBuilder

def plot_dike_profile(dike_input: List[float], outfile: Optional[Path]) -> None:
    """
    Generates a `DikeProfile` plot with the reference data given in `dike_input`. The plot is either shown or saved depending on whether the argument `outfile` is given or not.

    Args:
        dike_input (List[float]): List of values representing a Dike's profile data.
        outfile (Optional[Path]): File path where to save the plot.
    """
    _dike_input = DikeInput.from_list(dike_input)
    _dike = DikeProfileBuilder.from_input(_dike_input).build()
    _plot = dike_plot.plot_profile(_dike)
    if not outfile:
        _plot.show()
        return
    elif outfile.is_file():
        outfile.unlink()
    if not outfile.parent.exists():
        outfile.parent.mkdir(parents=True)
    _plot.savefig(outfile)
```

## CLI with Click

To simplify our project structure, we will just create a `main.py` in the _dikesfordummies_ directory.

### Creating an endpoint.
Click provides us with a simple way of processing the information coming from command line and connecting it to our library. 

```bash
poetry add click
```

First, we need to make our file recognisible and 'executable':
```python
if __name__ == "__main__":
    ...
```

Now the command line should be able to pass their arguments. In `Click` we do this with `@click.command` and `@click.option`:

```python
from dikesfordummies import workflows

@click.command()
@click.option(
    "--dike_input",
    nargs=10,
    default=_default_input.values(),
    type=float,
    help=f"List of {len(_default_input.keys())} values for the dike input. Values represent {_dike_keys}.",
)
@click.option(
    "--outfile",
    type=click.Path(path_type=Path),
    help="The (optional) path where to save the profile plot.",
)
def plot_profile(dike_input: List[float], outfile: Optional[Path]):
    workflows.plot_dike_profile(dike_input, outfile)

if __name__ == "__main__":
    plot_profile()
``` 

Fortunately for us, `Click` already does the type checking for us. So we can assume that when an outfile parameter is given, then it will be of type `pathlib.Path` as specified in the argument `path_type`.

We can try to run this now:
```bash
python dikesfordummies\main.py plot_profile --help
```

### Creating multiple entry points.
You may be already wondering how to append more commands so that not just this method can be used. Well, that's easily solved by adding a `@click.group`:

```python
@click.group()
def cli():
    pass


@cli.command(name="plot_profile")
@click.option(...)
@click.option(...)
def plot_profile(dike_input: List[float], outfile: Optional[Path]):
    ...

if __name__ == "__main__":
    cli()
```

And if we try again the help command the same result should show.

We can try to run this now:
```bash
python dikesfordummies\main.py plot_profile --help
```

### Debugging from CLI.

It is relatively easy to extend the current settings to include a 'one-off' CLI call in our `launch.json`.

```json
{
    "version": "0.2.0",
    "configurations": [
        ...
        {
            "name": "CLI plot default dike",
            "type": "python",
            "request": "launch",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "program": "${workspaceFolder}\\dikesfordummies\\main.py",
            "args": [
                "plot_profile",
                "--outfile",
                "dike_plot.png"
            ],
            "justMyCode": true,
        },
        ...
    ]
}
```

### Testing our CLI.

Let's not forget about tests for our endpoints:

```python
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
```

## GUI with QT

Building a GUI in QT has its limitations if we compare to other great frameworks such as WPF. However, this should not prevent us from achieving our goals.

To simplify this project we will just create the logic in a directory __within__ _dikesfordummies_. In a production project you should try to have at least a separation of concerns such as:

Because we are just _playing around_ we will just create a new level in the project tree such as:
```
\dikesfordummies
    \core
        \dike
            ...
        ...
        main.py
    \gui
        ...
        main.py
    __init__.py
\tests
    \core
        ...
        main.py
    \gui
        ...
        main.py
    __init__.py
```
### Creating a basic GUI

With QT, all classical components are available. We will an interface that represents the previous endpoint.

```bash
poetry add pyqt5
```

We will create a new `main.py` which will contain GUI logic.

```python
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

def main():
    app = QtWidgets.QApplication(sys.argv)
    screen = MainWindow()
    screen.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
```

### Debugging from CLI
We can also add a debug setting:

```json
{
    "version": "0.2.0",
    "configurations": [
        ...
        {
            "name": "Run GUI Main window",
            "type": "python",
            "request": "launch",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "program": "${workspaceFolder}\\dikesfordummies\\gui\\main.py",
            "args": [],
            "justMyCode": true,
        },
        ...
    ]
)
```

### Adding workflows.
Let's make it simple, we want to plot, or save the default geometry.
We can demonstrate that with two simple buttons:

```python

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Dikes For Dummies")
        self._set_menu_options()

    def _set_menu_options(self) -> None:
        self._create_menu_button(
            50,
            "Output directory",
            "Select output directory for plot(s).",
            self._get_output_file,
        )
        self._create_menu_button(
            100, "Plot", "Plot default profile", self._plot_profile
        )

    def _get_output_file(self) -> None:
        _output_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select output plot directory."
        )
        if _output_dir:
            self._output_dir = Path(_output_dir)

    def _create_menu_button(
        self,
        ay_pos: float,
        title: str,
        tooltip: str,
        event: Callable,
        enabled: bool = True,
    ) -> QtWidgets.QPushButton:
        return utils.create_menu_button(
            self, dict(ax=50, ay=ay_pos, aw=160, az=30), title, tooltip, event, enabled
        )

    def _plot_profile(self):
        # call DFS
        _outfile = None
        if self._output_dir:
            _outfile = self._output_dir / "default_plot.png"
        workflows.plot_dike_profile(list(workflows._default_input.values()), _outfile)

```

With this, we are good to go. We have now a very simple GUI that connects to the rest of the library.

### Testing
Depending on your approach about testing gui's you may not need to do too much work. For our case, we can just simply test the initialization and plotting of a profile:

```python
def test_gui(request: pytest.FixtureRequest):
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
```

## Summary
That's it for this chapter. We have seen what the principles are towards creating interfaces in a python project. 