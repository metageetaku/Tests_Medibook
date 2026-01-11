from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pytest

@pytest.fixture
def browser():
    options = Options()
    options.headless = True
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",  # nom du service Selenium
        options=options
    )
    yield driver
    driver.quit()
