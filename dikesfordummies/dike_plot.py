from matplotlib import pyplot
from shapely.geometry import LineString

from dikesfordummies.dike.dike_profile_protocol import DikeProfileProtocol


def _plot_line(ax, ob, color):
    parts = hasattr(ob, "geoms") and ob or [ob]
    for part in parts:
        x, y = part.xy
        ax.plot(x, y, color=color, linewidth=3, solid_capstyle="round", zorder=1)


def plot_profile(dike_profile: DikeProfileProtocol) -> pyplot:
    """
    Plots a dike profile (`DikeProfileProtocol`) using matplotlib and a predefined color.

    Args:
        dike_profile (DikeProfileProtocol): Profile to plot.

    Returns:
        pyplot: Plot containing a graphical interpretation of the Dike's profile geometry.
    """
    fig = pyplot.figure(1, dpi=90)
    _subplot = fig.add_subplot(221)
    _plot_line(
        _subplot, LineString(dike_profile.characteristic_points), color="#03a9fc"
    )
    return fig
