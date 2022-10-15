from pathlib import Path
from typing import List, Optional

from dikesfordummies import dike_plot
from dikesfordummies.dike.dike_input import DikeInput
from dikesfordummies.dike.dike_profile_builder import DikeProfileBuilder

_default_input = dict(
    buiten_maaiveld=0,
    buiten_talud=3,
    buiten_berm_hoogte=0,
    buiten_berm_breedte=0,
    kruin_hoogte=6,
    kruin_breedte=5,
    binnen_talud=3,
    binnen_berm_hoogte=0,
    binnen_berm_breedte=0,
    binnen_maaiveld=0,
)


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
