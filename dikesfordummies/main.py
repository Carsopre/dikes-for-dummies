from pathlib import Path
from typing import List, Optional

import click

from dikesfordummies import workflows

_default_input = workflows._default_input
_dike_keys = ", ".join(_default_input.keys())


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
