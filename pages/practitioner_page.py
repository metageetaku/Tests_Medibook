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

    def _safe_click(self, locator):
        """Scroll + attente + clic JS fallback (méthode fiable en CI)"""
        element = self.wait.until(EC.element_to_be_clickable(locator))

        # Scroll vers l'élément
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

        try:
            element.click()
        except:
            # Fallback ultime si un overlay bloque le clic
            self.browser.execute_script("arguments[0].click();", element)

    def select_day(self):
        """Sélectionne le 4e jour disponible"""
        locator = (By.CSS_SELECTOR, "button.day-btn:nth-child(4)")
        self._safe_click(locator)

    def select_slot(self):
        """Sélectionne le 4e créneau horaire"""
        locator = (By.CSS_SELECTOR, "button.slot-btn:nth-child(4)")
        self._safe_click(locator)

    def confirm(self):
        """Clique sur le bouton de confirmation"""
        locator = (By.CSS_SELECTOR, ".btn")
        self._safe_click(locator)
