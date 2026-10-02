import tempfile
import unittest
from pathlib import Path
from database import FarmDatabase
from pipeline import read_observations_csv, import_observations


class PipelineTests(unittest.TestCase):
    def test_reads_and_validates_sample_csv(self):
        sample = Path(__file__).parents[1] / "data" / "sample_observations.csv"
        records, errors = read_observations_csv(sample)
        self.assertEqual(len(records), 6)
        self.assertEqual(errors, [])

    def test_import_is_idempotent(self):
        sample = Path(__file__).parents[1] / "data" / "sample_observations.csv"
        with tempfile.TemporaryDirectory() as folder:
            db = FarmDatabase(Path(folder) / "test.sqlite")
            first = import_observations(sample, db)
            second = import_observations(sample, db)
            self.assertEqual(first["imported"], 6)
            self.assertEqual(second["imported"], 0)
            self.assertEqual(second["duplicates_skipped"], 6)
            self.assertEqual(len(db.analytics_rows()), 6)


if __name__ == "__main__":
    unittest.main()
