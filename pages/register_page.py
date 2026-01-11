from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    def open(self):
        self.browser.get(f"{self.base_url}/register")


    def open(self):
        """Ouvre la page d'inscription"""
        self.browser.get("http://localhost:3000/register")
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

    def accept_terms(self):
        """Coche la case des CGU"""
        self.browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/main/div/div/form/div[6]/label/input"
        ).click()

    def submit(self):
        """Clique sur le bouton d'inscription"""
        self.browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/main/div/div/form/button"
        ).click()

    def get_message(self):
        """Récupère le message de succès ou d'erreur"""
        return self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div[1]/main/div/div/div[2]/span")
            )
        ).text
