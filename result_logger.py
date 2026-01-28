import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from const import SOURCE_DATAFRAME


def _safe_stem(name: str) -> str:
    # Keep filenames stable and OS-friendly
    stem = os.path.splitext(os.path.basename(name))[0]
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in stem).strip("_")
    return safe or "upload"


def _default_result_paths(uploaded_filename: str) -> Tuple[str, str]:
    # Filename-friendly UTC timestamp
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    stem = _safe_stem(uploaded_filename)
    base = os.path.join("logs", f"{stem}_{ts}")
    return f"{base}.json", f"{base}.csv"


def _attributes_to_rows(extracted_attributes: Optional[Any]) -> List[Dict[str, Any]]:
    if not extracted_attributes or not isinstance(extracted_attributes, list):
        return []
    rows: List[Dict[str, Any]] = []
    for item in extracted_attributes:
        if isinstance(item, dict):
            rows.append(
                {
                    "id": item.get("id"),
                    "value": item.get("value"),
                }
            )
    return rows


def _meta_by_id() -> Dict[str, Dict[str, str]]:
    """
    Build a lookup from attribute id -> metadata fields, based on SOURCE_DATAFRAME:
    [id, attr_type, category_name, name, tier_desc]
    """
    meta: Dict[str, Dict[str, str]] = {}
    for row in SOURCE_DATAFRAME:
        if not row or len(row) < 5:
            continue
        attr_id = row[0]
        meta[str(attr_id)] = {
            "attr_type": str(row[1]) if row[1] is not None else "",
            "category_name": str(row[2]) if row[2] is not None else "",
            "name": str(row[3]) if row[3] is not None else "",
            "tier_desc": str(row[4]) if row[4] is not None else "",
        }
    return meta


def _csv_escape(value: Any) -> str:
    s = "" if value is None else str(value)
    s = s.replace('"', '""')
    return f'"{s}"'


def save_result_files(
    *,
    uploaded_filename: str,
    prompt_text: str,
    temperature: float,
    extracted_attributes: Optional[Any],
) -> Dict[str, str]:
    """
    Save one run as two files:
    - metadata JSON file (prompt, temperature, etc.)
    - extracted attributes CSV file (id,value)

    Returns absolute paths: {"metadata_json": "...", "attributes_csv": "..."}
    """
    metadata_path, csv_path = _default_result_paths(uploaded_filename)
    os.makedirs(os.path.dirname(metadata_path) or ".", exist_ok=True)

    rows = _attributes_to_rows(extracted_attributes)
    meta = _meta_by_id()

    # Write CSV (simple, no external deps)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        f.write("id,attr_type,category_name,name,tier_desc,value\n")
        for r in rows:
            id_str = "" if r.get("id") is None else str(r.get("id"))
            m = meta.get(id_str, {})
            f.write(
                ",".join(
                    [
                        id_str,
                        _csv_escape(m.get("attr_type", "")),
                        _csv_escape(m.get("category_name", "")),
                        _csv_escape(m.get("name", "")),
                        _csv_escape(m.get("tier_desc", "")),
                        _csv_escape(r.get("value")),
                    ]
                )
                + "\n"
            )

    metadata = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uploaded_filename": uploaded_filename,
        "temperature": temperature,
        "prompt": prompt_text,
        "extracted_attributes_count": len(rows),
        "attributes_csv": os.path.abspath(csv_path),
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return {
        "metadata_json": os.path.abspath(metadata_path),
        "attributes_csv": os.path.abspath(csv_path),
    }

