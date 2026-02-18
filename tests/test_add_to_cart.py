from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

_PRODUCT_TO_DATATEST = {
    "Sauce Labs Backpack": "add-to-cart-sauce-labs-backpack",
    "Sauce Labs Bike Light": "add-to-cart-sauce-labs-bike-light",
    "Sauce Labs Bolt T-Shirt": "add-to-cart-sauce-labs-bolt-t-shirt",
    "Sauce Labs Fleece Jacket": "add-to-cart-sauce-labs-fleece-jacket",
    "Sauce Labs Onesie": "add-to-cart-sauce-labs-onesie",
    "Test.allTheThings() T-Shirt (Red)": "add-to-cart-test.allthethings()-t-shirt-(red)",
}

def add_to_cart(self, product_name: str) -> bool:
    self.wait.wait.until(EC.presence_of_all_elements_located(self._inventory_items))

    if product_name not in _PRODUCT_TO_DATATEST:
        return False  # nepoznat proizvod u mapi

    add_dt = _PRODUCT_TO_DATATEST[product_name]
    remove_dt = add_dt.replace("add-to-cart", "remove")

    def _click_add_by_datatest(container=None) -> bool:
        try:
            locator = (By.CSS_SELECTOR, f"button[data-test='{add_dt}']")
            btn = (container.find_element(*locator) if container else self.driver.find_element(*locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", btn)
            self.wait.wait.until(EC.element_to_be_clickable(locator))
            btn.click()
            self.wait.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"button[data-test='{remove_dt}']")))
            return True
        except Exception:
            return False

    if _click_add_by_datatest():
        return True

    try:
        name_link = self.driver.find_element(
            By.XPATH,
            f"//div[contains(@class,'inventory_item_name') and normalize-space()='{product_name}']"
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", name_link)
        name_link.click()

        self.wait.wait.until(EC.presence_of_element_located((By.ID, "inventory_item_container")))
        if _click_add_by_datatest():
            self.driver.back()
            self.wait.wait.until(EC.presence_of_all_elements_located(self._inventory_items))
            return True
    except (NoSuchElementException, TimeoutException):
        pass

    return False
