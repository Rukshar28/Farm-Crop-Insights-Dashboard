
from pathlib import Path
from models import FarmPlot, CropObservation
from database import FarmDatabase
from analytics import summarize, export_csv
from visualization import create_charts
from lifecycle_demo import run_demo

db = FarmDatabase()
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "outputs"


def seed_sample_data():
    if db.count_plots() > 0:
        return
    plot_ids = [
        db.add_plot(FarmPlot("North Field", "Demo Farm", "Wheat", 2.0)),
        db.add_plot(FarmPlot("River Plot", "Demo Farm", "Rice", 1.5)),
        db.add_plot(FarmPlot("East Field", "Demo Farm", "Maize", 1.2)),
    ]
    samples = [
        (plot_ids[0], "2026-06-01", 22, 420, "Fictional sample"),
        (plot_ids[1], "2026-06-01", 48, 510, "Fictional sample"),
        (plot_ids[2], "2026-06-02", 30, 360, "Fictional sample"),
        (plot_ids[0], "2026-06-15", 18, 455, "Fictional sample"),
        (plot_ids[1], "2026-06-15", 55, 545, "Fictional sample"),
        (plot_ids[2], "2026-06-16", 27, 390, "Fictional sample"),
    ]
    for values in samples:
        db.add_observation(CropObservation(*values))


def show_plots():
    plots = db.list_plots()
    if not plots:
        print("No plots found.")
    for plot in plots:
        print(plot.describe())


def add_plot():
    print("Enter plot details:")
    name = input("Plot name: ").strip()
    location = input("Location/farm: ").strip()
    crop = input("Crop type: ").strip()
    area = float(input("Area in hectares: "))
    plot_id = db.add_plot(FarmPlot(name, location, crop, area))
    print(f"Added plot with ID {plot_id}.")


def add_observation():
    show_plots()
    plot_id = int(input("Plot ID: "))
    day = input("Observation date (YYYY-MM-DD): ").strip()
    rain = float(input("Rainfall (mm): "))
    yield_kg = float(input("Yield (kg): "))
    note = input("Note (optional): ").strip()
    observation = CropObservation(plot_id, day, rain, yield_kg, note)
    obs_id = db.add_observation(observation)
    print(f"Saved observation #{obs_id}.")


def show_observations():
    rows = db.list_observations()
    if not rows:
        print("No observations found.")
    for row in rows:
        print(f"#{row['id']} | {row['plot_name']} ({row['crop_type']}) | "
              f"{row['observation_date']} | rain {row['rainfall_mm']} mm | "
              f"yield {row['yield_kg']} kg")


def show_analytics():
    results = summarize(db.analytics_rows())
    if not results:
        print("No data available yet.")
        return
    print("\nPer-plot summary")
    print("-" * 78)
    for item in results:
        print(f"Plot {item['plot_id']} | {item['crop']:<8} | "
              f"observations: {item['observations']} | "
              f"total yield: {item['total_yield_kg']:.1f} kg | "
              f"avg rain: {item['avg_rainfall_mm']:.1f} mm | "
              f"yield/ha: {item['yield_per_hectare_kg']:.1f} kg/ha")


def main():
    seed_sample_data()
    print("Farm & Crop Insights Dashboard")
    while True:
        print("""
1. List plots
2. Add a plot
3. Add an observation
4. List observations
5. Show analytics summary
6. Generate charts
7. Export observations to CSV
8. Run object lifecycle demo
0. Exit
""")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                show_plots()
            elif choice == "2":
                add_plot()
            elif choice == "3":
                add_observation()
            elif choice == "4":
                show_observations()
            elif choice == "5":
                show_analytics()
            elif choice == "6":
                paths = create_charts(db.analytics_rows(), OUTPUT_DIR)
                print("Charts saved:")
                for path in paths:
                    print(path)
            elif choice == "7":
                path = export_csv(db.analytics_rows(), OUTPUT_DIR / "observations_export.csv")
                print(f"CSV exported to {path}")
            elif choice == "8":
                run_demo()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Please choose a listed option.")
        except (ValueError, KeyError) as error:
            print(f"Input/data error: {error}")
        except Exception as error:
            print(f"Operation failed: {error}")


if __name__ == "__main__":
    main()
