"""Charts for the farm observations."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def create_charts(rows, output_dir="outputs"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No observations yet. Add observations before creating charts.")

    # Yield by observation date
    dates = [row["observation_date"] for row in rows]
    yields = [row["yield_kg"] for row in rows]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(dates, yields, marker="o")
    ax.set_title("Recorded Crop Yield Over Time")
    ax.set_xlabel("Observation date")
    ax.set_ylabel("Yield (kg)")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    yield_path = output_dir / "yield_over_time.png"
    fig.savefig(yield_path, dpi=150)
    plt.close(fig)

    # Rainfall vs yield
    rainfall = [row["rainfall_mm"] for row in rows]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(rainfall, yields)
    ax.set_title("Rainfall vs Recorded Yield")
    ax.set_xlabel("Rainfall (mm)")
    ax.set_ylabel("Yield (kg)")
    fig.tight_layout()
    scatter_path = output_dir / "rainfall_vs_yield.png"
    fig.savefig(scatter_path, dpi=150)
    plt.close(fig)
    return [yield_path, scatter_path]
