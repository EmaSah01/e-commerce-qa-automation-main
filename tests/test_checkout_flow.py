import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_info_page import CheckoutInfoPage
from src.pages.checkout_overview_page import CheckoutOverviewPage
from src.pages.checkout_complete_page import CheckoutCompletePage


@pytest.mark.regression
def test_full_checkout_flow(driver, base_url, test_data):
    LoginPage(driver, base_url).open_login().login(
        test_data["valid"]["username"], test_data["valid"]["password"]
    )
    inv = InventoryPage(driver, base_url)
    for name in test_data["products"][:2]:
        assert inv.add_to_cart(name)
    inv.open_cart()
    CartPage(driver, base_url).checkout()
    info = test_data["checkout_info"]
    CheckoutInfoPage(driver, base_url).fill(info["first"], info["last"], info["zip"])
    CheckoutOverviewPage(driver, base_url).finish()
    complete = CheckoutCompletePage(driver, base_url)
    assert "Thank you for your order" in complete.success_text()


@pytest.mark.regression
def test_checkout_with_multiple_items(driver, base_url, test_data):
    """Test ordering multiple items at the same time"""
    LoginPage(driver, base_url).open_login().login(
        test_data["valid"]["username"], test_data["valid"]["password"]
    )
    inv = InventoryPage(driver, base_url)
    # Add all available products to cart
    for product_name in test_data["products"]:
        assert inv.add_to_cart(product_name), f"Failed to add {product_name} to cart"
    inv.open_cart()
    
    # Verify all items are in cart
    cart = CartPage(driver, base_url)
    cart_items = cart.items()
    assert len(cart_items) == len(test_data["products"]), \
        f"Expected {len(test_data['products'])} items in cart, found {len(cart_items)}"
    
    # Proceed to checkout
    cart.checkout()
    info = test_data["checkout_info"]
    CheckoutInfoPage(driver, base_url).fill(info["first"], info["last"], info["zip"])
    CheckoutOverviewPage(driver, base_url).finish()
    
    # Verify order completed
    complete = CheckoutCompletePage(driver, base_url)
    assert "Thank you for your order" in complete.success_text()
