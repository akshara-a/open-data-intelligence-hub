
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from audit_logs.audit_logger import log_transaction


class TestAuditLogger(unittest.TestCase):

    def test_audit_record_saved(self):

        result = {
            "asset_data": {
                "asset_name": "Laptop",
                "jurisdiction": "India"
            },
            "calculation": {
                "rule_id": "IND_TEST_01",
                "status": "calculated"
            },
            "requires_review": False
        }

        with tempfile.TemporaryDirectory() as temp_dir:

            audit_file = Path(temp_dir) / "audit_log.json"

            with patch("audit_logs.audit_logger.AUDIT_FILE", audit_file):

                record = log_transaction(result)

                self.assertTrue(audit_file.exists())

                with open(audit_file, "r", encoding="utf-8") as file:
                    saved_data = json.load(file)

                self.assertEqual(len(saved_data), 1)
                self.assertEqual(saved_data[0]["asset_name"], "Laptop")
                self.assertEqual(record["jurisdiction"], "India")

    def test_multiple_records_append(self):

        result = {
            "asset_data": {
                "asset_name": "Server",
                "jurisdiction": "India"
            },
            "calculation": {
                "rule_id": "IND_TEST_02",
                "status": "calculated"
            },
            "requires_review": False
        }

        with tempfile.TemporaryDirectory() as temp_dir:

            audit_file = Path(temp_dir) / "audit_log.json"

            with patch("audit_logs.audit_logger.AUDIT_FILE", audit_file):

                log_transaction(result)
                log_transaction(result)

                with open(audit_file, "r", encoding="utf-8") as file:
                    saved_data = json.load(file)

                self.assertEqual(len(saved_data), 2)


if __name__ == "__main__":
    unittest.main()
