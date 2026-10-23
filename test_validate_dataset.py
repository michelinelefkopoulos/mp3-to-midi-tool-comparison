"""Offline tests; fixtures are built in memory and the source CSV is unchanged."""
# SPDX-License-Identifier: CC0-1.0
import csv
import io
from pathlib import Path
import unittest
from validate_dataset import COLUMNS, inspect_csv


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        with Path(__file__).with_name("mp3-to-midi-tool-comparison.csv").open(encoding="utf-8", newline="") as file:
            self.rows = list(csv.DictReader(file, skipinitialspace=True))

    def inspect(self, rows):
        file = io.StringIO()
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
        file.seek(0)
        return inspect_csv(file)

    def test_published_snapshot(self):
        result = self.inspect(self.rows)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["rows"], 11)
        self.assertEqual(result["result_kinds"], {"converter": 10, "discussion": 1})
        self.assertFalse(result["quotes_verified"])

    def test_duplicate_position(self):
        self.rows[1]["google_organic_position"] = self.rows[0]["google_organic_position"]
        self.assertFalse(self.inspect(self.rows)["valid"])

    def test_duplicate_url(self):
        self.rows[1]["page_url"] = self.rows[0]["page_url"]
        self.assertFalse(self.inspect(self.rows)["valid"])

    def test_invalid_url(self):
        self.rows[0]["page_url"] = "javascript:alert(1)"
        self.assertFalse(self.inspect(self.rows)["valid"])

    def test_invalid_date(self):
        self.rows[0]["checked_at"] = "2026-02-30"
        self.assertFalse(self.inspect(self.rows)["valid"])

    def test_unstated_is_not_empty(self):
        self.rows[0]["supported_formats"] = ""
        self.assertFalse(self.inspect(self.rows)["valid"])

    def test_discussion_is_not_a_product_claim(self):
        row = next(row for row in self.rows if row["result_kind"] == "discussion")
        row["supported_formats"] = "MP3"
        self.assertFalse(self.inspect(self.rows)["valid"])

    def test_unicode_comma_and_quote(self):
        self.rows[0]["page_title"] = 'Unicode 音符, quoted "title"'
        self.assertTrue(self.inspect(self.rows)["valid"])

    def test_wrong_header(self):
        self.assertFalse(inspect_csv(io.StringIO("a,b\n1,2\n"))["valid"])


if __name__ == "__main__":
    unittest.main()
