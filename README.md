Selenium + pytest test framework

Overview
- Simple Selenium test framework using pytest. Tests live under `Test-Se/tests/` and are grouped by feature (e.g. `duckduckgo_tests`, `secretsauce_tests`).

Prerequisites
- Python 3.8+ and a virtual environment in `Test-Se/.venv` .
- Google Chrome installed and chromedriver accessible on PATH.

Setup
1. Activate the venv:

```powershell
& .\Test-Se\.venv\Scripts\Activate.ps1
```

2. Install dev requirements:

```powershell
pip install -r Test-Se/requirements-dev.txt
```

Running tests
- Run all tests configured in the project:

```powershell
pytest -q
```

- Run tests in a specific folder (example - DuckDuckGo tests):

```powershell
pytest Test-Se/tests/duckduckgo_tests -q
```

Generate HTML report
- Use `pytest-html` to produce an HTML report:

```powershell
pytest Test-Se/tests/duckduckgo_tests --html=duckduckgo_test_report.html -q
```

Screenshots and artifacts
- Tests save screenshots under `Test-Se/tests/<suite>/test_screenshots/` depending on the test.


