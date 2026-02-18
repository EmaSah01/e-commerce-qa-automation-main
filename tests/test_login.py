import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_login_success(driver, base_url, test_data):
    LoginPage(driver, base_url).open_login().login(
        test_data["valid"]["username"], test_data["valid"]["password"]
    )
    assert InventoryPage(driver, base_url).is_loaded()


@pytest.mark.regression
def test_login_locked_user_shows_error(driver, base_url, test_data):
    page = LoginPage(driver, base_url).open_login().login(
        test_data["locked"]["username"], test_data["locked"]["password"]
    )
    assert "locked out" in page.error_text().lower()
