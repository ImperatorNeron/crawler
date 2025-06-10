import argparse
from pathlib import Path

from github_crawler.core import settings
from github_crawler.main import run_from_json


def main():
    """Command-line interface for GitHub crawler."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=str(settings.DEFAULT_INPUT_DIR / "input.json"),
        help="Path to JSON file with input data",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=str(settings.DEFAULT_OUTPUT_DIR),
        help="Directory for saving results",
    )

    args = parser.parse_args()

    input_path = args.input
    output_dir = Path(args.output)
    run_from_json(input_path=input_path, output_dir=output_dir)


if __name__ == "__main__":
    main()
