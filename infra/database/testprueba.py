import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import csv
from datetime import datetime
from infra.database.mysql_connect import get_session
from domain.models.competicion import Competicion
from domain.models.equipo import Equipo
from domain.models.temporada import Temporada
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido

# Rutas de los CSV
csv_competitions = "data/datosFbref/fbref_competitions_202505141101.csv"
csv_teams = "data/datosFbref/fbref_teams_202505141059.csv"
csv_seasons = "data/datosFbref/fbref_seasons_202505141100.csv"
csv_matches = "data/datosFbref/fbref_matches_202505141101.csv"

def abreviar_equipo(nombre):
    if not nombre or not nombre.strip():
        return "UNK"
    palabras = nombre.strip().split()
    if len(nombre) <= 4:
        return nombre.upper()
    elif len(palabras) == 1:
        return nombre[:3].upper()
    else:
        abrev = ''.join(p[0].upper() for p in palabras if p.lower() not in ['fc', 'cf', 'cd', 'de'])
        return abrev if abrev else "UNK"

def main():
    session = get_session()

    #  Insertar COMPETICIONES (solo última ocurrencia por ID)
    with open(csv_competitions, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        ultima_competicion = {}
        for row in reader:
            comp_id = row["competition_id"]
            ultima_competicion[comp_id] = row

        for comp_id, row in ultima_competicion.items():
            nombre = row["competition_name"]
            abreviatura = abreviar_equipo(nombre)
            competicion = Competicion(
                competicion_id=comp_id,
                nombre=nombre,
                abreviatura=abreviatura
            )
            session.add(competicion)

    # 🏟 Insertar EQUIPOS
    with open(csv_teams, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nombre = row["name"]
            equipo = Equipo(
                equipo_id=row["team_id"],
                nombre=nombre,
                abreviatura=abreviar_equipo(nombre)
            )
            session.add(equipo)

    #  Insertar TEMPORADAS
    with open(csv_seasons, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            temporada = Temporada(
                competicion_id=row["competition_id"],
                temporada_id=row["season"],
                año_inicio=row["starting_year"],
                año_fin=row["ending_year"]
            )
            session.add(temporada)

    #  Insertar PARTIDOS
    with open(csv_matches, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            partido = Partido(
                partido_id=row["match_id"],
                fecha=datetime.fromisoformat(row["start_datetime"]),
                equipo_local_id=row["home_team_id"],
                equipo_visitante_id=row["away_team_id"],
                goles_local=int(row["home_goals"]),
                goles_visitante=int(row["away_goals"]),
                competicion_id=row["competition_id"],
                temporada_id=row["season"]
            )
            session.add(partido)

    #  Guardar cambios
    session.commit()
    session.close()
    print(" Todos los datos han sido cargados correctamente.")

if __name__ == "__main__":
    main()
