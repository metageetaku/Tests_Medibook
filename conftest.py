import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

@pytest.fixture(scope="function")
def browser():
    """Fixture ultra-simple pour Firefox"""
    options = Options()
    service = Service(executable_path="C:\\Windows\\geckodriver.exe")
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
