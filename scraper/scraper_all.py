import sys
import os
import json
import shutil
import time
import random
import multiprocessing as mp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.scraper_partido import scrape_season

# Script principal del scraping.
# Obtiene partidos y estadísticas de FBref y los guarda en BD o en ficheros JSONL.

SEASON = ["2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"]

COMPETITIONS = [
    {"id": 9, "name": "Premier-League"},
    {"id": 12, "name": "La-Liga"},
]

ROW_LIMIT = None
HEADLESS = False

# Disco externo 
EXTERNAL_BASE = r"D:\scraper-out"          
EXTERNAL_TMP  = r"D:\chrome-scraper-cache" 

CHECK_DISK_EVERY = 200  #comprobacion cada 200 partidos miramos espacio sobre disco
MIN_FREE_GB = 1.5       #minimo 1.5GB libre
RETRIES_STATS = 2       #reintentos por partido 

SLEEP_BETWEEN_MATCHES = (0.20, 0.60)  
PER_MATCH_TIMEOUT_S = 60 

# Configuacion modos BD/Simulacion
DRY_RUN = False
DB_ENABLED = False
try:
    if not DRY_RUN:
        from infra.database.mysql_connect import get_session
        from domain.models.competicion import Competicion
        from domain.models.temporada import Temporada
        from domain.models.equipo import Equipo
        from domain.models.partido import Partido
        from domain.models.estadisticas_partido import EstadisticasPartido

        DB_ENABLED = True
except Exception as e:
    print(f"No se pudieron importar módulos de BD: {e}")


def ensure_dirs():
    os.makedirs(EXTERNAL_BASE, exist_ok=True)

    if EXTERNAL_TMP:
        os.makedirs(EXTERNAL_TMP, exist_ok=True)
        os.environ["TMPDIR"] = EXTERNAL_TMP
        os.environ["TEMP"] = EXTERNAL_TMP
        os.environ["TMP"] = EXTERNAL_TMP
        os.environ["CHROME_CACHE_DIR"] = os.path.join(EXTERNAL_TMP, "cache")
        os.makedirs(os.environ["CHROME_CACHE_DIR"], exist_ok=True)


def out_file(entity: str):
    return os.path.join(EXTERNAL_BASE, f"{entity}.jsonl")


def ids_file(name: str):
    return os.path.join(EXTERNAL_BASE, f"{name}_ids.txt")


def write_jsonl(path: str, obj: dict):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def append_line(path: str, line: str):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())


def read_ids(path: str) -> set:
    if not os.path.exists(path):
        return set()

    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def check_disk_free_gb(path: str) -> float:
    try:
        usage = shutil.disk_usage(path)
        return usage.free / (1024 ** 3)
    except Exception:
        return 9999.0


def _estadisticas_worker(match_id, queue):
    from scraper.scraper_estadisticas import scrape_estadisticas

    try:
        result = scrape_estadisticas(match_id)
        queue.put(result)
    except Exception:
        queue.put(None)


def scrape_estadisticas_with_timeout(match_id: str, timeout_s: int = 60):
    ctx = mp.get_context("spawn")
    queue = ctx.Queue(maxsize=1)
    process = ctx.Process(target=_estadisticas_worker, args=(match_id, queue), daemon=True)
    process.start()
    process.join(timeout_s)

    if process.is_alive():
        try:
            process.terminate()
        except Exception:
            pass

        try:
            process.join(3)
        except Exception:
            pass

        return None

    try:
        return queue.get_nowait()
    except Exception:
        return None


def sim_guardar_competicion(comp):
    rec = {"comp_id": comp["id"], "name": comp["name"]}
    write_jsonl(out_file("competicion"), rec)
    print(f"Insertamos competición: {comp['id']} - {comp['name']}")


def sim_guardar_temporada(temporada):
    if not temporada:
        return

    rec = {
        "temporada_id": temporada.temporada_id,
        "anio_inicio": temporada.año_inicio,
        "anio_fin": temporada.año_fin,
    }
    write_jsonl(out_file("temporada"), rec)
    print(f"Insertamos temporada: {temporada.temporada_id} ({temporada.año_inicio}-{temporada.año_fin})")


def sim_guardar_equipos(equipos):
    path = out_file("equipo")

    for equipo in equipos:
        write_jsonl(
            path,
            {
                "equipo_id": equipo.equipo_id,
                "nombre": equipo.nombre,
                "abreviatura": equipo.abreviatura,
            },
        )

    for equipo in equipos[:5]:
        print(f"Insertamos equipo: {equipo.equipo_id} - {equipo.nombre} ({equipo.abreviatura})")

    if len(equipos) > 5:
        print(f"Hay {len(equipos) - 5} equipos más")


