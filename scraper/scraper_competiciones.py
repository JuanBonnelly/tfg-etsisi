import os
import sys
from typing import Dict, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from domain.models.competicion import Competicion
from scraper.scraper_utils import make_driver



URL_COMPETITIONS = "https://fbref.com/en/comps/"


def scrape_competiciones(driver) -> List[Dict[str, str]]:
    driver.get(URL_COMPETITIONS)

    try:
        contenedor = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "div_popular_comps"))
        )
    except Exception as e:
        print("Error localizando el contenedor de competiciones")
        driver.save_screenshot("fallo_competiciones.png")
        raise e

    links = contenedor.find_elements(By.TAG_NAME, "a")
    competiciones: List[Dict[str, str]] = []

    for link in links:
        try:
            href = link.get_attribute("href")
            if "/comps/" not in href:
                continue

            partes = href.split("/")
            comp_id = partes[5] 

            img = link.find_element(By.TAG_NAME, "img")
            nombre = img.get_attribute("data-tip")  

            competiciones.append({
                "id": comp_id,
                "nombre": nombre,
                "abreviatura": nombre[:3].upper() if nombre else "UNK",
                "url": href
            })
        except Exception:
            continue

    return competiciones


def scrape_competicion(comp_id: int, headless: bool = True) -> Competicion:
    driver = make_driver(headless=headless)
    try:
        competiciones = scrape_competiciones(driver)
        for c in competiciones:
            if str(c["id"]) == str(comp_id):
                return Competicion(
                    competicion_id=str(c["id"]),
                    nombre=c["nombre"],
                    abreviatura=c["abreviatura"]
                )
        raise ValueError(f"No se encontró la competición con ID {comp_id}")
    finally:
        driver.quit()


