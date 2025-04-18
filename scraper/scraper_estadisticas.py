import time
import random
import cloudscraper
from bs4 import BeautifulSoup

def scrape_estadisticas(partidos: list[dict]) -> list[dict]:
    scraper = cloudscraper.create_scraper()
    estadisticas = []

    for i, partido in enumerate(partidos, start=1):
        url = partido.get("match_url")
        match_id = partido.get("match_id")

        # print(f"\n[{i}] Accediendo a: {url}")
        response = scraper.get(url)
        if response.status_code != 200:
            # print(f"Error {response.status_code} al acceder a {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        datos = {"match_id": match_id}

        secciones = soup.find_all("tr")
        for seccion in secciones:
            th = seccion.find("th")
            if not th or not th.has_attr("colspan"):
                continue

            titulo = th.get_text(strip=True).lower()
            # print(f"Sección detectada: {titulo}")

            if "posesión" in titulo:
                tds = seccion.find_next_siblings("tr", limit=1)[0].find_all("td")
                try:
                    datos["posesion_local"] = float(tds[0].get_text(strip=True).replace("%", ""))
                    datos["posesion_visitante"] = float(tds[1].get_text(strip=True).replace("%", ""))
                    # print(f"Posesión: Local {datos['posesion_local']}% | Visitante {datos['posesion_visitante']}%")
                except:
                    pass

            elif "disparos a puerta" in titulo:
                siguiente = seccion.find_next_siblings("tr", limit=1)
                if siguiente:
                    divs_local = siguiente[0].find_all("td")[0].find_all("div")
                    divs_visitante = siguiente[0].find_all("td")[1].find_all("div")
                    try:
                        texto_local = divs_local[0].get_text(strip=True).lower()
                        datos["tiros_puerta_local"] = int(texto_local.split("of")[0].strip())
                        datos["tiros_local"] = int(texto_local.split("of")[1].split("—")[0].strip())
                        texto_visitante = divs_visitante[0].get_text(strip=True).lower()
                        datos["tiros_puerta_visitante"] = int(texto_visitante.split("of")[0].split()[-1])
                        datos["tiros_visitante"] = int(texto_visitante.split("of")[1].strip())
                        # print(f"Tiros totales: Local {datos['tiros_local']} | Visitante {datos['tiros_visitante']}")
                        # print(f"Tiros a puerta: Local {datos['tiros_puerta_local']} | Visitante {datos['tiros_puerta_visitante']}")
                    except:
                        pass

            elif "tarjetas" in titulo:
                siguiente = seccion.find_next_siblings("tr", limit=1)
                if siguiente:
                    tds = siguiente[0].find_all("td")
                    try:
                        amarillas_local = len(tds[0].find_all("span", class_="yellow_card"))
                        amarillas_visitante = len(tds[1].find_all("span", class_="yellow_card"))
                        rojas_local = len(tds[0].find_all("span", class_="red_card"))
                        rojas_visitante = len(tds[1].find_all("span", class_="red_card"))

                        datos["amarillas_local"] = amarillas_local
                        datos["rojas_local"] = rojas_local
                        datos["amarillas_visitante"] = amarillas_visitante
                        datos["rojas_visitante"] = rojas_visitante

                        # print(f"Amarillas -> L: {amarillas_local} | V: {amarillas_visitante}")
                        # print(f"Rojas -> L: {rojas_local} | V: {rojas_visitante}")
                    except:
                        pass

        # print(f"Diccionario final para {match_id}: {datos}")
        estadisticas.append(datos)
        time.sleep(random.uniform(1.5, 2.5))  # Anti-bloqueo

    return estadisticas

# Modo prueba para comprobar se extrae correctamente estadisticas
"""
if __name__ == "__main__":
    partidos_prueba = [
        {"match_id": "e62f6e78", "match_url": "https://fbref.com/es/partidos/e62f6e78/Crystal-Palace-Arsenal-Agosto-5-2022-Premier-League"},
        {"match_id": "6713c1dc", "match_url": "https://fbref.com/es/partidos/6713c1dc/Fulham-Liverpool-Agosto-6-2022-Premier-League"}
    ]
    estadisticas = scrape_estadisticas(partidos_prueba)
    for i, e in enumerate(estadisticas, start=1):
        print(f"\n[{i}] Estadísticas para partido {e['match_id']}")
        for k, v in e.items():
            if k != "match_id":
                print(f"   {k}: {v}")
"""
