import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from bs4 import BeautifulSoup
from infra.minio.minio_client import create_minio_client
from domain.models.partido import Partido


def scrape_partidos() -> list[Partido]:
    print("\n Accediendo al archivo HTML desde MinIO...")
    client = create_minio_client()
    obj = client.get_object("fbref", "partidos_2021_2022.html")
    html = obj.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    tabla = soup.find("table", {"id": "sched_2021-2022_9_1"})

    if not tabla:
        print(" No se encontró la tabla de partidos.")
        return []

    print(" Tabla encontrada en el HTML.")
    rows = tabla.find("tbody").find_all("tr")
    partidos = []

    for row in rows:
        if 'class' in row.attrs and "thead" in row['class']:
            continue

        cells = row.find_all("td")
        if not cells:
            continue

        fila = {}
        for cell in cells:
            data_stat = cell.get("data-stat")
            valor = cell.text.strip()
            fila[data_stat] = valor

            if data_stat == "score" and valor:
                goles = valor.replace("–", "-").split("-")
                if len(goles) == 2:
                    fila["home_team_score"] = goles[0].strip()
                    fila["away_team_score"] = goles[1].strip()

            if data_stat == "match_report":
                enlace = cell.find("a")
                if enlace and "/partidos/" in enlace.get("href", ""):
                    href = enlace.get("href")
                    fila["match_id"] = href.split("/")[5]
                    fila["match_url"] = f"{href}"

            if data_stat == "home_team" and valor:
                enlace = cell.find("a")
                if enlace and "equipos" in enlace.get("href", ""):
                    fila["home_team_id"] = enlace["href"].split("/")[3]
                    fila["home_team"] = enlace.text.strip()

            if data_stat == "away_team" and valor:
                enlace = cell.find("a")
                if enlace and "equipos" in enlace.get("href", ""):
                    fila["away_team_id"] = enlace["href"].split("/")[3]
                    fila["away_team"] = enlace.text.strip()

        if all(k in fila for k in ["date", "home_team_score", "away_team_score", "match_id"]):
            try:
                fecha = datetime.strptime(fila["date"], "%Y-%m-%d").date()
            except ValueError:
                continue

            partido = Partido(
                fecha=fecha,
                equipo_local_id=fila["home_team_id"],
                equipo_visitante_id=fila["away_team_id"],
                goles_local=int(fila["home_team_score"]),
                goles_visitante=int(fila["away_team_score"]),
                temporada_id=2021,
                competicion_id=9
            )
            partidos.append(partido)

    print(f"\n Se han extraído {len(partidos)} partidos correctamente desde MinIO.")
    return partidos

if __name__ == "__main__":
    partidos = scrape_partidos()
    for i, p in enumerate(partidos[:5], start=1):
        print(f"\n[{i}] {p.fecha} - {p.equipo_local_id} vs {p.equipo_visitante_id}")
        print(f"Marcador: {p.goles_local} - {p.goles_visitante}")
