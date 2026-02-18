from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class CheckoutCompletePage(BasePage):
    _header = (By.CSS_SELECTOR, "h2.complete-header, .complete-header")

    def success_text(self) -> str:
        return self.text_of(self._header)
