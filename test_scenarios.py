import os
from pages.search_page import SearchPage
from pages.register_page import RegisterPage
from pages.practitioner_page import PractitionerPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

# URL dynamique : localhost en local, "frontend" dans GitHub Actions
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


def test_inscription_reussie(browser: WebDriver):
    """Test 1 : Inscription réussie"""
    register = RegisterPage(browser, FRONTEND_URL)
    register.open()

    register.fill_form(
        "Test",
        "Automatise",
        "test.auto@email.com",
        "Password123!"
    )
    register.accept_terms()
    register.submit()

    wait = WebDriverWait(browser, 10)
    message_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert"))
    )
    message = message_element.text
    assert "Compte créé avec succès" in message, \
        f"Le message de succès attendu n'a pas été trouvé. Message reçu : {message}"


def test_email_deja_utilise(browser: WebDriver):
    """Test 2 : Email déjà utilisé"""
    register = RegisterPage(browser, FRONTEND_URL)
    register.open()

    register.fill_form(
        "Test",
        "Automatise",
        "jean.dupont@email.com",
        "Password123!"
    )
    register.accept_terms()
    register.submit()

    wait = WebDriverWait(browser, 10)
    message_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert"))
    )
    message = message_element.text
    assert "Un compte existe déjà avec cet email" in message, \
        f"Le message d'erreur attendu n'a pas été trouvé. Message reçu : {message}"


def test_recherche_praticien_par_specialite_et_ville(browser: WebDriver):
    """Recherche par spécialité et ville"""
    search = SearchPage(browser, FRONTEND_URL)
    search.open()

    search.select_specialty("Médecin généraliste")
    search.enter_city("Paris")
    search.submit()

    wait = WebDriverWait(browser, 10)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".practitioner-card"))
    )

    results = search.get_results()
    for result in results:
        name = result.find_element(By.CSS_SELECTOR, ".practitioner-name").text
        specialty = result.find_element(By.CSS_SELECTOR, ".practitioner-specialty").text
        city = result.find_element(By.CSS_SELECTOR, ".practitioner-address").text

        assert name.strip() != "", "Le nom du praticien est manquant"
        assert "Médecin généraliste" in specialty, \
            f"La spécialité est incorrecte. Reçue : {specialty}"
        assert "Paris" in city, \
            f"La ville est incorrecte. Reçue : {city}"


def test_recherche_praticien_sans_resultat(browser: WebDriver):
    """Recherche sans résultat"""
    search = SearchPage(browser, FRONTEND_URL)
    search.open()

    search.select_specialty("Cardiologue")
    search.enter_city("Titikaka")
    search.submit()

    wait = WebDriverWait(browser, 10)
    wait.until(
        lambda d: "Aucun" in d.find_element(By.TAG_NAME, "body").text
    )

    assert "Aucun praticien" in browser.find_element(By.TAG_NAME, "body").text, \
        "Le message 'Aucun praticien' n'a pas été trouvé."


def test_reservation_creneau(browser: WebDriver):
    """Test : Réservation d'un créneau pour un rendez-vous"""
    wait = WebDriverWait(browser, 10)

    # --- Connexion ---
    browser.get(f"{FRONTEND_URL}/login")
    wait.until(EC.presence_of_element_located((By.ID, "email")))

    browser.find_element(By.ID, "email").clear()
    browser.find_element(By.ID, "email").send_keys("jean.dupont@email.com")
    browser.find_element(By.ID, "password").clear()
    browser.find_element(By.ID, "password").send_keys("Password123!")

    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn"))
    )
    login_button.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#hero-title")))

    # --- Page du praticien ---
    practitioner = PractitionerPage(browser, FRONTEND_URL)
    practitioner.open("00111111-1111-1111-1111-111111111111")

    practitioner.select_day()
    practitioner.select_slot()
    practitioner.confirm()

    toast = wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, ".Toastify__toast-body > div:nth-child(2)")
    )
    wait.until(lambda d: toast.text.strip() != "")
    assert "Rendez-vous confirmé" in toast.text, \
        f"Le message de confirmation attendu n'a pas été trouvé. Message reçu : {toast.text}"

    # --- Vérification dans "Mes rendez-vous" ---
    browser.get(f"{FRONTEND_URL}/appointments")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.appointment-card"))
    )

    appointments = browser.find_elements(By.CSS_SELECTOR, "li.appointment-card h2")
    assert any("Claire Martin" in a.text for a in appointments), \
        "Le rendez-vous n'apparaît pas dans 'Mes rendez-vous'."
