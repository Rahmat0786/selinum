import os
from datetime import datetime
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.utils.config import config


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default="chrome", help="chrome|firefox|edge")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")
    parser.addoption("--base-url", action="store", default=config.base_url, help="Target website URL")


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--base-url")).rstrip("/") + "/"


@pytest.fixture
def driver(request: pytest.FixtureRequest):
    browser = str(request.config.getoption("--browser")).lower()
    headless = bool(request.config.getoption("--headless"))

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        if headless:
            options.add_argument("--headless=new")
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

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_test_name = report.nodeid.replace("::", "_").replace("/", "_")
    screenshot_path = screenshot_dir / f"{safe_test_name}_{timestamp}.png"

    web_driver.save_screenshot(str(screenshot_path))

    allure.attach.file(str(screenshot_path), name="failure_screenshot", attachment_type=allure.attachment_type.PNG)

    pytest_html = item.config.pluginmanager.getplugin("html")
    extra = getattr(report, "extra", [])
    if pytest_html:
        extra.append(pytest_html.extras.png(str(screenshot_path)))
    report.extra = extra

    if not os.getenv("CI"):
        print(f"Failure screenshot saved: {screenshot_path}")
