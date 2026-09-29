"""Analysis and CSV export functions."""

import csv
from collections import defaultdict
from pathlib import Path


def summarize(rows):
    if not rows:
        return []
    grouped = defaultdict(lambda: {"crop": "", "area": 0.0, "observations": 0,
                                   "total_yield": 0.0, "total_rainfall": 0.0})
    for row in rows:
        item = grouped[row["plot_id"]]
        item["crop"] = row["crop_type"]
        item["area"] = row["area_hectares"]
        item["observations"] += 1
        item["total_yield"] += row["yield_kg"]
        item["total_rainfall"] += row["rainfall_mm"]

    results = []
    for plot_id, item in grouped.items():
        n = item["observations"]
        results.append({
            "plot_id": plot_id,
            "crop": item["crop"],
            "observations": n,
            "total_yield_kg": item["total_yield"],
            "avg_rainfall_mm": item["total_rainfall"] / n,
            "yield_per_hectare_kg": item["total_yield"] / item["area"],
        })
    return sorted(results, key=lambda x: x["plot_id"])


def export_csv(rows, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fields = ["plot_id", "plot_name", "crop_type", "area_hectares",
              "observation_date", "rainfall_mm", "yield_kg"]
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return destination
