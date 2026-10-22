import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter

from sap_data import FIG

# Validated categorical order (dataviz reference palette, light mode). Assign in this order, never cycle.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
MUTED = "#b8b7b2"
INK = "#0b0b0b"
INK_2 = "#52514e"

usd = FuncFormatter(lambda x, _: f"${x / 1e6:.1f}M" if abs(x) >= 1e6 else f"${x / 1e3:.0f}k" if abs(x) >= 1e3 else f"${x:.0f}")
pct = PercentFormatter(1.0, decimals=0)


def style():
    plt.rcParams.update({
        "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
        "axes.edgecolor": MUTED, "axes.labelcolor": INK_2, "axes.titlecolor": INK,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#e8e7e3", "grid.linewidth": 0.8, "axes.axisbelow": True,
        "xtick.color": INK_2, "ytick.color": INK_2, "font.size": 10,
        "axes.prop_cycle": plt.cycler(color=SERIES),
        "legend.frameon": False, "lines.linewidth": 2, "lines.markersize": 7,
    })


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=200, bbox_inches="tight")
