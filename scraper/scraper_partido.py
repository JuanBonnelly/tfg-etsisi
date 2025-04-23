import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from bs4 import BeautifulSoup
from infra.minio.minio_client import create_minio_client
from domain.models.partido import Partido
from domain.models.equipo import Equipo

equipos_extraidos = {}
def scrape_partidos() -> tuple[list[Partido], list[Equipo]]:
    client = create_minio_client()
    obj = client.get_object("fbref", "partidos_2021_2022.html")
    html = obj.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    tabla = soup.find("table", {"id": "sched_2021-2022_9_1"})

    if not tabla:
        print(" No se encontró la tabla de partidos.")
        return [], []

    rows = tabla.find("tbody").find_all("tr")
    partidos = []
    #equipos_extraidos = {}

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
                    home_id = enlace["href"].split("/")[5]
                    home_name = enlace.text.strip()
                    fila["home_team_id"] = home_id
                    fila["home_team"] = home_name

                    if home_id not in equipos_extraidos:
                        equipo = Equipo(
                            equipo_id= home_id,  
                            nombre=home_name,
                            abreviatura=home_name[:3].upper()
                        )
                        equipos_extraidos[home_id] = equipo

            if data_stat == "away_team" and valor:
                enlace = cell.find("a")
                if enlace and "equipos" in enlace.get("href", ""):
                    away_id = enlace["href"].split("/")[5]
                    away_name = enlace.text.strip()
                    fila["away_team_id"] = away_id
                    fila["away_team"] = away_name

                    if away_id not in equipos_extraidos:
                        equipo = Equipo(
                            equipo_id= away_id,
                            nombre=away_name,
                            abreviatura=away_name[:3].upper()
                        )
                        equipos_extraidos[away_id] = equipo

        if all(k in fila for k in ["date", "home_team_score", "away_team_score", "match_id"]):
            try:
                fecha = datetime.strptime(fila["date"], "%Y-%m-%d").date()
            except ValueError:
                continue

            partido = Partido(
                partido_id = fila["match_id"],
                fecha=fecha,
                equipo_local_id=fila["home_team_id"],
                equipo_visitante_id=fila["away_team_id"],
                goles_local=int(fila["home_team_score"]),
                goles_visitante=int(fila["away_team_score"]),
                temporada_id=2021,
                competicion_id=9
            )
            partidos.append(partido)

    print(f"\n Se han extraído {len(partidos)} partidos y {len(equipos_extraidos)} equipos.")
    return partidos, list(equipos_extraidos.values())


if __name__ == "__main__":
    partidos, equipos = scrape_partidos()

    print("\n Primeros 5 partidos:")
    for i, p in enumerate(partidos[:40], start=1):
        print(f"[{i}] {p.fecha} - {p.equipo_local_id} vs {p.equipo_visitante_id} | {p.goles_local}-{p.goles_visitante}-----{p.partido_id}")

    print("\n Equipos extraídos:")
    for e in equipos:
        print(f"ID: {e.equipo_id}, Nombre: {e.nombre}, Abreviatura: {e.abreviatura}")


__all__ = ["scrape_partidos", "equipos_extraidos"]
