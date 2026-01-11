import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless=new")  # Mode headless
    options.add_argument("--no-sandbox")    # GitHub Actions spécifique
    options.add_argument("--disable-dev-shm-usage")  # GitHub Actions spécifique

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
