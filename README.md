# GitHub Crawler - Documentation

## Overview
This GitHub data scraping tool automates the collection of URLs for repositories, issues, and wikis from GitHub.

## Prerequisites
- Python 3.12+
- Poetry (dependency manager)

## Installation Guide

1. Clone the repository:
```bash
git clone https://github.com/ImperatorNeron/crawler.git
cd crawler
```

2. Create a venv for isolated poetry installation (choose what works for you):
```bash
python3 -m venv venv
python -m venv venv
py -m venv venv
```

3. Activate a venv (choose what works for you)
```bash
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate         # Windows (CMD)
venv\Scripts\activate.bat     # Windows (CMD)
venv\Scripts\Activate.ps1     # Windows (PowerShell)
``` 

4. Install Poetry (within the virtual environment):
```bash
pip install poetry
```

5. Install dependencies using Poetry:
```bash
poetry install
```

## Configuration

Default input file location `github_crawler/inputs/input.json` (With example, unstanble but free proxies)  
   Example structure(fake proxies):
```json
{
  "keywords": ["python", "web scraping"],
  "type": "Repositories",
  "proxies": ["111.111.111.111:8888", "111.43.23.23:1238"]
}
```

Supported Search Types ("type"):
- `Repositories`
- `Issues`
- `Wikis`

## Usage (Сhoose any option)

### Run with Default Settings
```bash
python -m github_crawler.cli
```
Uses default `github_crawler/inputs/input.json` and saves to `github_crawler/outputs/`

### Specify Output Directory
```bash
python -m github_crawler.cli --output path/to/output
# or short version:
python -m github_crawler.cli -o path/to/output
```

### Specify Custom Input File
```bash
python -m github_crawler.cli --input path/to/input.json
# or short version:
python -m github_crawler.cli -i path/to/input.json

```

### Full customization
```bash
python -m github_crawler.cli --input folder/input.json --output here/new
```

## Testing

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=github_crawler
```

## Proxy Configuration
Edit `github_crawler/inputs/input.json` to add your proxies in format:
```json
"proxies": ["ip:port", "ip:port"]
```

## Output Format
Results are saved in JSON files with structure:
```json
[
  {"url": "https://github.com/user/repo1"},
  {"url": "https://github.com/user/repo2"}
]
```

## Troubleshooting
If encountering errors:
1. Verify internet connection
2. Check proxy functionality
3. Validate input file structure
