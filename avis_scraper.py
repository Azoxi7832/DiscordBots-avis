import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

avis_envoyes = set()

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def get_reviews(driver, url):
    driver.get(url)
    time.sleep(3)

    avis = []
    try:
        avis_elements = driver.find_elements(By.CSS_SELECTOR, 'div[jscontroller="e6Mltc"]')
        for el in avis_elements:
            nom = el.find_element(By.CSS_SELECTOR, 'div.d4r55').text
            note = float(el.find_element(By.CSS_SELECTOR, 'span.KkqJbd').get_attribute("aria-label").split(" ")[0])
            commentaire = el.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text or "Aucun commentaire"
            timestamp = datetime.datetime.now().timestamp()

            id_unique = f"{nom}-{commentaire[:20]}"
            if id_unique not in avis_envoyes:
                avis_envoyes.add(id_unique)
                avis.append({
                    "nom": nom,
                    "note": note,
                    "commentaire": commentaire,
                    "timestamp": timestamp
                })
    except Exception as e:
        print(f"[Scraper] Erreur : {e}")
    return avis
