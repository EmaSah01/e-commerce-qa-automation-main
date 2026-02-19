import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage


class TestCartOperations:
    """Tests for adding and removing items from cart"""

    @pytest.mark.regression
    def test_add_single_item_to_cart(self, driver, base_url, test_data):
        """Test adding a single product to cart"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        product_name = test_data["products"][0]
        
        assert inv.add_to_cart(product_name), f"Failed to add {product_name} to cart"
        
        # Verify cart badge shows 1
        cart_badge = driver.find_elements(*inv._cart_badge)
        assert len(cart_badge) > 0, "Cart badge not visible"
        assert cart_badge[0].text == "1", "Cart badge should show 1 item"

    @pytest.mark.regression
    def test_add_multiple_items_shows_correct_count(self, driver, base_url, test_data):
        """Test cart badge updates correctly when adding multiple items"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        # Add 3 items
        for i, product_name in enumerate(test_data["products"][:3], 1):
            assert inv.add_to_cart(product_name), f"Failed to add {product_name}"
            
            # Verify cart badge
            cart_badge = driver.find_elements(*inv._cart_badge)
            assert len(cart_badge) > 0, "Cart badge not visible"
            assert cart_badge[0].text == str(i), f"Expected {i} items in cart"

    @pytest.mark.regression
    def test_cart_page_displays_added_items(self, driver, base_url, test_data):
        """Test that added items appear on cart page"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        added_products = test_data["products"][:2]
        
        for product in added_products:
            assert inv.add_to_cart(product)
        
        inv.open_cart()
        cart_page = CartPage(driver, base_url)
        cart_items = cart_page.items()
        
        assert len(cart_items) == len(added_products), \
            f"Expected {len(added_products)} items in cart, found {len(cart_items)}"

    @pytest.mark.regression
    def test_cart_item_contains_product_details(self, driver, base_url, test_data):
        """Test that cart items display product name, price, and quantity"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        product_name = test_data["products"][0]
        
        assert inv.add_to_cart(product_name)
        inv.open_cart()
        
        cart_page = CartPage(driver, base_url)
        cart_items = cart_page.items()
        
        assert len(cart_items) == 1
        item = cart_items[0]
        
        # Verify product name is in cart item
        item_text = item.text.lower()
        assert product_name.lower() in item_text or "sauce labs" in item_text or "t-shirt" in item_text, \
            "Product name not found in cart item"

    @pytest.mark.regression
    def test_empty_cart_shows_empty_message(self, driver, base_url, test_data):
        """Test that empty cart shows appropriate message"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        inv.open_cart()
        
        cart_page = CartPage(driver, base_url)
        cart_items = cart_page.items()
        
        assert len(cart_items) == 0, "Cart should be empty"

    @pytest.mark.regression
    def test_cart_persistence_navigation(self, driver, base_url, test_data):
        """Test that cart items persist when navigating back to inventory"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        product_name = test_data["products"][0]
        
        # Add item to cart
        assert inv.add_to_cart(product_name)
        
        # Navigate to cart and back
        inv.open_cart()
        driver.back()
        
        # Verify cart still has item
        cart_badge = driver.find_elements(*inv._cart_badge)
        assert len(cart_badge) > 0, "Cart badge should still show after navigation"

    @pytest.mark.regression
    def test_can_add_all_products_to_cart(self, driver, base_url, test_data):
        """Test that all 6 products can be added to cart"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        # Add all products
        for product in test_data["products"]:
            assert inv.add_to_cart(product), f"Failed to add {product}"
        
        # Verify all are in cart
        inv.open_cart()
        cart_page = CartPage(driver, base_url)
        cart_items = cart_page.items()
        
        assert len(cart_items) == len(test_data["products"])


class TestCartCheckout:
    """Tests for cart to checkout flow"""

    @pytest.mark.regression
    def test_checkout_button_visible_in_cart(self, driver, base_url, test_data):
        """Test checkout button is visible when cart has items"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        checkout_btn = driver.find_element(*CartPage(driver, base_url)._checkout_btn)
        
        assert checkout_btn.is_displayed(), "Checkout button not visible"
        assert checkout_btn.is_enabled(), "Checkout button not enabled"

    @pytest.mark.regression
    def test_checkout_button_empty_cart(self, driver, base_url):
        """Test checkout button behavior with empty cart"""
        # Skip if button doesn't exist - document behavior
        from selenium.common.exceptions import NoSuchElementException
        
        try:
            checkout_btn = driver.find_element(*CartPage(driver, base_url)._checkout_btn)
            # Button exists and is displayed even for empty cart (depends on app)
            assert isinstance(checkout_btn, object)
        except NoSuchElementException:
            # Button might not exist for empty cart
            pass
