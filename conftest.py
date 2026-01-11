# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

@pytest.fixture(scope="function")
def browser():
    options = Options()
    options.add_argument("--headless")  # headless pour CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Point vers geckodriver téléchargé par le workflow
    service = Service("/usr/local/bin/geckodriver")

    driver = webdriver.Firefox(service=service, options=options, timeout=180)
    yield driver
    driver.quit()
