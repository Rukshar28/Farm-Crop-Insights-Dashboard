# Farm & Crop Insights Dashboard

A beginner-friendly Python project demonstrating Object-Oriented Programming, object lifecycle, inheritance, SQLite databases, data analysis, and visualization.

## Project goal
Track farm plots and crop observations, store them in SQLite, and generate useful charts from sample data. This is a learning/demo project using fictional sample data—not a production agronomy or yield-prediction system.

## Features
- Add/list farm plots
- Add/list crop observations (date, rainfall, yield)
- SQLite persistence with a foreign-key relationship
- OOP domain model with inheritance
- Summary analytics by plot and crop
- Save charts as PNG files
- Optional CSV export of observations
- Sample data seeded automatically on first run
- Lifecycle demonstration showing construction and cleanup concepts

## Requirements
- Python 3.10+
- Packages in `requirements.txt`

## Setup (Windows PowerShell)
```powershell
cd farm_crop_insights
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py main.py
```

If PowerShell blocks activation, you can skip activation and use:
```powershell
py -m pip install -r requirements.txt
py main.py
```

## Menu
Choose an option in the terminal:
1. List plots
2. Add a plot
3. Add an observation
4. List observations
5. Show analytics summary
6. Generate charts
7. Export observations to CSV
8. Run object lifecycle demo
0. Exit

The SQLite database is created at `data/farm_insights.db`. Charts are saved under `outputs/`.

## Topics mapped to course concepts
| Course topic | Where to find it |
|---|---|
| Classes and objects | `models.py` (`FarmEntity`, `FarmPlot`, `CropObservation`) |
| Constructors | `__init__` methods in `models.py` |
| Inheritance | `FarmPlot` and `CropObservation` inherit from `FarmEntity` |
| Attributes and methods | Domain classes in `models.py` |
| Object lifecycle / destructor | `lifecycle_demo.py` |
| Database connection lifecycle | `database.py` uses a context manager (`with`) |
| SQL / relational data | `database.py` |
| Data analysis | `analytics.py` |
| Visualization | `visualization.py` |
| CSV | `analytics.py` |

## Important note about `__del__`
Python's `__del__` may run when an object is garbage-collected, but its timing is not guaranteed. Do not use it to close database connections or other critical resources. This project uses a context manager for predictable database cleanup and keeps `__del__` in a separate educational demo.

## Suggested demo for Hrishi (5 minutes)
1. Explain the use case: organize plot observations and inspect yield/rainfall patterns.
2. Add a plot and one observation through the menu.
3. Show the SQLite database persists data between runs.
4. Run the summary and generate charts.
5. Point out the class hierarchy and explain how future features can be added.

## Future improvements (incremental roadmap)
1. Add CSV import for real observations.
2. Add validation (nonnegative area/rainfall/yield; valid dates).
3. Add filters by crop, plot, and date range.
4. Build a Streamlit web dashboard.
5. Add weather/API integration with proper source attribution and error handling.
6. Add unit tests and logging.
7. Explore a simple yield-estimation model only after collecting enough reliable, representative data; evaluate it against a baseline and clearly communicate uncertainty.

## Data fields
- Plot: name, location, crop type, area in hectares
- Observation: plot ID, date, rainfall in mm, yield in kg

All bundled sample records are fictional and intended only for testing.
