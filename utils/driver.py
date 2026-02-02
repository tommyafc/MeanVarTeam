from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
    options.binary_location = "/usr/bin/chromium-browser"   # o prova "/usr/lib/chromium-browser/chromium-browser" se log dice così

    # Prova percorsi multipli per chromedriver
    possible_paths = [
        "/usr/bin/chromedriver",
        "/usr/lib/chromium-browser/chromedriver",
        "/usr/local/bin/chromedriver"
    ]

    chromedriver_path = None
    for path in possible_paths:
        if os.path.exists(path):
            chromedriver_path = path
            break

    if chromedriver_path is None:
        raise FileNotFoundError(
            f"Chromedriver NON trovato in nessuno dei percorsi: {possible_paths}. "
            "Controlla i log di build per vedere dove è installato."
        )

    print(f"Usando chromedriver da: {chromedriver_path}")  # ← utile nei log runtime

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
