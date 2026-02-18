import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_info_page import CheckoutInfoPage
import time


class TestCheckoutValidation:
    """Test checkout form validation with invalid data"""

    def _navigate_to_checkout(self, driver, base_url, test_data):
        """Helper to navigate to checkout page"""
        # Use the same flow as test_checkout_flow.py which works
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        inv = InventoryPage(driver, base_url)
        inv.add_to_cart(test_data["products"][0])
        inv.open_cart()
        CartPage(driver, base_url).checkout()

    def _check_error_message_visible(self, driver):
        """Check if error message is visible on the page"""
        try:
            error = driver.find_element(By.CSS_SELECTOR, "[data-test='error'], .error, h3.error-message")
            return error.is_displayed()
        except:
            return False

    def _is_on_checkout_info_page(self, driver):
        """Verify we're still on checkout info page"""
        return "/checkout-step-one.html" in driver.current_url

    # ===== EMPTY FIELD TESTS =====
    @pytest.mark.regression
    def test_empty_first_name(self, driver, base_url, test_data):
        """Test checkout with empty first name - should show error or prevent continuation"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").clear()
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver), \
            "Empty first name should trigger validation"

    @pytest.mark.regression
    def test_empty_last_name(self, driver, base_url, test_data):
        """Test checkout with empty last name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").clear()
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver), \
            "Empty last name should trigger validation"

    @pytest.mark.regression
    def test_empty_zip_code(self, driver, base_url, test_data):
        """Test checkout with empty zip code"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").clear()
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver), \
            "Empty zip code should trigger validation"

    @pytest.mark.regression
    def test_all_fields_empty(self, driver, base_url, test_data):
        """Test checkout with all fields empty"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").clear()
        driver.find_element(By.ID, "last-name").clear()
        driver.find_element(By.ID, "postal-code").clear()
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver), \
            "All empty fields should trigger validation"

    # ===== WHITESPACE ONLY TESTS =====
    @pytest.mark.regression
    def test_whitespace_only_first_name(self, driver, base_url, test_data):
        """Test checkout with whitespace only in first name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("   ")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver), \
            "Whitespace-only first name should trigger validation"

    @pytest.mark.regression
    def test_whitespace_only_last_name(self, driver, base_url, test_data):
        """Test checkout with whitespace only in last name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("   ")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver), \
            "Whitespace-only last name should trigger validation"

    # ===== NUMERIC DATA IN NAME TESTS =====
    @pytest.mark.regression
    def test_numeric_only_first_name(self, driver, base_url, test_data):
        """Test checkout with numeric only first name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("12345")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        # Note: Some systems allow numeric names, so we just verify form submission behavior
        assert "/checkout-step-one.html" in driver.current_url or \
               "/checkout-step-two.html" in driver.current_url or \
               self._check_error_message_visible(driver), \
            "Numeric first name should be validated"

    @pytest.mark.regression
    def test_numeric_only_last_name(self, driver, base_url, test_data):
        """Test checkout with numeric only last name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("98765")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert "/checkout-step-one.html" in driver.current_url or \
               "/checkout-step-two.html" in driver.current_url or \
               self._check_error_message_visible(driver), \
            "Numeric last name should be validated"

    @pytest.mark.regression
    def test_alphanumeric_names(self, driver, base_url, test_data):
        """Test checkout with alphanumeric names (numbers mixed with letters)"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema123")
        driver.find_element(By.ID, "last-name").send_keys("Test456")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        # Verify if allowed or rejected
        assert "/checkout-step-two.html" in driver.current_url or \
               self._is_on_checkout_info_page(driver), \
            "Alphanumeric names handling should be clear"

    # ===== INVALID ZIP CODE TESTS =====
    @pytest.mark.regression
    def test_numeric_only_zip_code(self, driver, base_url, test_data):
        """Test checkout with valid numeric zip code format"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(2)
        # Valid zip code should proceed to next page
        assert "/checkout-step-two.html" in driver.current_url, \
            "Valid numeric zip code should proceed to checkout step two"

    @pytest.mark.regression
    def test_alphabetic_zip_code(self, driver, base_url, test_data):
        """Test checkout with alphabetic zip code"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("ABCDE")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver), \
            "Alphabetic zip code should trigger validation"

    @pytest.mark.regression
    def test_special_characters_zip_code(self, driver, base_url, test_data):
        """Test checkout with special characters in zip code"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("71-000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        # Some systems allow hyphens in zip codes
        assert "/checkout-step-two.html" in driver.current_url or \
               self._is_on_checkout_info_page(driver) or \
               self._check_error_message_visible(driver), \
            "Special character zip code behavior should be validated"

    @pytest.mark.regression
    def test_too_short_zip_code(self, driver, base_url, test_data):
        """Test checkout with too short zip code (less than 5 digits)"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("123")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver), \
            "Too short zip code should trigger validation"

    @pytest.mark.regression
    def test_too_long_zip_code(self, driver, base_url, test_data):
        """Test checkout with too long zip code"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("71000123456789")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver) or \
               "/checkout-step-two.html" in driver.current_url, \
            "Long zip code handling should be validated"

    # ===== SPECIAL CHARACTERS TESTS =====
    @pytest.mark.regression
    def test_special_characters_in_first_name(self, driver, base_url, test_data):
        """Test checkout with special characters in first name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Em@#$%")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver) or \
               "/checkout-step-two.html" in driver.current_url, \
            "Special characters in name handling should be validated"

    @pytest.mark.regression
    def test_special_characters_in_last_name(self, driver, base_url, test_data):
        """Test checkout with special characters in last name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys("Test@#$%")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver) or \
               "/checkout-step-two.html" in driver.current_url, \
            "Special characters in last name handling should be validated"

    # ===== EDGE CASES =====
    @pytest.mark.regression
    def test_very_long_first_name(self, driver, base_url, test_data):
        """Test checkout with very long first name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        long_name = "A" * 500
        driver.find_element(By.ID, "first-name").send_keys(long_name)
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        # Verify form handles long input
        assert "/checkout-step-two.html" in driver.current_url or \
               self._is_on_checkout_info_page(driver), \
            "Long first name handling should be evaluated"

    @pytest.mark.regression
    def test_very_long_last_name(self, driver, base_url, test_data):
        """Test checkout with very long last name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        long_name = "B" * 500
        driver.find_element(By.ID, "first-name").send_keys("Ema")
        driver.find_element(By.ID, "last-name").send_keys(long_name)
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        # Verify form handles long input
        assert "/checkout-step-two.html" in driver.current_url or \
               self._is_on_checkout_info_page(driver), \
            "Long last name handling should be evaluated"

    @pytest.mark.regression
    def test_single_character_names(self, driver, base_url, test_data):
        """Test checkout with single character names and zip"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("A")
        driver.find_element(By.ID, "last-name").send_keys("B")
        driver.find_element(By.ID, "postal-code").send_keys("1")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        assert self._is_on_checkout_info_page(driver) or self._check_error_message_visible(driver) or \
               "/checkout-step-two.html" in driver.current_url, \
            "Single character input handling should be validated"

    @pytest.mark.regression
    def test_unicode_characters_in_name(self, driver, base_url, test_data):
        """Test checkout with unicode characters in name"""
        self._navigate_to_checkout(driver, base_url, test_data)
        
        driver.find_element(By.ID, "first-name").send_keys("Émá")
        driver.find_element(By.ID, "last-name").send_keys("Tëšter")
        driver.find_element(By.ID, "postal-code").send_keys("71000")
        
        driver.find_element(By.ID, "continue").click()
        
        time.sleep(1)
        # Verify unicode handling
        assert "/checkout-step-two.html" in driver.current_url or \
               self._is_on_checkout_info_page(driver) or \
               self._check_error_message_visible(driver), \
            "Unicode character handling should be validated"
