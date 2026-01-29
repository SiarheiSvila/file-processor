import os
import json
from result_logger import _safe_stem, _attributes_to_rows, _csv_escape, _meta_by_id

def test_safe_stem():
    assert _safe_stem("My File.pdf") == "My_File"
    assert _safe_stem("test@#$.pdf") == "test"
    assert _safe_stem("---") == "upload"
    assert _safe_stem("path/to/file.json") == "file"

def test_attributes_to_rows():
    extracted = [{"id": 1, "value": "A"}, {"id": 2, "value": "B", "extra": "ignored"}]
    expected = [{"id": 1, "value": "A"}, {"id": 2, "value": "B"}]
    assert _attributes_to_rows(extracted) == expected

def test_attributes_to_rows_invalid():
    assert _attributes_to_rows(None) == []
    assert _attributes_to_rows("not a list") == []
    assert _attributes_to_rows([1, 2, 3]) == []

def test_csv_escape():
    assert _csv_escape('normal') == '"normal"'
    assert _csv_escape('with "quote"') == '"with ""quote"""'
    assert _csv_escape(None) == '""'
    assert _csv_escape(123) == '"123"'

def test_meta_by_id():
    meta = _meta_by_id()
    assert isinstance(meta, dict)
    # Check one known ID from const.py
    # [1630, 'Medical', 'Plan', 'Variable Coinsurance Applies', 'INN-OON']
    assert meta['1630'] == {
        "attr_type": "Medical",
        "category_name": "Plan",
        "name": "Variable Coinsurance Applies",
        "tier_desc": "INN-OON",
    }

from result_logger import save_result_files
from unittest.mock import patch, mock_open

def test_save_result_files():
    with patch("os.makedirs"), \
         patch("builtins.open", mock_open()) as m_open, \
         patch("result_logger.datetime") as m_datetime:

        m_datetime.now.return_value.strftime.return_value = "20231027_120000Z"
        m_datetime.now.return_value.isoformat.return_value = "2023-10-27T12:00:00Z"

        extracted = [{"id": 1630, "value": "Yes"}]
        result = save_result_files(
            uploaded_filename="test.pdf",
            prompt_text="test prompt",
            temperature=0.3,
            extracted_attributes=extracted
        )

        assert "test_20231027_120000Z.json" in result["metadata_json"]
        assert "test_20231027_120000Z.csv" in result["attributes_csv"]

        # Check if files were opened
        assert m_open.call_count == 2
