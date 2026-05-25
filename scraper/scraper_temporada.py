import os
import sys

from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from domain.models.competicion import Competicion
from domain.models.temporada import Temporada
from infra.minio.minio_client import create_minio_client


def scrape_temporadas() -> tuple[list[Temporada], list[Competicion]]:
    temporadas = []
    competiciones = []

    client = create_minio_client()
    response = client.get_object("fbref", "temporadas.html")
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    tabla = soup.find("table", {"id": "seasons"})

    if tabla is None:
        raise ValueError("No se encontró la tabla de temporadas en el HTML.")

    tbody = tabla.find("tbody")
    if tbody is None:
        raise ValueError("No se encontró el cuerpo de la tabla de temporadas.")

    for fila in tbody.find_all("tr"):
        celdas = fila.find_all("td")
        if not celdas:
            continue

        try:
            year_id = fila.find("th", {"data-stat": "year_id"})
            if year_id is None:
                continue

            year_text = year_id.get_text(strip=True).replace("–", "-")
            año_inicio, año_fin = map(int, year_text.split("-"))
            temporada_id = year_text

            enlace = year_id.find("a")
            if not enlace:
                continue

            href = enlace.get("href", "")
            partes = href.split("/")
            if len(partes) < 6:
                continue

            competicion_id = int(partes[5])

            celda_liga = fila.find("td", {"data-stat": "league_name"})
            if celda_liga is None:
                continue

            nombre = celda_liga.get_text(strip=True)
            abreviatura = nombre[:3].upper()

            temporada = Temporada(
                temporada_id=temporada_id,
                año_inicio=año_inicio,
                año_fin=año_fin,
                competicion_id=competicion_id,
            )

            competicion = Competicion(
                competicion_id=competicion_id,
                nombre=nombre,
                abreviatura=abreviatura,
            )

            temporadas.append(temporada)

            if all(c.competicion_id != competicion_id for c in competiciones):
                competiciones.append(competicion)

        except Exception as e:
            print(f"Error procesando una fila de temporadas: {e}")

    return temporadas, competiciones


if __name__ == "__main__":
    temporadas, competiciones = scrape_temporadas()

    print("\nTEMPORADAS EXTRAÍDAS:")
    for temporada in temporadas:
        print(
            f"Temporada ID: {temporada.temporada_id}, "
            f"Inicio: {temporada.año_inicio}, "
            f"Fin: {temporada.año_fin}, "
            f"Competición ID: {temporada.competicion_id}"
        )

    print("\nCOMPETICIONES EXTRAÍDAS:")
    for competicion in competiciones:
        print(
            f"Competición ID: {competicion.competicion_id}, "
            f"Nombre: {competicion.nombre}, "
            f"Abreviatura: {competicion.abreviatura}"
        )

    print(f"\nTotal: {len(temporadas)} temporadas | {len(competiciones)} competiciones.")