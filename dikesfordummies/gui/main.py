import sys
from pathlib import Path
from typing import Callable

from PyQt5 import QtWidgets

from dikesfordummies import workflows
from dikesfordummies.gui import utils


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
        """
        Runs the analysis
        :return:
        """
        # call DFS
        _outfile = None
        if self._output_dir:
            _outfile = self._output_dir / "default_plot.png"
        workflows.plot_dike_profile(list(workflows._default_input.values()), _outfile)


def main():
    app = QtWidgets.QApplication(sys.argv)
    screen = MainWindow()
    screen.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
