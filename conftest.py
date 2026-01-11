from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pytest

@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    selenium_url = os.environ.get("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")
    driver = webdriver.Remote(command_executor=selenium_url, options=chrome_options)
    yield driver
    driver.quit()
