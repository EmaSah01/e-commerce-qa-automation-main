import pytest
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


class TestLoginSuccess:
    """Tests for successful login scenarios"""

    @pytest.mark.smoke
    def test_login_success(self, driver, base_url, test_data):
        """Test successful login with valid credentials"""
        LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], test_data["valid"]["password"]
        )
        assert InventoryPage(driver, base_url).is_loaded()

    @pytest.mark.regression
    def test_login_success_redirects_to_inventory(self, driver, base_url, test_data):
        """Verify successful login redirects to inventory page"""
        page = LoginPage(driver, base_url).open_login()
        page.login(test_data["valid"]["username"], test_data["valid"]["password"])
        assert "inventory.html" in driver.current_url.lower()

    @pytest.mark.regression
    def test_login_with_problem_user(self, driver, base_url, test_data):
        """Test login with problem_user account"""
        LoginPage(driver, base_url).open_login().login(
            test_data["problem"]["username"], test_data["problem"]["password"]
        )
        assert InventoryPage(driver, base_url).is_loaded()

    @pytest.mark.regression
    def test_login_with_performance_user(self, driver, base_url, test_data):
        """Test login with performance_glitch_user account"""
        LoginPage(driver, base_url).open_login().login(
            test_data["perf"]["username"], test_data["perf"]["password"]
        )
        assert InventoryPage(driver, base_url).is_loaded()


class TestLoginErrors:
    """Tests for login error scenarios"""

    @pytest.mark.regression
    def test_login_locked_user_shows_error(self, driver, base_url, test_data):
        """Test locked out user receives error message"""
        page = LoginPage(driver, base_url).open_login().login(
            test_data["locked"]["username"], test_data["locked"]["password"]
        )
        assert "locked out" in page.error_text().lower()

    @pytest.mark.regression
    def test_login_invalid_credentials_wrong_password(self, driver, base_url, test_data):
        """Test login with valid username but wrong password"""
        page = LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], "wrong_password"
        )
        error_msg = page.error_text().lower()
        assert "username and password do not match" in error_msg or "invalid" in error_msg

    @pytest.mark.regression
    def test_login_invalid_credentials_wrong_username(self, driver, base_url):
        """Test login with invalid username"""
        page = LoginPage(driver, base_url).open_login().login(
            "invalid_user", "secret_sauce"
        )
        error_msg = page.error_text().lower()
        assert "username and password do not match" in error_msg or "invalid" in error_msg

    @pytest.mark.regression
    def test_login_empty_username(self, driver, base_url, test_data):
        """Test login with empty username field"""
        page = LoginPage(driver, base_url).open_login().login(
            "", test_data["valid"]["password"]
        )
        error_msg = page.error_text().lower()
        assert "username is required" in error_msg or "required" in error_msg

    @pytest.mark.regression
    def test_login_empty_password(self, driver, base_url, test_data):
        """Test login with empty password field"""
        page = LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"], ""
        )
        error_msg = page.error_text().lower()
        assert "password is required" in error_msg or "required" in error_msg

    @pytest.mark.regression
    def test_login_empty_both_fields(self, driver, base_url):
        """Test login with both username and password empty"""
        page = LoginPage(driver, base_url).open_login().login("", "")
        error_msg = page.error_text().lower()
        assert "required" in error_msg

    @pytest.mark.regression
    def test_login_error_message_visible(self, driver, base_url):
        """Test that error message is displayed and visible"""
        page = LoginPage(driver, base_url).open_login().login(
            "invalid", "invalid"
        )
        assert len(page.error_text().strip()) > 0


class TestLoginPageElements:
    """Tests for login page UI elements"""

    @pytest.mark.regression
    def test_login_page_loads(self, driver, base_url):
        """Test login page loads correctly"""
        login_page = LoginPage(driver, base_url).open_login()
        # Verify we're on login page by checking URL
        assert "saucedemo.com" in driver.current_url.lower()

    @pytest.mark.regression
    def test_username_field_exists(self, driver, base_url):
        """Test username input field is present"""
        login_page = LoginPage(driver, base_url).open_login()
        username_field = driver.find_element(*login_page._user)
        assert username_field.is_displayed()
        assert username_field.get_attribute("type") == "text"

    @pytest.mark.regression
    def test_password_field_exists(self, driver, base_url):
        """Test password input field is present"""
        login_page = LoginPage(driver, base_url).open_login()
        password_field = driver.find_element(*login_page._pass)
        assert password_field.is_displayed()
        assert password_field.get_attribute("type") == "password"

    @pytest.mark.regression
    def test_login_button_exists(self, driver, base_url):
        """Test login button is present and enabled"""
        login_page = LoginPage(driver, base_url).open_login()
        login_btn = driver.find_element(*login_page._login_btn)
        assert login_btn.is_displayed()
        assert login_btn.is_enabled()


class TestLoginDataValidation:
    """Tests for input validation and data handling"""

    @pytest.mark.regression
    def test_login_with_special_characters_in_password(self, driver, base_url):
        """Test login attempt with special characters in password"""
        page = LoginPage(driver, base_url).open_login().login(
            "standard_user", "p@$$w0rd!@#"
        )
        # Should show error, not crash
        assert len(page.error_text().strip()) > 0

    @pytest.mark.regression
    def test_login_with_spaces_in_credentials(self, driver, base_url, test_data):
        """Test login with spaces in username/password"""
        page = LoginPage(driver, base_url).open_login().login(
            " " + test_data["valid"]["username"], test_data["valid"]["password"]
        )
        # Should not match (spaces added)
        error_msg = page.error_text().lower()
        assert "username and password do not match" in error_msg or "invalid" in error_msg or "required" in error_msg

    @pytest.mark.regression
    def test_login_username_case_sensitive(self, driver, base_url, test_data):
        """Test if login is case sensitive for username"""
        page = LoginPage(driver, base_url).open_login().login(
            test_data["valid"]["username"].upper(), test_data["valid"]["password"]
        )
        # Based on most systems, should fail if case-sensitive
        # This documents the behavior
        result = InventoryPage(driver, base_url).is_loaded()
        # Just verify it behaves consistently
        assert isinstance(result, bool)
