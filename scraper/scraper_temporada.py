import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bs4 import BeautifulSoup
from infra.minio.minio_client import create_minio_client

from domain.models.temporada import Temporada
from domain.models.competicion import Competicion

def scrape_temporadas() -> tuple[list[Temporada], list[Competicion]]:
    temporadas = []
    competiciones = []
    client = create_minio_client()
    obj = client.get_object("fbref", "temporadas.html")
    html = obj.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    tabla = soup.find("table", {"id": "seasons"})

    for fila in tabla.find("tbody").find_all("tr"):
        celdas = fila.find_all("td")
        if not celdas:
            continue

        try:
            year_id = fila.find("th", {"data-stat": "year_id"})
            year_text = year_id.get_text(strip=True).replace("–", "-")
            año_inicio, año_fin = map(int, year_text.split("-"))
            temporada_id = year_text  

            enlace = year_id.find("a")
            if not enlace:
                continue

            href = enlace["href"]
            parts = href.split("/")
            if len(parts) < 6:
                print(" href mal formado:", href)
                continue

            competicion_id = int(parts[5])

            league_cell = fila.find("td", {"data-stat": "league_name"})
            nombre = league_cell.get_text(strip=True)
            abreviatura = nombre[:3].upper()

            temporada = Temporada(
                temporada_id=temporada_id,
                año_inicio=año_inicio,
                año_fin=año_fin,
                competicion_id=competicion_id
            )
            competicion = Competicion(
                competicion_id=competicion_id,
                nombre=nombre,
                abreviatura=abreviatura
            )

            temporadas.append(temporada)
            if all(c.competicion_id != competicion_id for c in competiciones):
                competiciones.append(competicion)

        except Exception as e:
            print(f" Error procesando fila:\n{fila}\nError: {e}\n")

    return temporadas, competiciones

if __name__ == "__main__":
    temporadas, competiciones = scrape_temporadas()

    print("\n TEMPORADAS EXTRAÍDAS:")
    for t in temporadas:
        print(f"Temporada ID: {t.temporada_id}, Inicio: {t.año_inicio}, Fin: {t.año_fin}, Competición ID: {t.competicion_id}")

    print("\n COMPETICIONES EXTRAÍDAS:")
    for c in competiciones:
        print(f"Competición ID: {c.competicion_id}, Nombre: {c.nombre}, Abreviatura: {c.abreviatura}")

    print(f"\n Total: {len(temporadas)} temporadas | {len(competiciones)} competiciones.")
