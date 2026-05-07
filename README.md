# Selenium UI Automation Framework

Production-style Selenium + Pytest QA automation framework for web UI testing.

## Included QA Industry Practices

- Page Object Model (POM) structure
- Reusable Pytest fixtures and CLI options
- Cross-browser support (Chrome, Firefox, Edge)
- Headless execution for CI
- HTML test reporting (`pytest-html`)
- Allure raw results generation (`allure-pytest`)
- Automatic screenshot capture on test failure
- Smoke / regression / negative test markers
- Retry support for flaky test stabilization (`pytest-rerunfailures`)
- Parallel execution capability (`pytest-xdist`)
- GitHub Actions CI with report artifact publishing

## Tech Stack

- Python 3.12+
- Selenium 4
- Pytest
- Pytest HTML Reporter
- Allure Pytest

## Reference Website Under Test

- Default: Local demo website (`sample_site/index.html`) for fully offline execution
- Optional: Any public URL via `--base-url` or `BASE_URL` environment variable

## Project Structure

```text
selinum/
├── .github/workflows/ui-tests.yml
├── sample_site/
│   ├── index.html
│   └── inventory.html
├── src/
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   └── inventory_page.py
│   └── utils/config.py
├── tests/
│   ├── conftest.py
│   └── test_login.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run Tests

### Local headed run (Chrome)

```bash
pytest --browser=chrome
```

### Run against any external website URL

```bash
pytest --browser=chrome --headless --base-url=https://example.com/
```

### Headless run (CI-like)

```bash
pytest --browser=chrome --headless
```

### Run smoke suite only

```bash
pytest -m smoke --browser=chrome --headless
```

### Parallel execution

```bash
pytest -n auto --browser=chrome --headless
```

## Reports

### Pytest HTML Report

Generated automatically at:

- `reports/pytest_report.html`

### Allure Raw Results

Generate raw files:

```bash
pytest --alluredir=allure-results --browser=chrome --headless
```

(Optional) If Allure CLI is installed:

```bash
allure serve allure-results
```

## CI

GitHub Actions workflow:

- Executes UI tests on push / PR
- Uploads HTML report, screenshots, and Allure raw results as artifacts
