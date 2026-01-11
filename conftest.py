import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

@pytest.fixture(scope="function")
def browser():
    options = Options()
    options.add_argument("--headless")  # mode headless pour CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # point vers geckodriver installé par apt
    service = Service("/usr/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=options)

    yield driver
    driver.quit()
