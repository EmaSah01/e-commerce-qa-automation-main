from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage

class CheckoutOverviewPage(BasePage):
    _finish = (By.ID, "finish")

    def finish(self):
        self.click(self._finish)
        # čekaj finalnu (complete) stranicu i header
        self.wait.wait.until(EC.url_contains("/checkout-complete.html"))
        self.wait.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.complete-header, .complete-header")))
        return self
