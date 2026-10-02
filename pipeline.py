"""Capstone-style CSV ingestion, validation, transformation, and reporting."""
import csv
from datetime import date
from pathlib import Path
from database import FarmDatabase
from models import FarmPlot, CropObservation


REQUIRED_COLUMNS = {
    "plot_name", "location", "crop_type", "area_hectares",
    "observation_date", "rainfall_mm", "yield_kg"
}


def read_observations_csv(csv_path):
    """Read CSV rows, normalize text/numbers, and reject invalid records."""
    records = []
    errors = []
    with Path(csv_path).open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError("CSV is missing required columns: " + ", ".join(sorted(missing)))
        for line_number, raw in enumerate(reader, start=2):
            try:
                record = {
                    "plot_name": raw["plot_name"].strip(),
                    "location": raw["location"].strip(),
                    "crop_type": raw["crop_type"].strip(),
                    "area_hectares": float(raw["area_hectares"]),
                    "observation_date": date.fromisoformat(raw["observation_date"].strip()).isoformat(),
                    "rainfall_mm": float(raw["rainfall_mm"]),
                    "yield_kg": float(raw["yield_kg"]),
                    "note": (raw.get("note") or "").strip(),
                }
                if not all(record[k] for k in ("plot_name", "location", "crop_type")):
                    raise ValueError("plot name, location, and crop type are required")
                if record["area_hectares"] <= 0 or record["rainfall_mm"] < 0 or record["yield_kg"] < 0:
                    raise ValueError("area must be positive; rainfall and yield cannot be negative")
                records.append(record)
            except (TypeError, ValueError) as exc:
                errors.append(f"Line {line_number}: {exc}")
    return records, errors


def import_observations(csv_path, db=None):
    """Import valid CSV records; skip duplicate plot/date/rainfall/yield rows."""
    db = db or FarmDatabase()
    records, errors = read_observations_csv(csv_path)
    imported = 0
    skipped = 0
    for item in records:
        plot = next((p for p in db.list_plots()
                     if p.name == item["plot_name"] and p.location == item["location"]
                     and p.crop_type == item["crop_type"]), None)
        if plot is None:
            plot_id = db.add_plot(FarmPlot(item["plot_name"], item["location"],
                                           item["crop_type"], item["area_hectares"]))
        else:
            plot_id = plot.plot_id
        with db.connect() as conn:
            exists = conn.execute("""
                SELECT 1 FROM observations
                WHERE plot_id=? AND observation_date=? AND rainfall_mm=? AND yield_kg=?
            """, (plot_id, item["observation_date"], item["rainfall_mm"], item["yield_kg"])).fetchone()
        if exists:
            skipped += 1
            continue
        db.add_observation(CropObservation(
            plot_id, item["observation_date"], item["rainfall_mm"],
            item["yield_kg"], item["note"]
        ))
        imported += 1
    return {"read": len(records), "imported": imported, "duplicates_skipped": skipped, "errors": errors}
