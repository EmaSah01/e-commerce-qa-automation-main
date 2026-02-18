# conftest.py
import os
import json
import pytest
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=os.getenv("BASE_URL", "https://www.saucedemo.com"),
    )
    parser.addoption("--browser", action="store", default=os.getenv("BROWSER", "chrome"))
    parser.addoption("--headed", action="store_true", help="Run headed (disable headless)")
    parser.addoption("--window-size", action="store", default=os.getenv("WINDOW_SIZE", "1440,900"))
    parser.addoption("--implicit-wait", action="store", default=os.getenv("IMPLICIT_WAIT", "2"))
    # 🔥 nova opcija
    parser.addoption("--keep-browser-open", action="store_true", help="Do not quit browser after test")


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("--base-url").rstrip("/")


@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("--browser").lower()


@pytest.fixture(scope="function")
def driver(pytestconfig, browser_name):
    headed = pytestconfig.getoption("--headed")
    keep_open = pytestconfig.getoption("--keep-browser-open")
    size = pytestconfig.getoption("--window-size")
    implicit = int(pytestconfig.getoption("--implicit-wait"))
    w, h = [int(x) for x in size.split(",")] if "," in size else (1440, 900)

    if browser_name == "firefox":
        opts = FirefoxOptions()
        if not headed:
            opts.add_argument("-headless")
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        drv = webdriver.Firefox(service=service, options=opts)
    else:
        opts = ChromeOptions()
        if not headed:
            opts.add_argument("--headless=new")
        opts.add_argument(f"--window-size={w},{h}")
        opts.add_argument("--disable-gpu")
        service = ChromeService(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=opts)

    drv.implicitly_wait(implicit)
    yield drv

    # 🔥 zatvori samo ako korisnik nije tražio da ostane otvoren
    if not keep_open:
        drv.quit()


@pytest.fixture(scope="session")
def test_data():
    with open("src/data/users.json", "r", encoding="utf-8") as f:
        return json.load(f)
