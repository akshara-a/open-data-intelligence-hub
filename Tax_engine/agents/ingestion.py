"""Read and normalize asset data from client emails and CSV attachments."""

from __future__ import annotations

import csv
import posixpath
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile


class IngestionError(ValueError):
    """Raised when an input file cannot be interpreted safely."""


@dataclass(frozen=True)
class AssetInput:
    asset_id: str
    description: str | None = None
    cost: Decimal | None = None
    business_use_pct: Decimal | None = None
    placed_in_service_date: str | None = None
    region: str | None = None
    method: str | None = None
    recovery_period_years: Decimal | None = None
    residual_value: Decimal | None = None
    special_depreciation_pct: Decimal | None = None
    sources: tuple[str, ...] = ()


_ALIASES = {
    "asset_id": {"assetid", "assetnumber", "assetno", "id", "propertyid"},
    "description": {"description", "assetdescription", "property", "assetname"},
    "cost": {
        "cost", "costbasis", "basis", "purchaseprice", "acquisitioncost",
        "amount", "originalcost",
    },
    "business_use_pct": {
        "businessuse", "businessusepct", "businessusepercent",
        "businesspercentage", "businessusepercentage",
    },
    "placed_in_service_date": {
        "placedinservicedate", "inservicedate", "dateplacedinservice",
        "acquisitiondate", "purchasedate",
    },
    "region": {"region", "jurisdiction", "taxregion", "state", "country"},
    "method": {"method", "depreciationmethod"},
    "recovery_period_years": {
        "recoveryperiod", "recoveryperiodyears", "usefullife", "usefullifeyears",
        "lifeyears",
    },
    "residual_value": {"residualvalue", "salvagevalue", "scrapvalue"},
    "special_depreciation_pct": {
        "specialdepreciation", "specialdepreciationpct",
        "specialdepreciationpercent", "bonusdepreciationpct",
        "bonusdepreciationpercent",
    },
}
_HEADER_TO_FIELD = {
    alias: field for field, aliases in _ALIASES.items() for alias in aliases
}


def _header_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _decimal(value: str, field: str, source: str) -> Decimal:
    cleaned = value.strip().replace(",", "").replace("$", "").replace("€", "").replace("£", "")
    is_percent = cleaned.endswith("%")
    if is_percent:
        cleaned = cleaned[:-1].strip()
    try:
        parsed = Decimal(cleaned)
    except InvalidOperation as exc:
        raise IngestionError(f"{source}: invalid {field} value {value!r}") from exc
    if not parsed.is_finite():
        raise IngestionError(f"{source}: {field} must be a finite number")
    if field == "business_use_pct" and is_percent:
        return parsed
    return parsed


def _date(value: str, source: str) -> str:
    value = value.strip()
    for pattern in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(value, pattern).date().isoformat()
        except ValueError:
            pass
    raise IngestionError(
        f"{source}: unsupported placed-in-service date {value!r}; "
        "use YYYY-MM-DD or MM/DD/YYYY"
    )


def _normalize_values(values: dict[str, str], source: str) -> AssetInput:
    normalized: dict[str, object] = {}
    for raw_key, raw_value in values.items():
        field = _HEADER_TO_FIELD.get(_header_key(raw_key))
        value = raw_value.strip()
        if field is None or not value:
            continue
        if field in {
            "cost", "business_use_pct", "recovery_period_years",
            "residual_value", "special_depreciation_pct",
        }:
            parsed_value: object = _decimal(value, field, source)
        elif field == "placed_in_service_date":
            parsed_value = _date(value, source)
        elif field == "method":
            parsed_value = value.lower().replace("-", "_").replace(" ", "_")
        else:
            parsed_value = value
        if field in normalized and normalized[field] != parsed_value:
            raise IngestionError(
                f"{source}: conflicting values for {field} in the same record"
            )
        normalized[field] = parsed_value

    asset_id = normalized.get("asset_id")
    if not isinstance(asset_id, str) or not asset_id:
        raise IngestionError(f"{source}: each record must include an asset ID")
    return AssetInput(asset_id=asset_id, sources=(source,), **{
        key: value for key, value in normalized.items() if key != "asset_id"
    })


