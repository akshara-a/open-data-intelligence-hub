
import unittest
from pathlib import Path

from supervisor_agent.supervisor import run_supervisor

BASE_DIR = Path(__file__).resolve().parents[1]
EMAIL_FILE = BASE_DIR / "data" / "raw" / "sample_email.txt"


class TestPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not EMAIL_FILE.exists():
            raise FileNotFoundError(
                f"Sample email not found: {EMAIL_FILE}"
            )

        cls.email_text = EMAIL_FILE.read_text(
            encoding="utf-8"
        )

    def test_supervisor_pipeline(self):

        result = run_supervisor(self.email_text)

        self.assertIsInstance(result, dict)

        self.assertIn("asset_data", result)
        self.assertIn("calculation", result)
        self.assertIn("reasoning", result)
        self.assertIn("requires_review", result)

        self.assertIsInstance(result["asset_data"], dict)
        self.assertIsInstance(result["calculation"], dict)
        self.assertIsInstance(result["reasoning"], dict)

        self.assertIsInstance(result["requires_review"], bool)


if __name__ == "__main__":
    unittest.main()
