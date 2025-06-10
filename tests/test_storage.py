from datetime import datetime
import json
from unittest.mock import patch
import pytest
from github_crawler.crawler.storage import (
    load_input_data,
    sanitize_filename,
    save_output,
)


def test_load_input_data_valid_json_returns_data(tmp_input_file):
    data = {"key": "value"}
    file_path = tmp_input_file(json.dumps(data))
    assert load_input_data(file_path) == data


def test_load_input_data_file_not_found_raises_error():
    with pytest.raises(FileNotFoundError):
        load_input_data("non_existent_file.json")


def test_load_input_data_invalid_json_raises_error(tmp_input_file):
    file_path = tmp_input_file("{invalid_json")
    with pytest.raises(json.JSONDecodeError):
        load_input_data(file_path)


@pytest.mark.parametrize(
    "input_name, expected",
    [
        ("output_normal", "output_normal"),
        ("file<name>.json", "file_name_.json"),
        ("path/:*?\\|file.json", "path______file.json"),
    ],
)
def test_sanitize_filename_special_chars_replaced(input_name, expected):
    assert sanitize_filename(input_name) == expected


def test_save_output_directory_missing_creates_directory(tmp_path):
    output_dir = tmp_path / "tmp_dir"
    results = [{"url": "https://github.com/farnodes/DevOps-Internship/issues/25"}]
    save_output(["cisco"], "Issues", results, output_dir)
    assert output_dir.exists()


def test_save_output_special_chars_filename_sanitized(tmp_path):
    output_path = save_output(["<cool", "not:>so"], "Issues", [], tmp_path)
    assert "_cool_not__so" in output_path.name


def test_save_output_valid_data_saves_correctly(tmp_path):
    results = [{"url": "https://github.com/farnodes/DevOps-Internship/issues/25"}]
    output_path = save_output(["cisco"], "Issues", results, tmp_path)

    with output_path.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == results


@patch("github_crawler.crawler.storage.datetime")
def test_save_output_keywords_type_timestamp_filename_correct(mock_dt, tmp_path):
    mock_dt.now.return_value = datetime(2025, 6, 9, 10, 20, 30)
    output_path = save_output(["key1", "key2"], "Issues", [], tmp_path)
    assert output_path.name == "output_2025-06-09_10-20-30_key1_key2_Issues.json"