def sim_guardar_partidos(partidos, team_names):
    path = out_file("partido")

    for partido in partidos:
        rec = {
            "partido_id": partido.partido_id,
            "fecha": partido.fecha.strftime("%Y-%m-%d") if partido.fecha else None,
            "equipo_local_id": partido.equipo_local_id,
            "equipo_visitante_id": partido.equipo_visitante_id,
            "goles_local": partido.goles_local,
            "goles_visitante": partido.goles_visitante,
            "temporada_id": partido.temporada_id,
            "competicion_id": partido.competicion_id,
            "equipo_local_nombre": team_names.get(partido.equipo_local_id, None),
            "equipo_visitante_nombre": team_names.get(partido.equipo_visitante_id, None),
        }
        write_jsonl(path, rec)

    for partido in partidos[:5]:
        fecha_txt = partido.fecha.strftime("%Y-%m-%d") if partido.fecha else "NA"
        local = team_names.get(partido.equipo_local_id, partido.equipo_local_id)
        visitante = team_names.get(partido.equipo_visitante_id, partido.equipo_visitante_id)
        print(
            f"Insertamos partido: {partido.partido_id} | {fecha_txt} | "
            f"{local} ({partido.equipo_local_id}) vs {visitante} ({partido.equipo_visitante_id}) "
            f"{partido.goles_local}-{partido.goles_visitante} | temp={partido.temporada_id} comp={partido.competicion_id}"
        )

    if len(partidos) > 5:
        print(f"Hay {len(partidos) - 5} partidos más")


def sim_guardar_estadisticas(match_id, stats):
    rec = {"match_id": match_id, **stats}
    write_jsonl(out_file("estadisticas_partido"), rec)
    print(f"Insertamos estadísticas: {match_id} -> {stats}")


def db_upsert_competicion(session, comp_dict):
    comp_id = comp_dict["id"]
    competicion = session.query(Competicion).filter_by(competicion_id=comp_id).one_or_none()

    nombre = comp_dict["name"].replace("-", " ")
    abreviatura = comp_dict["name"][:3].upper()

    if competicion is None:
        competicion = Competicion(
            competicion_id=comp_id,
            nombre=nombre,
            abreviatura=abreviatura,
        )
        session.add(competicion)
    else:
        competicion.nombre = nombre
        competicion.abreviatura = abreviatura


def db_upsert_temporada(session, temporada):
    session.merge(temporada)


def db_upsert_equipo(session, equipo):
    session.merge(equipo)


def db_upsert_partido(session, partido):
    session.merge(partido)


def db_upsert_stats(session, match_id, stats: dict):
    estadisticas = session.query(EstadisticasPartido).filter_by(partido_id=match_id).one_or_none()

    if estadisticas is None:
        estadisticas = EstadisticasPartido(partido_id=match_id)
        session.add(estadisticas)

    for key, value in stats.items():
        if hasattr(estadisticas, key):
            setattr(estadisticas, key, value)


