
from pages.search_page import SearchPage
from selenium.webdriver.common.by import By
from pages.register_page import RegisterPage
from pages.practitioner_page import PractitionerPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

def test_inscription_reussie(browser):
    """Test 1 : Inscription réussie"""

    register = RegisterPage(browser)

    # Ouvrir la page d'inscription
    register.open()

    # Remplir le formulaire
    register.fill_form(
        "Test",
        "Automatise",
        "test.auto@email.com",
        "Password123!"
    )

    # Accepter les CGU
    register.accept_terms()

    # Soumettre le formulaire
    register.submit()

    # Vérifier le message de succès
    message = register.get_message()
    assert "Compte créé avec succès" in message, f"Message inattendu: {message}"

def test_email_deja_utilise(browser):
    """Test 2 : Email déjà utilisé"""

    register = RegisterPage(browser)

    # Ouvrir la page d'inscription
    register.open()

    # Remplir le formulaire avec un email déjà existant
    register.fill_form(
        "Test",
        "Automatise",
        "jean.dupont@email.com",
        "Password123!"
    )

    # Accepter les CGU
    register.accept_terms()

    # Soumettre le formulaire
    register.submit()

    # Vérifier le message d'erreur
    message = register.get_message()
    assert "Un compte existe déjà avec cet email" in message, f"Message inattendu: {message}"

def test_recherche_praticien_par_specialite_et_ville(browser: WebDriver):
    """Recherche par spécialité et ville"""

    search = SearchPage(browser)
    search.open()

    # Sélection de la spécialité et de la ville
    search.select_specialty("Médecin généraliste")
    search.enter_city("Paris")
    search.submit()

    # Récupération des résultats
    results = search.get_results()

    # Vérification de chaque résultat
    for result in results:
        name = result.find_element(By.CSS_SELECTOR, ".practitioner-name").text
        specialty = result.find_element(By.CSS_SELECTOR, ".practitioner-specialty").text
        city = result.find_element(By.CSS_SELECTOR, ".practitioner-address").text

        assert name.strip() != "", "Le nom du praticien est manquant"
        assert "Médecin généraliste" in specialty, "La spécialité est incorrecte"
        assert "Paris" in city, "La ville est incorrecte"


def test_recherche_praticien_sans_resultat(browser: WebDriver):
    """Recherche sans résultat"""

    search = SearchPage(browser)
    search.open()

    # Sélection d'une spécialité et d'une ville inexistante
    search.select_specialty("Cardiologue")
    search.enter_city("Titikaka")
    search.submit()

    # Attendre que le message 'Aucun praticien' apparaisse
    wait = WebDriverWait(browser, 10)
    wait.until(lambda d: "Aucun" in d.find_element(By.TAG_NAME, "body").text)

    assert "Aucun praticien" in browser.find_element(By.TAG_NAME, "body").text

def test_reservation_creneau(browser):
    """Test : Réservation d'un créneau pour un rendez-vous"""

    wait = WebDriverWait(browser, 10)

    # --- Connexion ---
    browser.get("http://localhost:3000/login")
    wait.until(EC.presence_of_element_located((By.ID, "email")))

    browser.find_element(By.ID, "email").clear()
    browser.find_element(By.ID, "email").send_keys("jean.dupont@email.com")
    browser.find_element(By.ID, "password").clear()
    browser.find_element(By.ID, "password").send_keys("Password123!")

    # Bouton de connexion
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn")))
    login_button.click()

    # Attendre l'arrivée sur la page d'accueil
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#hero-title")))

    # --- Page du praticien ---
    practitioner = PractitionerPage(browser)
    practitioner.open("00111111-1111-1111-1111-111111111111")

    # Sélection du jour et du créneau 
    practitioner.select_day()
    practitioner.select_slot()

    # Confirmation
    practitioner.confirm()

    # --- Vérification du toast ---
    toast = wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, ".Toastify__toast-body > div:nth-child(2)")
    )
    wait.until(lambda d: toast.text.strip() != "")

    assert "Rendez-vous confirmé" in toast.text, \
        f"Message inattendu: {toast.text}"

    # --- Vérification dans "Mes rendez-vous" ---
    browser.get("http://localhost:3000/appointments")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.appointment-card")))

    appointments = browser.find_elements(By.CSS_SELECTOR, "li.appointment-card h2")
    assert any("Claire Martin" in a.text for a in appointments), \
        "Le rendez-vous n'apparaît pas dans 'Mes rendez-vous'"
    
