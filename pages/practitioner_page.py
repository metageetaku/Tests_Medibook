from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PractitionerPage:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.wait = WebDriverWait(browser, 10)

    def open(self, practitioner_id):
        """Ouvre la page du praticien"""
        self.browser.get(f"{self.base_url}/practitioners/{practitioner_id}")
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".practitioner-main-info"))
        )

    def select_day(self):
        """Sélectionne le 4e jour disponible"""
        day_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.day-btn:nth-child(4) > span:nth-child(2)")
            )
        )
        day_button.click()

    def select_slot(self):
        """Sélectionne le 4e créneau horaire"""
        slot_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.slot-btn:nth-child(4)")
            )
        )
        slot_button.click()

    def confirm(self):
        """Clique sur le bouton de confirmation"""
        confirm_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn"))
        )
        confirm_button.click()
