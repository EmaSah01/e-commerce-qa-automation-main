# src/pages/base_page.py
from src.utils.wait import Wait

class BasePage:
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = Wait(driver)

    def open(self, path: str = "/"):
        self.driver.get(self.base_url + path)
        return self

    def type(self, locator, text: str):
        el = self.wait.visible(locator)
        el.clear()
        el.send_keys(text)
        return el

    def click(self, locator):
        el = self.wait.clickable(locator)
        el.click()
        return el

    def text_of(self, locator) -> str:
        return self.wait.visible(locator).text

    def is_visible(self, locator) -> bool:
        try:
            self.wait.visible(locator)
            return True
        except Exception:
            return False
