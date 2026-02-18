from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage

class CheckoutInfoPage(BasePage):
    _first = (By.ID, "first-name")
    _last = (By.ID, "last-name")
    _zip = (By.ID, "postal-code")
    _continue = (By.ID, "continue")

    def fill(self, first: str, last: str, zip_code: str):
        # osiguraj da su polja vidljiva
        self.wait.visible(self._first)
        self.type(self._first, first)
        self.type(self._last, last)
        self.type(self._zip, zip_code)
        self.click(self._continue)

        # čekaj overview (step two)
        self.wait.wait.until(EC.url_contains("/checkout-step-two.html"))
        self.wait.wait.until(EC.presence_of_element_located((By.ID, "finish")))
        return self
