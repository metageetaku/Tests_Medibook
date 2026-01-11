import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

@pytest.fixture(scope="function")
def browser():
    """
    Fixture pour lancer Firefox en mode headless avec Selenium.
    Compatible CI et Xvfb.
    """
    options = Options()
    options.add_argument("--headless")  # Mode headless obligatoire pour CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(GeckoDriverManager().install())
    
    driver = webdriver.Firefox(service=service, options=options)

    # Attente optionnelle pour s'assurer que le navigateur est prêt
    time.sleep(2)
    
    yield driver
    driver.quit()
