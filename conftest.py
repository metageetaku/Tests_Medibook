# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os

@pytest.fixture
def browser():
    firefox_options = Options()
    firefox_options.headless = True  # headless pour CI

    remote_url = os.environ.get("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")

    # Correct pour Selenium 4+
    driver = webdriver.Remote(
        command_executor=remote_url,
        options=firefox_options
    )
    yield driver
    driver.quit()
