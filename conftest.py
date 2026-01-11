# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

@pytest.fixture
def browser():
    remote_url = os.environ.get("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")
    driver = webdriver.Remote(
        command_executor=remote_url,
        desired_capabilities=DesiredCapabilities.FIREFOX
    )
    yield driver
    driver.quit()
