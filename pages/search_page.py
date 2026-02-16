from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class SearchPage:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.wait = WebDriverWait(browser, 10)

    def open(self):
        """Ouvre la page de recherche"""
        self.browser.get(f"{self.base_url}/search")
        self.wait.until(EC.presence_of_element_located((By.ID, "specialty")))

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

    def select_specialty(self, text):
        """Sélectionne une spécialité dans la liste déroulante"""
        dropdown = self.wait.until(EC.presence_of_element_located((By.ID, "specialty")))
        Select(dropdown).select_by_visible_text(text)

    def enter_city(self, city):
        """Saisit une ville dans le champ de recherche"""
        field = self.wait.until(EC.presence_of_element_located((By.ID, "city")))
        field.clear()
        field.send_keys(city)

    def submit(self):
        """Clique sur le bouton Rechercher"""
        locator = (By.CSS_SELECTOR, "button[type='submit']")
        self._safe_click(locator)

    def get_results(self):
        """Retourne la liste des résultats trouvés"""
        return self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".practitioner-info"))
        )
