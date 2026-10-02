# Farm & Crop Insights Dashboard

A beginner-friendly, modular Python project demonstrating OOP, SQLite, CSV ETL, JSON/web APIs, data validation, analysis, and visualization.

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
- Lifecycle demonstration showing construction and cleanup concepts\n- Retrieve current weather by place name using Open-Meteo geocoding and forecast APIs (JSON over HTTP)\n- Save and review weather observations in SQLite\n- Import/validate/normalize CSV observations with duplicate protection\n- Automated unit tests for CSV validation and repeatable imports

## Requirements
- Python 3.10+
- Packages in `requirements.txt`

## Setup (Windows PowerShell)
```powershell
cd farm_crop_insights
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py main.py\n# Optional: run the test suite\npy -m unittest discover -s tests -v
```

If PowerShell blocks activation, you can skip activation and use:
```powershell
py -m pip install -r requirements.txt
py main.py\n# Optional: run the test suite\npy -m unittest discover -s tests -v
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
| CSV export | `analytics.py` |\n| CSV ingestion, validation, transformation, duplicate checks | `pipeline.py` |\n| HTTP requests, JSON decoding, API errors | `weather_api.py` |\n| SQLite weather persistence and parameterized queries | `database.py` (`weather_observations`) |\n| Unit testing | `tests/test_pipeline.py` |

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


## Course module mapping

### Using Python to Access Web Data
- `weather_api.py` uses `urllib.request` to make HTTP requests and `.decode("utf-8")` plus `json.loads()` to parse JSON.
- It uses query-string encoding, timeouts, a user-agent, and explicit handling for HTTP/network/JSON errors.
- Current weather comes from Open-Meteo's public APIs; internet access is required for menu option 9.

### Using Databases with Python
- `database.py` uses SQLite, `sqlite3.Row`, context managers, parameterized `?` placeholders, `INSERT`, `SELECT`, and a relational foreign key between plots and observations.
- Weather observations are persisted in a separate table.

### Capstone: Retrieving, Processing, and Visualizing Data with Python
- `pipeline.py` reads CSV input, validates required fields/dates/numeric ranges, normalizes values, and imports valid records into SQLite while skipping repeat imports.
- `analytics.py` summarizes stored observations and exports CSV.
- `visualization.py` creates PNG charts with Matplotlib.
- Run the pipeline using menu option 11; generate charts using option 6.

## Notes and limitations
- The bundled crop observations are fictional demonstration data.
- Weather data is retrieved live when option 9 is selected; no weather data is fabricated if the service is unavailable.
- Weather is contextual information only. This project does not make agronomic recommendations or predict crop yield.
