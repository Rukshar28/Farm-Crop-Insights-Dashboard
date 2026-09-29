"""SQLite persistence layer. Connections are closed predictably with a context manager."""

import sqlite3
from pathlib import Path
from models import FarmPlot, CropObservation

DB_PATH = Path(__file__).parent / "data" / "farm_insights.db"


class FarmDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS plots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    crop_type TEXT NOT NULL,
                    area_hectares REAL NOT NULL CHECK(area_hectares > 0)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plot_id INTEGER NOT NULL,
                    observation_date TEXT NOT NULL,
                    rainfall_mm REAL NOT NULL CHECK(rainfall_mm >= 0),
                    yield_kg REAL NOT NULL CHECK(yield_kg >= 0),
                    note TEXT DEFAULT '',
                    FOREIGN KEY(plot_id) REFERENCES plots(id) ON DELETE CASCADE
                )
            """)

    def count_plots(self):
        with self.connect() as conn:
            return conn.execute("SELECT COUNT(*) FROM plots").fetchone()[0]

    def add_plot(self, plot: FarmPlot):
        with self.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO plots(name, location, crop_type, area_hectares) VALUES (?, ?, ?, ?)",
                (plot.name, plot.location, plot.crop_type, plot.area_hectares)
            )
            return cursor.lastrowid

    def list_plots(self):
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM plots ORDER BY id").fetchall()
        return [FarmPlot(row["name"], row["location"], row["crop_type"],
                         row["area_hectares"], row["id"]) for row in rows]

    def add_observation(self, observation: CropObservation):
        with self.connect() as conn:
            cursor = conn.execute("""
                INSERT INTO observations(plot_id, observation_date, rainfall_mm, yield_kg, note)
                VALUES (?, ?, ?, ?, ?)
            """, (observation.plot_id, observation.observation_date, observation.rainfall_mm,
                  observation.yield_kg, observation.note))
            return cursor.lastrowid

    def list_observations(self):
        with self.connect() as conn:
            rows = conn.execute("""
                SELECT o.*, p.name AS plot_name, p.crop_type
                FROM observations o JOIN plots p ON p.id = o.plot_id
                ORDER BY o.observation_date, o.id
            """).fetchall()
        return [dict(row) for row in rows]

    def analytics_rows(self):
        with self.connect() as conn:
            return [dict(row) for row in conn.execute("""
                SELECT p.id AS plot_id, p.name AS plot_name, p.crop_type,
                       p.area_hectares, o.observation_date, o.rainfall_mm, o.yield_kg
                FROM observations o JOIN plots p ON p.id = o.plot_id
                ORDER BY o.observation_date
            """).fetchall()]
