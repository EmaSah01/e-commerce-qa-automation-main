from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage

class CartPage(BasePage):
    _cart_item = (By.CSS_SELECTOR, ".cart_item")
    _checkout_btn = (By.ID, "checkout")

    def items(self):
        return self.driver.find_elements(*self._cart_item)

    def checkout(self):
        # klik na Checkout i čekaj step one (info formu)
        self.click(self._checkout_btn)
        self.wait.wait.until(EC.url_contains("/checkout-step-one.html"))
        self.wait.wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        return self
