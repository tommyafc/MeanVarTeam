from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")              # obbligatorio su Render
    options.add_argument("--disable-dev-shm-usage")   # importantissimo
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.binary_location = "/usr/bin/chromium-browser"  # ← chiave!

    chromedriver_path = "/usr/bin/chromedriver"   # o /usr/lib/chromium-browser/chromedriver

    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"Chromedriver NON trovato: {chromedriver_path}. Controlla log build.")

    service = Service(executable_path=chromedriver_path)

    # Disabilita Selenium Manager (non vogliamo download automatico)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
