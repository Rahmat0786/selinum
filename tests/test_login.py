import pytest

from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage
from src.utils.config import config


@pytest.mark.ui
@pytest.mark.smoke
def test_successful_login(driver, base_url):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.open(base_url)
    login_page.login(config.valid_user, config.valid_password)

    assert inventory_page.get_title() == "Products"


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.negative
def test_locked_out_user_cannot_login(driver, base_url):
    login_page = LoginPage(driver)

    login_page.open(base_url)
    login_page.login(config.locked_user, config.locked_password)

    assert "locked out" in login_page.get_error_message().lower()
