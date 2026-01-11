import subprocess
import time


def clean_and_restart_docker():
        # Arrête et supprime TOUS les conteneurs, réseaux et volumes définis dans docker-compose.yml
        subprocess.run(["docker", "compose", "down", "-v"], check=True)

        # Relance les conteneurs en reconstruisant les images
        subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)

        time.sleep(20)