def read_csv(path: Path) -> list[AssetInput]:
    """Read records from a CSV file with flexible, recognized column names."""
    records: list[AssetInput] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                raise IngestionError(f"{path}: CSV file has no header row")
            for line_number, row in enumerate(reader, start=2):
                if not any(value and value.strip() for value in row.values() if value):
                    continue
                values = {key: value or "" for key, value in row.items() if key}
                records.append(_normalize_values(values, f"{path.name}:{line_number}"))
    except OSError as exc:
        raise IngestionError(f"cannot read {path}: {exc}") from exc
    except csv.Error as exc:
        raise IngestionError(f"invalid CSV in {path}: {exc}") from exc
    return records


def _column_index(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference)
    if not letters:
        raise IngestionError(f"invalid spreadsheet cell reference {reference!r}")
    index = 0
    for letter in letters.group():
        index = index * 26 + ord(letter) - ord("A") + 1
    return index - 1


def _xlsx_text(zip_file: ZipFile, name: str) -> ElementTree.Element:
    try:
        return ElementTree.fromstring(zip_file.read(name))
    except (KeyError, ElementTree.ParseError) as exc:
        raise IngestionError(f"invalid .xlsx workbook structure at {name}") from exc


def read_xlsx(path: Path) -> list[AssetInput]:
    """Read the first worksheet of a standard, unencrypted .xlsx workbook."""
    namespace = {
        "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "package": "http://schemas.openxmlformats.org/package/2006/relationships",
    }
    try:
        with ZipFile(path) as workbook:
            files = workbook.infolist()
            if len(files) > 256 or sum(item.file_size for item in files) > 20_000_000:
                raise IngestionError(f"{path}: workbook exceeds the supported size limits")
            workbook_xml = _xlsx_text(workbook, "xl/workbook.xml")
            first_sheet = workbook_xml.find("main:sheets/main:sheet", namespace)
            if first_sheet is None:
                raise IngestionError(f"{path}: workbook contains no worksheets")
            relationship_id = first_sheet.attrib.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            )
            relationships = _xlsx_text(workbook, "xl/_rels/workbook.xml.rels")
            target = next(
                (
                    rel.attrib["Target"]
                    for rel in relationships.findall("package:Relationship", namespace)
                    if rel.attrib.get("Id") == relationship_id
                ),
                None,
            )
            if target is None:
                raise IngestionError(f"{path}: first worksheet relationship is missing")
            sheet_path = posixpath.normpath(
                target.lstrip("/") if target.startswith("/") else posixpath.join("xl", target)
            )
            if not sheet_path.startswith("xl/") or ".." in sheet_path.split("/"):
                raise IngestionError(f"{path}: invalid worksheet path")

            shared_strings: list[str] = []
            if "xl/sharedStrings.xml" in workbook.namelist():
                root = _xlsx_text(workbook, "xl/sharedStrings.xml")
                shared_strings = [
                    "".join(item.itertext())
                    for item in root.findall("main:si", namespace)
                ]

            style_formats: list[str] = []
            if "xl/styles.xml" in workbook.namelist():
                styles = _xlsx_text(workbook, "xl/styles.xml")
                custom_formats = {
                    int(item.attrib["numFmtId"]): item.attrib.get("formatCode", "")
                    for item in styles.findall("main:numFmts/main:numFmt", namespace)
                }
                cell_formats = styles.find("main:cellXfs", namespace)
                if cell_formats is not None:
                    for item in cell_formats:
                        format_id = int(item.attrib.get("numFmtId", "0"))
                        style_formats.append(
                            custom_formats.get(format_id, f"builtin:{format_id}")
                        )

            date_1904 = (
                workbook_xml.find("main:workbookPr", namespace) is not None
                and workbook_xml.find("main:workbookPr", namespace).attrib.get("date1904")
                in {"1", "true"}
            )
            worksheet = _xlsx_text(workbook, sheet_path)
            rows: list[tuple[int, dict[int, str]]] = []
            for row in worksheet.findall(".//main:sheetData/main:row", namespace):
                row_values: dict[int, str] = {}
                for cell in row.findall("main:c", namespace):
                    reference = cell.attrib.get("r", "")
                    value_node = cell.find("main:v", namespace)
                    cell_type = cell.attrib.get("t")
                    if cell_type == "inlineStr":
                        value = "".join(
                            cell.find("main:is", namespace).itertext()
                        ) if cell.find("main:is", namespace) is not None else ""
                    elif value_node is None:
                        value = ""
                    elif cell_type == "s":
                        try:
                            value = shared_strings[int(value_node.text or "")]
                        except (ValueError, IndexError) as exc:
                            raise IngestionError(
                                f"{path}: invalid shared-string cell {reference}"
                            ) from exc
                    else:
                        value = value_node.text or ""

                    style_index = int(cell.attrib.get("s", "0"))
                    style = (
                        style_formats[style_index]
                        if style_index < len(style_formats)
                        else "builtin:0"
                    )
                    if value:
                        format_id = (
                            int(style.partition(":")[2])
                            if style.startswith("builtin:")
                            else None
                        )
                        date_format_ids = {
                            14, 15, 16, 17, 22, 27, 28, 29, 30, 31, 32,
                            33, 34, 35, 36, 50, 51, 52, 53, 54, 55, 56, 57, 58,
                        }
                        if format_id in date_format_ids:
                            try:
                                serial = Decimal(value)
                                if not serial.is_finite():
                                    raise InvalidOperation
                                days = int(serial)
                                if date_1904:
                                    origin = datetime(1904, 1, 1)
                                elif days < 60:
                                    origin = datetime(1899, 12, 31)
                                elif days == 60:
                                    raise ValueError("Excel serial 60 is not a real date")
                                else:
                                    origin = datetime(1899, 12, 30)
                                value = (origin + timedelta(days=days)).date().isoformat()
                            except (InvalidOperation, OverflowError, ValueError):
                                raise IngestionError(
                                    f"{path}: invalid spreadsheet date in cell {reference}"
                                )
                        elif "%" in style or format_id in {9, 10}:
                            try:
                                value = str(Decimal(value) * Decimal("100")) + "%"
                            except InvalidOperation as exc:
                                raise IngestionError(
                                    f"{path}: invalid percentage in cell {reference}"
                                ) from exc
                    row_values[_column_index(reference)] = value
                if row_values:
                    rows.append((int(row.attrib.get("r", "0")), row_values))
    except OSError as exc:
        raise IngestionError(f"cannot read {path}: {exc}") from exc
    except BadZipFile as exc:
        raise IngestionError(f"{path}: not a valid .xlsx zip package") from exc

    if not rows:
        raise IngestionError(f"{path}: first worksheet is empty")
    _, header_cells = rows[0]
    headers = {
        index: value.strip()
        for index, value in header_cells.items()
        if value.strip()
    }
    if not headers:
        raise IngestionError(f"{path}: first worksheet has no header row")
    records: list[AssetInput] = []
    for line_number, cells in rows[1:]:
        values = {
            header: cells.get(index, "")
            for index, header in headers.items()
            if cells.get(index, "").strip()
        }
        if values:
            records.append(_normalize_values(values, f"{path.name}:{line_number}"))
    return records


