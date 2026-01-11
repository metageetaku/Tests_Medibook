import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

@pytest.fixture
def browser():
    options = Options()
    options.headless = True
    service = Service()
    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    driver.quit()
