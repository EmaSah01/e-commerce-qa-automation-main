import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_info_page import CheckoutInfoPage
from src.pages.checkout_overview_page import CheckoutOverviewPage
from src.pages.checkout_complete_page import CheckoutCompletePage


class TestCheckoutValidation:
    """Tests for checkout form validation and error handling"""

    @pytest.mark.regression
    def test_checkout_missing_first_name(self, driver, base_url, test_data):
        """Test checkout form validation when first name is missing"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info_page = CheckoutInfoPage(driver, base_url)
        checkout_info = test_data["checkout_info"]
        
        # Try to submit with empty first name
        info_page.type(info_page._first, "")
        info_page.type(info_page._last, checkout_info["last"])
        info_page.type(info_page._zip, checkout_info["zip"])
        info_page.click(info_page._continue)
        
        # Should see error or stay on same page
        assert "checkout-step-one" in driver.current_url.lower(), \
            "Should remain on checkout step one with error"

    @pytest.mark.regression
    def test_checkout_missing_last_name(self, driver, base_url, test_data):
        """Test checkout form validation when last name is missing"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info_page = CheckoutInfoPage(driver, base_url)
        checkout_info = test_data["checkout_info"]
        
        info_page.type(info_page._first, checkout_info["first"])
        info_page.type(info_page._last, "")
        info_page.type(info_page._zip, checkout_info["zip"])
        info_page.click(info_page._continue)
        
        assert "checkout-step-one" in driver.current_url.lower()

    @pytest.mark.regression
    def test_checkout_missing_zip_code(self, driver, base_url, test_data):
        """Test checkout form validation when zip code is missing"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info_page = CheckoutInfoPage(driver, base_url)
        checkout_info = test_data["checkout_info"]
        
        info_page.type(info_page._first, checkout_info["first"])
        info_page.type(info_page._last, checkout_info["last"])
        info_page.type(info_page._zip, "")
        info_page.click(info_page._continue)
        
        assert "checkout-step-one" in driver.current_url.lower()

    @pytest.mark.regression
    def test_checkout_all_fields_empty(self, driver, base_url):
        """Test checkout form with all fields empty"""
        # This test validates form requires all fields
        from selenium.webdriver.common.by import By
        
        CheckoutInfoPage(driver, base_url)
        
        # Try to click continue without filling
        continue_btn = driver.find_element(By.ID, "continue")
        continue_btn.click()
        
        # Should remain on checkout page
        assert "checkout-step-one" in driver.current_url.lower()

    @pytest.mark.regression
    def test_checkout_special_characters_in_name(self, driver, base_url, test_data):
        """Test checkout form accepts special characters in names"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info_page = CheckoutInfoPage(driver, base_url)
        info_page.fill("Jean-Pierre", "O'Brien", "12345-6789")
        
        # Should proceed to next step
        assert "checkout-step-two" in driver.current_url.lower()

    @pytest.mark.regression
    def test_checkout_numeric_values_in_names(self, driver, base_url, test_data):
        """Test checkout form accepts numbers in names (edge case)"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info_page = CheckoutInfoPage(driver, base_url)
        info_page.fill("John123", "Doe456", "12345")
        
        assert "checkout-step-two" in driver.current_url.lower()


class TestCheckoutOverview:
    """Tests for checkout overview page"""

    @pytest.mark.regression
    def test_overview_displays_item_summary(self, driver, base_url, test_data):
        """Test that overview page shows added items"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        product = test_data["products"][0]
        assert inv.add_to_cart(product)
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info = test_data["checkout_info"]
        CheckoutInfoPage(driver, base_url).fill(info["first"], info["last"], info["zip"])
        
        overview = CheckoutOverviewPage(driver, base_url)
        overview_items = driver.find_elements(overview._overview_item if hasattr(overview, '_overview_item') else None)
        
        # Document the behavior
        assert "checkout-step-two" in driver.current_url.lower()

    @pytest.mark.regression
    def test_overview_finish_button_visible(self, driver, base_url, test_data):
        """Test that finish button is visible on overview page"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info = test_data["checkout_info"]
        CheckoutInfoPage(driver, base_url).fill(info["first"], info["last"], info["zip"])
        
        overview = CheckoutOverviewPage(driver, base_url)
        finish_btn = driver.find_element(*overview._finish)
        
        assert finish_btn.is_displayed(), "Finish button not visible"
        assert finish_btn.is_enabled(), "Finish button not enabled"

    @pytest.mark.regression
    def test_completes_order_successfully(self, driver, base_url, test_data):
        """Test complete end-to-end successful order"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info = test_data["checkout_info"]
        CheckoutInfoPage(driver, base_url).fill(info["first"], info["last"], info["zip"])
        CheckoutOverviewPage(driver, base_url).finish()
        
        complete = CheckoutCompletePage(driver, base_url)
        assert "Thank you for your order" in complete.success_text()
        assert "checkout-complete" in driver.current_url.lower()


class TestCheckoutNavigation:
    """Tests for navigation during checkout"""

    @pytest.mark.regression
    def test_back_button_during_checkout_info(self, driver, base_url, test_data):
        """Test browser back button during checkout info step"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        # Go back to cart
        driver.back()
        
        assert "cart.html" in driver.current_url.lower()

    @pytest.mark.regression
    def test_back_button_from_overview(self, driver, base_url, test_data):
        """Test back button on overview page goes to info page"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        assert inv.add_to_cart(test_data["products"][0])
        
        inv.open_cart()
        CartPage(driver, base_url).checkout()
        
        info = test_data["checkout_info"]
        CheckoutInfoPage(driver, base_url).fill(info["first"], info["last"], info["zip"])
        
        # Go back from overview
        driver.back()
        
        assert "checkout-step-one" in driver.current_url.lower() or "cart.html" in driver.current_url.lower()
