from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.wait = WebDriverWait(browser, 10)

    def open(self):
        """Ouvre la page d'inscription"""
        self.browser.get(f"{self.base_url}/register")
        self.wait.until(EC.presence_of_element_located((By.ID, "firstName")))

    def fill_form(self, first, last, email, password):
        """Remplit le formulaire d'inscription"""
        self.browser.find_element(By.ID, "firstName").clear()
        self.browser.find_element(By.ID, "firstName").send_keys(first)

        self.browser.find_element(By.ID, "lastName").clear()
        self.browser.find_element(By.ID, "lastName").send_keys(last)

        self.browser.find_element(By.ID, "email").clear()
        self.browser.find_element(By.ID, "email").send_keys(email)

        self.browser.find_element(By.ID, "password").clear()
        self.browser.find_element(By.ID, "password").send_keys(password)

        self.browser.find_element(By.ID, "confirmPassword").clear()
        self.browser.find_element(By.ID, "confirmPassword").send_keys(password)

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

    def accept_terms(self):
        """Coche la case des CGU"""
        locator = (By.CSS_SELECTOR, "input[type='checkbox']")
        self._safe_click(locator)

    def submit(self):
        """Clique sur le bouton d'inscription"""
        locator = (By.CSS_SELECTOR, "button[type='submit']")
        self._safe_click(locator)

    def get_message(self):
        """Récupère le message de succès ou d'erreur"""
        return self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "main div span")
            )
        ).text
