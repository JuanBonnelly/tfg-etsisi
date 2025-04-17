import time
import random
import cloudscraper
from bs4 import BeautifulSoup

# === CONFIGURACIÓN ===
temporada_id = "2022-2023"
competicion_id = 9
nombre_competicion = "Premier-League"
url = f"https://fbref.com/es/comps/{competicion_id}/{temporada_id}/horario/Marcadores-y-partidos-de-{temporada_id}-{nombre_competicion}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

print(f"Scrapeando URL: {url}")
scraper = cloudscraper.create_scraper()
response = scraper.get(url, headers=headers)
print(f"Código de estado: {response.status_code}")

if response.status_code != 200:
    print("Error al acceder a la página.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
tabla = soup.find("table")

if not tabla:
    print("No se encontró la tabla de partidos.")
    exit()

rows = tabla.find("tbody").find_all("tr")
partidos = []

for i, row in enumerate(rows[:10]):
    cells = row.find_all("td")
    if not cells:
        continue  

    fila = {}

    # Extraer Fecha
    fecha = row.find("th", {"data-stat": "date"})
    fila["date"] = fecha.text.strip() if fecha else None

    for cell in cells:
        data_stat = cell.get("data-stat")
        fila[data_stat] = cell.text.strip()

        # Extraer marcador y goles
        if data_stat == "score" and cell.text.strip():
            marcador = cell.text.strip()
            goles = marcador.replace("–", "-").split("-")
            if len(goles) == 2:
                fila["home_team_score"] = goles[0].strip()
                fila["away_team_score"] = goles[1].strip()

        # Extraer enlace al detalle del partido
        if data_stat == "match_report":
            enlace = cell.find("a")
            if enlace and "/partidos/" in enlace.get("href"):
                href = enlace.get("href")
                fila["match_id"] = href.split("/")[3]
                fila["match_url"] = f"https://fbref.com{href}"

    # Guardamos solo si tenemos todos los datos clave
    if all(k in fila for k in ["home_team_score", "away_team_score", "match_id"]):
        partidos.append(fila)
    #time.sleep(random.uniform(1.5, 3.0))  lo activaremos cuando hagamos la extraccion de datos para simular comportamiento humano.
# === mostramos los datos para comprobacion sacamos correctamente los datos
for i, p in enumerate(partidos, start=1):
    print(f"\n[{i}] {p.get('date')} - {p.get('home_team')} vs {p.get('away_team')}")
    print(f"Marcador: {p.get('home_team_score')} - {p.get('away_team_score')}")
    print(f"ID partido: {p.get('match_id')}")
    print(f"URL detalle: {p.get('match_url')}")

print(f"\nSe han extraído {len(partidos)} partidos correctamente.")
