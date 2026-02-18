# src/pages/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.support.ui import Select

from src.pages.base_page import BasePage


class InventoryPage(BasePage):
    # ----- Locators -----
    _title = (By.CSS_SELECTOR, ".title")
    _inventory_items = (By.CSS_SELECTOR, ".inventory_item")
    _sort_select = (By.CSS_SELECTOR, "select[data-test='product-sort-container']")
    _cart_link = (By.CSS_SELECTOR, ".shopping_cart_link")
    _cart_badge = (By.CSS_SELECTOR, ".shopping_cart_badge")

    _PRODUCT_TO_DATATEST = {
        "Sauce Labs Backpack": "add-to-cart-sauce-labs-backpack",
        "Sauce Labs Bike Light": "add-to-cart-sauce-labs-bike-light",
        "Sauce Labs Bolt T-Shirt": "add-to-cart-sauce-labs-bolt-t-shirt",
        "Sauce Labs Fleece Jacket": "add-to-cart-sauce-labs-fleece-jacket",
        "Sauce Labs Onesie": "add-to-cart-sauce-labs-onesie",
        "Test.allTheThings() T-Shirt (Red)": "add-to-cart-test.allthethings()-t-shirt-(red)",
    }

    # ----- Status/helpers -----
    def is_loaded(self) -> bool:
        return self.is_visible(self._title)

    def item_names(self):
        self.wait.wait.until(EC.presence_of_all_elements_located(self._inventory_items))
        items = self.driver.find_elements(*self._inventory_items)
        names = []
        for i in items:
            try:
                names.append(
                    i.find_element(By.CSS_SELECTOR, ".inventory_item_name, [data-test='inventory-item-name']").text
                )
            except NoSuchElementException:
                continue
        return names

    def sort(self, mode: str):
        """mode ∈ {'az','za','lohi','hilo'}"""
        self.wait.wait.until(EC.element_to_be_clickable(self._sort_select))
        Select(self.driver.find_element(*self._sort_select)).select_by_value(mode)
        self.wait.wait.until(EC.presence_of_all_elements_located(self._inventory_items))
        return self

    def cart_badge_count(self) -> int:
        return int(self.driver.find_element(*self._cart_badge).text) if self.is_visible(self._cart_badge) else 0

    def cart_count(self) -> int:
        return self.cart_badge_count()

    # ----- Actions -----
    def add_to_cart(self, product_name: str) -> bool:
        """
        Stabilno dodavanje u korpu:
        - kartica se traži XPath-om sa navodnicima oko imena
        - preferira se 'data-test' dugme
        - klika se kroz retry koji svježe refinda element (izbjegava stale)
        - potvrđuje se preko 'remove-*' ili badge +1
        """
        # Listing učitan
        self.wait.wait.until(EC.presence_of_element_located(self._title))
        self.wait.wait.until(EC.presence_of_all_elements_located(self._inventory_items))

        # Kartica proizvoda (OBAVEZNO navodnici u XPath-u)
        card_xpath = (
            "//div[contains(@class,'inventory_item')]"
            "[.//div[(@class='inventory_item_name' or contains(@class,'inventory_item_name') "
            "or @data-test='inventory-item-name') and normalize-space()='%s']]" % product_name
        )
        try:
            card = self.driver.find_element(By.XPATH, card_xpath)
        except NoSuchElementException:
            return False

        # Ako je već u korpi — gotovo
        try:
            txt = card.find_element(By.XPATH, ".//button").text.strip().lower()
            if txt == "remove":
                return True
        except NoSuchElementException:
            pass

        # Primarni lokator: data-test, pa fallbackovi
        data_test = self._PRODUCT_TO_DATATEST.get(product_name)
        add_locators = []
        if data_test:
            add_locators.append((By.CSS_SELECTOR, f"button[data-test='{data_test}']"))
        add_locators += [
            (By.XPATH, ".//button[contains(@data-test,'add-to-cart')]"),
            (By.XPATH, ".//button[normalize-space()='Add to cart']"),
            (By.CSS_SELECTOR, ".pricebar button.btn_inventory"),
        ]

        import time

        def click_with_retry(container_locator, button_locator, retries=3, pause=0.25):
            """
            Svaki pokušaj ponovo traži i karticu i dugme (izbjegava stale).
            container_locator: (By, value) koji opisuje trenutnu karticu/okvir
            button_locator: (By, value) za dugme unutar tog okvira
            """
            last_err = None
            for _ in range(retries):
                try:
                    container = self.driver.find_element(*container_locator)
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", container)
                    btn = container.find_element(*button_locator)
                    # `element_to_be_clickable` sa lokatorom preko lambda re-find:
                    self.wait.wait.until(lambda d: btn.is_displayed() and btn.is_enabled())
                    btn.click()
                    return True
                except (StaleElementReferenceException, NoSuchElementException) as e:
                    last_err = e
                    time.sleep(pause)
            if last_err:
                raise last_err
            return False

        # Locator za “trenutnu” karticu (da je lako refind-amo u retry-ju)
        card_locator = (By.XPATH, card_xpath)

        # Pokušaj na listingu
        before = self.cart_badge_count()
        for loc in add_locators:
            try:
                if click_with_retry(card_locator, loc):
                    break
            except (NoSuchElementException, StaleElementReferenceException):
                continue
        else:
            # Fallback: detalj proizvoda
            try:
                name_el = self.driver.find_element(
                    By.XPATH, card_xpath + "//*[@data-test='inventory-item-name' or contains(@class,'inventory_item_name')]"
                )
                name_el.click()
                self.wait.wait.until(EC.presence_of_element_located((By.ID, "inventory_item_container")))
                detail_locator = (By.ID, "inventory_item_container")

                for loc in add_locators:
                    try:
                        if click_with_retry(detail_locator, loc):
                            break
                    except (NoSuchElementException, StaleElementReferenceException):
                        continue
                else:
                    return False

                # Potvrda na detalju
                try:
                    if data_test:
                        remove_dt = data_test.replace("add-to-cart", "remove")
                        self.wait.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, f"button[data-test='{remove_dt}']"))
                        )
                    else:
                        self.wait.wait.until(EC.text_to_be_present_in_element((By.XPATH, "//button"), "Remove"))
                except TimeoutException:
                    self.wait.wait.until(lambda d: self.cart_badge_count() == before + 1)

                # Nazad na listing
                self.driver.back()
                self.wait.wait.until(EC.presence_of_all_elements_located(self._inventory_items))
                return True

            except (NoSuchElementException, TimeoutException):
                return False

        # Potvrda na listingu
        try:
            if data_test:
                remove_dt = data_test.replace("add-to-cart", "remove")
                self.wait.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"button[data-test='{remove_dt}']"))
                )
            else:
                # bar promjena teksta na prvom dugmetu u kartici
                self.wait.wait.until(EC.text_to_be_present_in_element((By.XPATH, ".//button"), "Remove"))
        except TimeoutException:
            self.wait.wait.until(lambda d: self.cart_badge_count() == before + 1)

        return True

    def open_cart(self):
        self.click(self._cart_link)
        self.wait.wait.until(EC.url_contains("/cart.html"))
        self.wait.wait.until(EC.presence_of_element_located((By.ID, "cart_contents_container")))
        return self
