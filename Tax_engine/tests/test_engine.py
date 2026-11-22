from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError
from zipfile import ZipFile

from agents.ingestion import (
    AssetInput,
    IngestionError,
    read_csv,
    read_email,
    read_xlsx,
    reconcile,
)
from agents.reasoning import calculate_assets
from agents.supervisor import run
from llm.router import Generation, LLMRouter, RouterError
from tax_lib.depreciation import MACRS_TABLES, calculate_macrs_gds


class IngestionTests(unittest.TestCase):
    def test_reads_csv_aliases_and_email_and_reconciles(self) -> None:
        data_dir = Path(__file__).resolve().parents[1] / "data"
        row = read_csv(data_dir / "attachments" / "sample_assets.csv")[0]
        email = read_email(data_dir / "emails" / "demo_asset.txt")[0]
        asset = reconcile([row, email])[0]

        self.assertEqual(asset.asset_id, "DEMO-001")
        self.assertEqual(asset.cost, Decimal("1250.00"))
        self.assertEqual(asset.placed_in_service_date, "2025-01-15")
        self.assertEqual(set(asset.sources), {"sample_assets.csv:2", "demo_asset.txt"})

    def test_rejects_conflicting_reconciled_values(self) -> None:
        first = AssetInput("A-1", cost=Decimal("100"), sources=("email.txt",))
        second = AssetInput("A-1", cost=Decimal("101"), sources=("assets.csv:2",))

        with self.assertRaisesRegex(IngestionError, "conflicting cost"):
            reconcile([first, second])

    def test_rejects_business_use_outside_percentage_range(self) -> None:
        with self.assertRaisesRegex(IngestionError, "between 0 and 100"):
            reconcile([
                AssetInput(
                    "A-1",
                    cost=Decimal("100"),
                    business_use_pct=Decimal("101"),
                )
            ])

    def test_rejects_conflicting_alias_columns_in_one_csv_row(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "assets.csv"
            path.write_text(
                "Asset ID,Cost,Purchase Price,Business Use %,Residual Value,"
                "Depreciation Method,Recovery Period Years\n"
                "A-1,100,101,100%,0,straight_line,5\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(IngestionError, "conflicting values for cost"):
                read_csv(path)

    def test_reads_xlsx_shared_strings_percent_and_date_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "assets.xlsx"
            serial = (date(2025, 1, 15) - date(1899, 12, 30)).days
            with ZipFile(path, "w") as workbook:
                workbook.writestr(
                    "xl/workbook.xml",
                    '<workbook xmlns="http://schemas.openxmlformats.org/'
                    'spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/'
                    'officeDocument/2006/relationships"><sheets><sheet name="Assets" '
                    'sheetId="1" r:id="rId1"/></sheets></workbook>',
                )
                workbook.writestr(
                    "xl/_rels/workbook.xml.rels",
                    '<Relationships xmlns="http://schemas.openxmlformats.org/'
                    'package/2006/relationships"><Relationship Id="rId1" '
                    'Target="worksheets/sheet1.xml" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/'
                    '2006/relationships/worksheet"/></Relationships>',
                )
                workbook.writestr(
                    "xl/sharedStrings.xml",
                    '<sst xmlns="http://schemas.openxmlformats.org/'
                    'spreadsheetml/2006/main">'
                    + "".join(
                        f"<si><t>{header}</t></si>"
                        for header in (
                            "Asset ID", "Cost", "Business Use %",
                            "Depreciation Method", "Recovery Period Years",
                            "Special Depreciation %", "Placed in Service Date",
                            "XLSX-1", "macrs_gds_200_db_half_year",
                        )
                    )
                    + "</sst>",
                )
                workbook.writestr(
                    "xl/styles.xml",
                    '<styleSheet xmlns="http://schemas.openxmlformats.org/'
                    'spreadsheetml/2006/main"><cellXfs count="3">'
                    '<xf numFmtId="0"/><xf numFmtId="10"/><xf numFmtId="14"/>'
                    '</cellXfs></styleSheet>',
                )
                workbook.writestr(
                    "xl/worksheets/sheet1.xml",
                    '<worksheet xmlns="http://schemas.openxmlformats.org/'
                    'spreadsheetml/2006/main"><sheetData>'
                    '<row r="1">' + "".join(
                        f'<c r="{column}1" t="s"><v>{index}</v></c>'
                        for index, column in enumerate(("A", "B", "C", "D", "E", "F", "G"))
                    ) + '</row><row r="2">'
                    '<c r="A2" t="s"><v>7</v></c><c r="B2"><v>1000</v></c>'
                    '<c r="C2" s="1"><v>1</v></c><c r="D2" t="s"><v>8</v></c>'
                    '<c r="E2"><v>5</v></c><c r="F2" s="1"><v>0</v></c>'
                    f'<c r="G2" s="2"><v>{serial}</v></c>'
                    '</row></sheetData></worksheet>',
                )
            asset = read_xlsx(path)[0]

        self.assertEqual(asset.asset_id, "XLSX-1")
        self.assertEqual(asset.cost, Decimal("1000"))
        self.assertEqual(asset.business_use_pct, Decimal("100"))
        self.assertEqual(asset.special_depreciation_pct, Decimal("0"))
        self.assertEqual(asset.placed_in_service_date, "2025-01-15")


class CalculationTests(unittest.TestCase):
    def test_macrs_5_year_first_year_uses_table_a1_rate(self) -> None:
        result = calculate_macrs_gds(
            cost=Decimal("1000"),
            business_use_pct=Decimal("80"),
            recovery_period_years=Decimal("5"),
            special_depreciation_pct=Decimal("0"),
            placed_in_service_year=2025,
        )

        self.assertEqual(result["business_depreciable_basis"], Decimal("800"))
        self.assertEqual(result["table_rate_pct"], Decimal("20.00"))
        self.assertEqual(result["annual_depreciation"], Decimal("160.0000"))
        self.assertEqual(sum(calculate_macrs_gds(
            cost=Decimal("100"),
            business_use_pct=Decimal("100"),
            recovery_period_years=Decimal("7"),
            special_depreciation_pct=Decimal("0"),
            placed_in_service_year=2025,
        )["table_rate_pct"] for _ in range(1)), Decimal("14.29"))

    def test_macrs_applies_explicit_special_depreciation_to_remaining_basis(self) -> None:
        result = calculate_macrs_gds(
            cost=Decimal("1000"),
            business_use_pct=Decimal("100"),
            recovery_period_years=Decimal("5"),
            special_depreciation_pct=Decimal("40"),
            placed_in_service_year=2025,
        )

        self.assertEqual(result["special_depreciation_amount"], Decimal("400"))
        self.assertEqual(result["macrs_basis_after_special_depreciation"], Decimal("600"))
        self.assertEqual(result["macrs_depreciation_amount"], Decimal("120.0000"))
        self.assertEqual(result["annual_depreciation"], Decimal("520.0000"))

    def test_rejects_unsupported_tax_year(self) -> None:
        with self.assertRaisesRegex(ValueError, "supports tax year 2025 only"):
            calculate_macrs_gds(
                cost=Decimal("1000"),
                business_use_pct=Decimal("100"),
                recovery_period_years=Decimal("5"),
                special_depreciation_pct=Decimal("0"),
                placed_in_service_year=2026,
                tax_year=2026,
            )

    def test_supported_macrs_schedules_total_100_percent(self) -> None:
        for schedule in MACRS_TABLES.values():
            self.assertEqual(sum(schedule), Decimal("100.00"))

    def test_requires_explicit_depreciation_assumptions(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing depreciation method"):
            calculate_assets([AssetInput("A-1", cost=Decimal("100"))])


class RouterTests(unittest.TestCase):
    def test_cloud_request_uses_configured_bearer_key(self) -> None:
        router = LLMRouter()
        with patch.dict(
            os.environ,
            {
                "TAX_CLOUD_API_KEY": "test-key",
                "TAX_CLOUD_MODEL": "test-model",
            },
        ):
            with patch.object(
                router,
                "_post_json",
                return_value={"choices": [{"message": {"content": "summary"}}]},
            ) as post:
                self.assertEqual(
                    router._cloud_generate("prompt", "https://example.test/v1"),
                    "summary",
                )

        headers = post.call_args.args[2]
        self.assertEqual(headers["Authorization"], "Bearer test-key")

    def test_cloud_failure_routes_to_local(self) -> None:
        with patch.dict(os.environ, {"TAX_CLOUD_BASE_URL": "https://example.invalid/v1"}):
            with patch.object(LLMRouter, "_cloud_generate", side_effect=URLError("offline")):
                with patch.object(LLMRouter, "_local_generate", return_value="local summary"):
                    result = LLMRouter().generate("prompt")

        self.assertEqual(result, Generation(
            "local summary",
            "local",
            "URLError",
        ))

    def test_both_routes_unavailable_raises(self) -> None:
        with patch.dict(os.environ, {"TAX_CLOUD_BASE_URL": "https://example.invalid/v1"}):
            with patch.object(LLMRouter, "_cloud_generate", side_effect=URLError("offline")):
                with patch.object(LLMRouter, "_local_generate", side_effect=URLError("offline")):
                    with self.assertRaises(RouterError):
                        LLMRouter().generate("prompt")


class SupervisorTests(unittest.TestCase):
    def test_writes_export_and_mathematical_audit(self) -> None:
        class FakeRouter:
            def generate(self, prompt: str) -> Generation:
                if not prompt.strip():
                    raise AssertionError("audit narrative prompt should not be empty")
                return Generation("Check source documents against the calculated totals.", "local")

        project_dir = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as output:
            result = run(project_dir / "data", Path(output), router=FakeRouter())
            export = json.loads(result.json_path.read_text(encoding="utf-8"))
            audit = result.audit_path.read_text(encoding="utf-8")

        self.assertEqual(result.asset_count, 101)
        self.assertEqual(len(export["assets"]), 101)
        self.assertEqual(
            len({asset["asset_id"] for asset in export["assets"]}),
            101,
        )
        self.assertEqual(export["assets"][0]["annual_depreciation_estimate"], "250.00")
        self.assertIn("1250.00", audit)
        self.assertIn("250.00", audit)
        self.assertIn("Not a tax filing", audit)
        self.assertIn("Table A-1", audit)

    def test_generation_outage_still_writes_deterministic_audit(self) -> None:
        class OfflineRouter:
            def generate(self, prompt: str) -> Generation:
                if not prompt.strip():
                    raise AssertionError("audit narrative prompt should not be empty")
                raise RouterError("cloud and local unavailable")

        project_dir = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as output:
            result = run(project_dir / "data", Path(output), router=OfflineRouter())
            audit = result.audit_path.read_text(encoding="utf-8")

        self.assertIn("deterministic fallback", audit)
        self.assertIn("250.00", audit)


if __name__ == "__main__":
    unittest.main()
