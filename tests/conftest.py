import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.config import config


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default="chrome", help="chrome|firefox|edge")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")
    parser.addoption("--base-url", action="store", default=config.base_url, help="Target website URL")


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    raw_base_url = str(request.config.getoption("--base-url")).strip()
    if raw_base_url.startswith(("http://", "https://")):
        return raw_base_url.rstrip("/") + "/"
    return raw_base_url


@pytest.fixture
def driver(request: pytest.FixtureRequest):
    browser = str(request.config.getoption("--browser")).lower()
    headless = bool(request.config.getoption("--headless"))

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        chrome_binary_path = os.getenv("CHROME_BINARY_PATH") or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
        if chrome_binary_path:
            options.binary_location = chrome_binary_path
        if headless:
            options.add_argument("--headless=new")
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH") or shutil.which("chromedriver")
        if chromedriver_path:
            chrome_service = ChromeService(executable_path=chromedriver_path)
            driver_instance = webdriver.Chrome(service=chrome_service, options=options)
        else:
            driver_instance = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if headless:
            options.add_argument("-headless")
        driver_instance = webdriver.Firefox(options=options)
    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("--window-size=1920,1080")
        if headless:
            options.add_argument("--headless=new")
        driver_instance = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver_instance.implicitly_wait(3)
    yield driver_instance
    driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    web_driver = item.funcargs.get("driver")
    if not web_driver:
        return

    screenshot_dir = Path("reports/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    safe_test_name = report.nodeid.replace("::", "_").replace("/", "_")
    screenshot_path = screenshot_dir / f"{safe_test_name}_{timestamp}.png"

    web_driver.save_screenshot(str(screenshot_path))

    allure.attach.file(str(screenshot_path), name="failure_screenshot", attachment_type=allure.attachment_type.PNG)

    pytest_html = item.config.pluginmanager.getplugin("html")
    extras = getattr(report, "extras", [])
    if pytest_html:
        extras.append(pytest_html.extras.png(screenshot_path.read_bytes()))
    report.extras = extras

    if not os.getenv("CI"):
        print(f"Failure screenshot saved: {screenshot_path}")
