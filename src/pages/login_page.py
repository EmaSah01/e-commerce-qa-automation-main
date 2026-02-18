from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    _user = (By.ID, "user-name")
    _pass = (By.ID, "password")
    _login_btn = (By.ID, "login-button")
    _error = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open_login(self):
        return self.open("/")

    def login(self, username: str, password: str):
        self.type(self._user, username)
        self.type(self._pass, password)
        self.click(self._login_btn)
        return self

    def error_text(self) -> str:
        return self.text_of(self._error)
