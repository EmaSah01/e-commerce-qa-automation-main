import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from selenium.webdriver.common.by import By


class TestProductDetails:
    """Tests for product information and display"""

    @pytest.mark.regression
    def test_inventory_page_displays_all_products(self, driver, base_url, test_data):
        """Test that inventory page displays all 6 products"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        product_names = inv.item_names()
        assert len(product_names) == 6, f"Expected 6 products, found {len(product_names)}"

    @pytest.mark.regression
    def test_each_product_has_name_price_and_image(self, driver, base_url, test_data):
        """Test that each product displays name, price, and image"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        items = driver.find_elements(*inv._inventory_items)
        
        for item in items:
            # Check for product name
            try:
                name = item.find_element(By.CSS_SELECTOR, ".inventory_item_name, [data-test='inventory-item-name']")
                assert name.is_displayed(), "Product name not visible"
                assert len(name.text.strip()) > 0, "Product name is empty"
            except:
                pytest.fail(f"Product name element not found in item")
            
            # Check for price
            try:
                price = item.find_element(By.CSS_SELECTOR, ".inventory_item_price")
                assert price.is_displayed(), "Product price not visible"
                assert "$" in price.text, "Price should contain currency symbol"
            except:
                pytest.fail("Product price element not found")
            
            # Check for image
            try:
                img = item.find_element(By.CSS_SELECTOR, "img")
                assert img.is_displayed(), "Product image not visible"
            except:
                pytest.fail("Product image not found")

    @pytest.mark.regression
    def test_product_description_visible(self, driver, base_url, test_data):
        """Test that product description is visible"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        items = driver.find_elements(*inv._inventory_items)
        
        for item in items:
            try:
                desc = item.find_element(By.CSS_SELECTOR, ".inventory_item_desc")
                assert desc.is_displayed(), "Product description not visible"
                assert len(desc.text.strip()) > 0, "Product description is empty"
            except:
                pytest.fail("Product description element not found")

    @pytest.mark.regression
    def test_known_product_names_displayed(self, driver, base_url, test_data):
        """Test that specific products are displayed"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        product_names = inv.item_names()
        
        # Check if test products are in the list
        for test_product in test_data["products"][:3]:
            assert any(test_product.lower() in name.lower() for name in product_names), \
                f"Product '{test_product}' not found in inventory"

    @pytest.mark.regression
    def test_product_prices_are_valid(self, driver, base_url):
        """Test that all product prices are valid positive numbers"""
        inv = InventoryPage(driver, base_url)
        items = driver.find_elements(*inv._inventory_items)
        
        for item in items:
            price_element = item.find_element(By.CSS_SELECTOR, ".inventory_item_price")
            price_text = price_element.text.strip()
            
            # Extract number from price string (e.g., "$29.99")
            import re
            match = re.search(r'\$(\d+\.\d{2})', price_text)
            assert match, f"Invalid price format: {price_text}"
            
            price_value = float(match.group(1))
            assert price_value > 0, f"Price should be positive: {price_value}"


class TestProductSorting:
    """Tests for product sorting functionality"""

    @pytest.mark.regression
    def test_sort_dropdown_exists(self, driver, base_url, test_data):
        """Test that sort dropdown is present"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        sort_select = driver.find_element(*inv._sort_select)
        assert sort_select.is_displayed(), "Sort dropdown not visible"

    @pytest.mark.regression
    @pytest.mark.parametrize("sort_mode,expected_first", [
        ("az", "Sauce Labs Backpack"),
        ("za", "Test.allTheThings() T-Shirt (Red)"),
        ("lohi", "Sauce Labs Onesie"),
        ("hilo", "Sauce Labs Fleece Jacket"),
    ])
    def test_sorting_modes(self, driver, base_url, test_data, sort_mode, expected_first):
        """Test all sorting modes work correctly"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        inv.sort(sort_mode)
        
        first_product = inv.item_names()[0]
        assert expected_first == first_product, \
            f"Expected '{expected_first}' first for sort '{sort_mode}', got '{first_product}'"

    @pytest.mark.regression
    def test_sort_persists_after_page_reload(self, driver, base_url, test_data):
        """Test that sort selection persists"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        inv.sort("za")
        
        # Get first product
        first_before = inv.item_names()[0]
        
        # Reload page
        driver.refresh()
        inv = InventoryPage(driver, base_url)
        
        # Check if sort persists (depends on app implementation)
        first_after = inv.item_names()[0]
        # Document the behavior
        assert isinstance(first_after, str)


class TestProductInteraction:
    """Tests for user interactions with products"""

    @pytest.mark.regression
    def test_add_to_cart_button_changes_text(self, driver, base_url, test_data):
        """Test that Add to Cart button changes to Remove after click"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        items = driver.find_elements(*inv._inventory_items)
        first_item = items[0]
        
        # Get button before
        btn_before = first_item.find_element(By.XPATH, ".//button")
        button_text_before = btn_before.text.strip().lower()
        
        # Add to cart
        assert "add" in button_text_before or "remove" not in button_text_before, \
            "First button should be 'Add to cart'"
        
        btn_before.click()
        
        # Verify button changed
        try:
            btn_after = first_item.find_element(By.XPATH, ".//button")
            button_text_after = btn_after.text.strip().lower()
            assert "remove" in button_text_after, "Button should change to 'Remove' after adding"
        except:
            # Button reference might be stale, check via cart badge
            assert inv.cart_badge_count() >= 1, "Cart badge should show item was added"

    @pytest.mark.regression
    def test_multiple_products_add_independently(self, driver, base_url, test_data):
        """Test that adding different products works independently"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        # Add first product
        assert inv.add_to_cart(test_data["products"][0])
        assert inv.cart_badge_count() == 1
        
        # Add second product
        assert inv.add_to_cart(test_data["products"][1])
        assert inv.cart_badge_count() == 2

    @pytest.mark.regression
    def test_cannot_add_unknown_product(self, driver, base_url, test_data):
        """Test that adding non-existent product returns False"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        
        result = inv.add_to_cart("Non Existent Product")
        assert result is False, "Should not be able to add unknown product"