def read_email(path: Path) -> list[AssetInput]:
    """Extract labeled key/value fields from a plain-text email."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise IngestionError(f"cannot read {path}: {exc}") from exc

    values: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*([^:=]+?)\s*[:=]\s*(.*?)\s*$", line)
        if match and _header_key(match.group(1)) in _HEADER_TO_FIELD:
            key = match.group(1)
            previous = next(
                (name for name in values if _header_key(name) == _header_key(key)),
                None,
            )
            if previous is not None and values[previous] != match.group(2):
                raise IngestionError(
                    f"{path.name}: conflicting repeated values for {key}"
                )
            values[match.group(1)] = match.group(2)
    if not values:
        raise IngestionError(f"{path}: no recognized labeled asset fields found")
    return [_normalize_values(values, path.name)]


def load_inputs(data_dir: Path) -> list[AssetInput]:
    """Load supported files in stable path order from the input directories."""
    email_dir = data_dir / "emails"
    attachment_dir = data_dir / "attachments"
    records: list[AssetInput] = []
    for path in sorted(email_dir.glob("*.txt")):
        records.extend(read_email(path))
    for path in sorted(attachment_dir.glob("*.csv")):
        records.extend(read_csv(path))
    for path in sorted(attachment_dir.glob("*.xlsx")):
        records.extend(read_xlsx(path))
    return records


def reconcile(records: list[AssetInput]) -> list[AssetInput]:
    """Merge partial records by asset ID, rejecting conflicting field values."""
    merged: dict[str, dict[str, object]] = {}
    fields = (
        "description", "cost", "business_use_pct", "placed_in_service_date",
        "region", "method", "recovery_period_years", "residual_value",
        "special_depreciation_pct",
    )
    for record in records:
        target = merged.setdefault(
            record.asset_id,
            {"asset_id": record.asset_id, "sources": []},
        )
        sources = target["sources"]
        assert isinstance(sources, list)
        sources.extend(record.sources)
        for field in fields:
            value = getattr(record, field)
            if value is None:
                continue
            previous = target.get(field)
            if previous is not None and previous != value:
                raise IngestionError(
                    f"asset {record.asset_id!r} has conflicting {field}: "
                    f"{previous!r} versus {value!r} (source {record.sources[0]})"
                )
            target[field] = value

    results: list[AssetInput] = []
    for asset_id, values in sorted(merged.items()):
        if values.get("cost") is None:
            raise IngestionError(f"asset {asset_id!r} is missing cost")
        business_use = values.get("business_use_pct")
        if not isinstance(business_use, Decimal) or not 0 <= business_use <= 100:
            if business_use is None:
                raise IngestionError(f"asset {asset_id!r} is missing business-use percentage")
            raise IngestionError(
                f"asset {asset_id!r} business use must be between 0 and 100"
            )
        cost = values["cost"]
        residual = values.get("residual_value")
        if not isinstance(cost, Decimal):
            raise IngestionError(f"asset {asset_id!r} cost must be a number")
        if cost < 0:
            raise IngestionError(f"asset {asset_id!r} cost cannot be negative")
        if residual is not None and (
            not isinstance(residual, Decimal) or residual < 0 or residual > cost
        ):
            raise IngestionError(
                f"asset {asset_id!r} residual value must be between zero and cost"
            )
        special_depreciation = values.get("special_depreciation_pct")
        if special_depreciation is None:
            raise IngestionError(
                f"asset {asset_id!r} is missing explicit special-depreciation percentage"
            )
        if not isinstance(special_depreciation, Decimal) or not 0 <= special_depreciation <= 100:
            raise IngestionError(
                f"asset {asset_id!r} special depreciation must be between 0 and 100"
            )
        sources = values["sources"]
        assert isinstance(sources, list)
        results.append(AssetInput(
            asset_id=asset_id,
            description=values.get("description"),
            cost=cost,
            business_use_pct=business_use,
            placed_in_service_date=values.get("placed_in_service_date"),
            region=values.get("region"),
            method=values.get("method"),
            recovery_period_years=values.get("recovery_period_years"),
            residual_value=residual,
            special_depreciation_pct=special_depreciation,
            sources=tuple(sorted(set(sources))),
        ))
    return results