def main():
    ensure_dirs()

    if DB_ENABLED:
        with get_session() as session:
            for comp in COMPETITIONS:
                db_upsert_competicion(session, comp)
            session.commit()
    else:
        for comp in COMPETITIONS:
            sim_guardar_competicion(comp)

    processed_ids_path = ids_file("processed_stats")
    processed = read_ids(processed_ids_path)

    total_stats_acum = 0

    for comp in COMPETITIONS:
        comp_id = comp["id"]
        comp_name = comp["name"]
        print(f"\n=== Scrapeando competición: {comp_name} (ID: {comp_id}) ===")

        for season in SEASON:
            print(f"\n=== Temporada: {season} ===")
            url = f"https://fbref.com/en/comps/{comp_id}/{season}/schedule/{season}-{comp_name}-Scores-and-Fixtures"

            try:
                partidos, equipos, temporada = scrape_season(
                    url=url,
                    headless=HEADLESS,
                    season=season,
                    limit=ROW_LIMIT,
                )
                print(f"Equipos extraídos: {len(equipos)}")
                print(f"Partidos extraídos: {len(partidos)}")
                if partidos:
                    print(f"Primer partido extraído: {partidos[0].partido_id}")
            except Exception as e:
                print(f"Fallo scrape_season {season}-{comp_name}: {e}")
                continue

            uniq = len({partido.partido_id for partido in partidos if partido.partido_id})
            if uniq != len(partidos):
                print(f"Duplicados posibles: total={len(partidos)} únicos={uniq}")

            team_names = {
                equipo.equipo_id: equipo.nombre
                for equipo in equipos
                if getattr(equipo, "equipo_id", None)
            }

            if DB_ENABLED:
                try:
                    with get_session() as session:
                        if temporada:
                            temporada.competicion_id = comp_id
                            db_upsert_temporada(session, temporada)

                        for equipo in equipos:
                            db_upsert_equipo(session, equipo)

                        for partido in partidos:
                            db_upsert_partido(session, partido)

                        session.commit()
                except Exception as e:
                    print(f"Error temporada, equipos y partidos en BD: {e}")
            else:
                sim_guardar_temporada(temporada)
                print(f"Equipos encontrados: {len(equipos)}")
                print(f"Partidos encontrados: {len(partidos)}")
                sim_guardar_equipos(equipos)
                sim_guardar_partidos(partidos, team_names)

            diferidos = []
            procesados_temporada = 0

            for partido in partidos:
                if not partido.partido_id:
                    continue
                if partido.partido_id in processed:
                    continue

                if (total_stats_acum % CHECK_DISK_EVERY) == 0:
                    free_gb = check_disk_free_gb(EXTERNAL_BASE)
                    if free_gb < MIN_FREE_GB:
                        print(f"Poco espacio en {EXTERNAL_BASE}: {free_gb:.2f} GB libres.")

                print(f"\nScrapeando estadísticas de partido: {partido.partido_id}")
                success = False

                for attempt in range(RETRIES_STATS + 1):
                    try:
                        stats = scrape_estadisticas_with_timeout(
                            partido.partido_id,
                            timeout_s=PER_MATCH_TIMEOUT_S,
                        )
                        if stats is None:
                            raise RuntimeError("stats = None / timeout")

                        if DB_ENABLED:
                            with get_session() as session:
                                db_upsert_stats(session, partido.partido_id, stats)
                                session.commit()
                        else:
                            sim_guardar_estadisticas(partido.partido_id, stats)

                        append_line(processed_ids_path, partido.partido_id)
                        processed.add(partido.partido_id)

                        total_stats_acum += 1
                        procesados_temporada += 1
                        success = True
                        break
                    except Exception as e:
                        print(
                            f"Fallo stats {partido.partido_id} intento "
                            f"{attempt + 1}/{RETRIES_STATS + 1}: {e}"
                        )
                        time.sleep(1.2 * (attempt + 1))

                if not success:
                    diferidos.append(partido.partido_id)
                    print(f"Aplazado {partido.partido_id} para segunda pasada.")

                time.sleep(random.uniform(*SLEEP_BETWEEN_MATCHES))

            if diferidos:
                print(f"\nSegunda pasada: {len(diferidos)} partidos diferidos en {season} {comp_name}")

            still_failed = []

            for match_id in diferidos:
                print(f"Reintentando stats diferidas: {match_id}")
                ok = False

                for attempt in range(RETRIES_STATS + 1):
                    try:
                        stats = scrape_estadisticas_with_timeout(match_id, timeout_s=PER_MATCH_TIMEOUT_S)
                        if stats is None:
                            raise RuntimeError("stats = None / timeout")

                        if DB_ENABLED:
                            with get_session() as session:
                                db_upsert_stats(session, match_id, stats)
                                session.commit()
                        else:
                            sim_guardar_estadisticas(match_id, stats)

                        append_line(processed_ids_path, match_id)
                        processed.add(match_id)

                        total_stats_acum += 1
                        procesados_temporada += 1
                        ok = True
                        break
                    except Exception as e:
                        print(
                            f"Fallo en segunda pasada {match_id} intento "
                            f"{attempt + 1}/{RETRIES_STATS + 1}: {e}"
                        )
                        time.sleep(1.2 * (attempt + 1))

                if not ok:
                    still_failed.append(match_id)

            if still_failed:
                missed_path = ids_file(f"missed_stats_{comp_id}_{season.replace('-', '')}")
                for match_id in still_failed:
                    append_line(missed_path, match_id)

                print(f"{len(still_failed)} partidos siguen fallando. Listados en: {missed_path}")

            print(
                f"\n{comp_name} {season}: "
                f"OK en temporada={procesados_temporada}, acumuladas={total_stats_acum}"
            )

    print("\nScraping completado.")


if __name__ == "__main__":
    main()