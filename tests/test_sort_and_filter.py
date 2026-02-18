import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


@pytest.mark.regression
@pytest.mark.parametrize(
    "mode, expected_first",
    [
        ("az", "Sauce Labs Backpack"),
        ("za", "Test.allTheThings() T-Shirt (Red)"),
        ("lohi", "Sauce Labs Onesie"),
        ("hilo", "Sauce Labs Fleece Jacket"),
    ],
)
def test_inventory_sorting(driver, base_url, test_data, mode, expected_first):
    LoginPage(driver, base_url).open_login().login(
        test_data["valid"]["username"], test_data["valid"]["password"]
    )
    inv = InventoryPage(driver, base_url)
    inv.sort(mode)
    assert inv.item_names()[0] == expected_first
