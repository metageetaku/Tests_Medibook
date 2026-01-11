import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def clean_and_restart_docker():
        # Arrête et supprime TOUS les conteneurs, réseaux et volumes définis dans docker-compose.yml
        subprocess.run(["docker", "compose", "down", "-v"], check=True)

        # Relance les conteneurs en reconstruisant les images
        subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)

        time.sleep(20)

def create_user_with_selenium():
    """Crée un utilisateur via Selenium avec les bons sélecteurs."""
    print("Création d'un utilisateur...")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    try:
        driver.get("http://localhost:3000/register")

        # Remplit le formulaire
        driver.find_element(By.ID, "firstName").send_keys("Test")
        driver.find_element(By.ID, "lastName").send_keys("Automatise")
        driver.find_element(By.ID, "email").send_keys("jean.dupont@email.com")
        driver.find_element(By.ID, "password").send_keys("Password123!")

        # Accepte les CGU
        driver.find_element(By.CSS_SELECTOR, ".form-checkbox > input:nth-child(1)").click()

        # Soumet le formulaire
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        print("Utilisateur créé avec succès !")
    except NoSuchElementException as e:
        print(f"Erreur : Impossible de trouver un élément du formulaire. {e}")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    clean_and_restart_docker()
    create_user_with_selenium()
    print("Setup terminé avec succès !")
