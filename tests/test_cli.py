import pytest
import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

from github_crawler.core import settings


@pytest.mark.parametrize(
    "cli_args, expected_input, expected_output",
    [
        (
            ["script_name"],
            str(settings.DEFAULT_INPUT_DIR / "input.json"),
            str(settings.DEFAULT_OUTPUT_DIR),
        ),
        (
            [
                "script_name",
                "-i",
                "custom/inputs/input.json",
                "-o",
                "custom/outputs/dir",
            ],
            "custom/inputs/input.json",
            "custom/outputs/dir",
        ),
        (
            [
                "script_name",
                "--input",
                "custom/inputs/input.json",
                "--output",
                "custom/outputs/dir",
            ],
            "custom/inputs/input.json",
            "custom/outputs/dir",
        ),
    ],
)
def test_main_args_variants_run_called_with_expected_paths(
    monkeypatch,
    cli_args,
    expected_input,
    expected_output,
):
    monkeypatch.setattr(sys, "argv", cli_args)
    mock_args = MagicMock()
    mock_args.input = expected_input
    mock_args.output = expected_output

    with (
        patch("argparse.ArgumentParser.parse_args", return_value=mock_args),
        patch("github_crawler.cli.run_from_json") as mock_run,
    ):
        from github_crawler.cli import main

        main()

    mock_run.assert_called_once_with(
        input_path=expected_input, output_dir=Path(expected_output)
    )
