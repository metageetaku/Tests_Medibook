import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.headless = True  # True = pas de fenêtre, parfait pour CI
    # Sur Windows GitHub runner, Firefox est déjà dans le PATH
    service = Service()  # Selenium trouvera geckodriver automatiquement
    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    driver.quit()
