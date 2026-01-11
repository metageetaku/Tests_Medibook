from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class SearchPage:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    def open(self):
        self.browser.get(f"{self.base_url}/search")


    def open(self):
        """Ouvre la page de recherche"""
        self.browser.get("http://localhost:3000/search")
        self.wait.until(EC.presence_of_element_located((By.ID, "specialty")))

    def select_specialty(self, text):
        """Sélectionne une spécialité dans la liste déroulante"""
        Select(self.browser.find_element(By.ID, "specialty")).select_by_visible_text(text)

    def enter_city(self, city):
        """Saisit une ville dans le champ de recherche"""
        field = self.browser.find_element(By.ID, "city")
        field.clear()
        field.send_keys(city)

    def submit(self):
        """Clique sur le bouton Rechercher"""
        self.browser.find_element(By.XPATH, "//button[contains(text(),'Rechercher')]").click()

    def get_results(self):
        """Retourne la liste des résultats trouvés"""
        return self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".practitioner-info"))
        )
