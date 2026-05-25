import os
import re
import sys
from datetime import datetime
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.scraper_utils import make_driver
from domain.models.equipo import Equipo
from domain.models.partido import Partido
from domain.models.temporada import Temporada


_COMP_RE = re.compile(r"/comps/(\d+)/")


def _safe_text(element) -> Optional[str]:
    if not element:
        return None

    try:
        return (element.get_attribute("textContent") or "").strip()
    except Exception:
        return None


def _parse_score_text(text: str) -> Tuple[Optional[int], Optional[int]]:
    text = (text or "").strip().replace("–", "-")
    parts = [part.strip() for part in text.split("-")]

    if len(parts) == 2 and all(part.isdigit() for part in parts):
        return int(parts[0]), int(parts[1])

    return None, None


def _team_from_cell(row, data_stat: str) -> Optional[Equipo]:
    try:
        cell = row.find_element(By.CSS_SELECTOR, f'td[data-stat="{data_stat}"]')
        link = cell.find_element(By.TAG_NAME, "a")

        nombre = _safe_text(link)
        href = link.get_attribute("href") or ""

        match = re.search(r"/(squads|equipos)/([A-Za-z0-9]+)/", href)
        equipo_id = match.group(2) if match else None
        abreviatura = re.sub(r"[^A-Za-z0-9]", "", nombre)[:3].upper() if nombre else "UNK"

        if not (equipo_id and nombre):
            return None

        return Equipo(equipo_id=equipo_id, nombre=nombre, abreviatura=abreviatura)
    except Exception:
        return None


def _extract_date(row, last_date: Optional[datetime]) -> Optional[datetime]:
    try:
        date_cell = row.find_element(By.CSS_SELECTOR, 'td[data-stat="date"]')
        csk = date_cell.get_attribute("csk")

        if csk:
            try:
                return datetime.strptime(csk, "%Y-%m-%d")
            except Exception:
                pass

        text = _safe_text(date_cell)
        if text:
            for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                try:
                    return datetime.strptime(text, fmt)
                except Exception:
                    continue
    except Exception:
        pass

    return last_date


def _row_is_header_or_spacer(row) -> bool:
    row_class = (row.get_attribute("class") or "").lower()

    if "thead" in row_class or "spacer" in row_class:
        return True

    try:
        if not row.find_elements(By.TAG_NAME, "td"):
            return True
    except Exception:
        return True

    return False


def _comp_id_from_url(url: str) -> int:
    match = _COMP_RE.search(url or "")
    if not match:
        raise ValueError(f"No se pudo extraer competicion_id desde la URL: {url}")

    return int(match.group(1))


def _extract_matches_from_table(table, *, season: str, comp_id: int, limit: Optional[int]):
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    partidos: List[Partido] = []
    equipos_map: dict[str, Equipo] = {}

    try:
        anio_inicio, anio_fin = map(int, season.split("-"))
    except Exception:
        anio_inicio, anio_fin = 0, 0

    temporada = Temporada(
        temporada_id=season,
        año_inicio=anio_inicio,
        año_fin=anio_fin,
        competicion_id=comp_id,
    )

    last_date: Optional[datetime] = None

    for index, row in enumerate(rows, start=1):
        if limit is not None and index > limit:
            break

        if _row_is_header_or_spacer(row):
            continue

        equipo_local = _team_from_cell(row, "home_team")
        equipo_visitante = _team_from_cell(row, "away_team")

        fecha = _extract_date(row, last_date)
        last_date = fecha or last_date

        match_id = None
        goles_local = None
        goles_visitante = None

        for data_stat in ("match_report", "score"):
            try:
                cell = row.find_element(By.CSS_SELECTOR, f'td[data-stat="{data_stat}"]')
                link = cell.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href") or ""

                if "/matches/" in href or "/partidos/" in href:
                    match_id = urlparse(href).path.split("/")[-2]

                    if data_stat == "score":
                        gl, gv = _parse_score_text(link.text)
                        goles_local, goles_visitante = gl, gv

                    break
            except Exception:
                continue

        if not match_id or goles_local is None or goles_visitante is None:
            try:
                cell = row.find_element(By.CSS_SELECTOR, 'td[data-stat="score"]')

                if goles_local is None or goles_visitante is None:
                    try:
                        link = cell.find_element(By.TAG_NAME, "a")
                        gl, gv = _parse_score_text(link.text)

                        if goles_local is None:
                            goles_local = gl
                        if goles_visitante is None:
                            goles_visitante = gv

                        if not match_id:
                            href = link.get_attribute("href") or ""
                            if "/matches/" in href or "/partidos/" in href:
                                match_id = urlparse(href).path.split("/")[-2]
                    except Exception:
                        pass

                if goles_local is None or goles_visitante is None:
                    csk_score = cell.get_attribute("csk")
                    if csk_score:
                        gl, gv = _parse_score_text(csk_score)
                        if goles_local is None:
                            goles_local = gl
                        if goles_visitante is None:
                            goles_visitante = gv

                if goles_local is None or goles_visitante is None:
                    gl, gv = _parse_score_text(cell.text)
                    if goles_local is None:
                        goles_local = gl
                    if goles_visitante is None:
                        goles_visitante = gv
            except Exception:
                pass

        if not match_id or not (equipo_local and equipo_visitante):
            continue

        if equipo_local.equipo_id not in equipos_map:
            equipos_map[equipo_local.equipo_id] = equipo_local

        if equipo_visitante.equipo_id not in equipos_map:
            equipos_map[equipo_visitante.equipo_id] = equipo_visitante

        partidos.append(
            Partido(
                partido_id=match_id,
                fecha=fecha,
                equipo_local_id=equipo_local.equipo_id,
                equipo_visitante_id=equipo_visitante.equipo_id,
                goles_local=goles_local,
                goles_visitante=goles_visitante,
                temporada_id=season,
                competicion_id=comp_id,
            )
        )

    partidosVistos = set()
    partidosSinDuplicados = []

    for partido in partidos:
        if partido.partido_id in partidosVistos:
            continue
        partidosVistos.add(partido.partido_id)
        partidosSinDuplicados.append(partido)

    equipos = list(equipos_map.values())
    return partidosSinDuplicados, equipos, temporada


def scrape_matches_from_season(url: str, *, season: str, headless: bool = True, limit: Optional[int] = None):
    comp_id = _comp_id_from_url(url)
    driver = make_driver(headless=headless)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 40)

        try:
            tables = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'table#sched, table[id^="sched"]')
                )
            )
        except TimeoutException:
            html = driver.page_source
            dump_path = os.path.join(os.path.dirname(__file__), "season_dump.html")

            with open(dump_path, "w", encoding="utf-8") as file:
                file.write(html)
            print(f"No se encontró la tabla de partidos. HTML guardado en: {dump_path}")
            print(f"Título de la página: {driver.title}")
            return [], [], Temporada( temporada_id=season, año_inicio=0, año_fin=0, competicion_id=comp_id)

        table = tables[0]
        partidos, equipos, temporada = _extract_matches_from_table(table, season=season, comp_id=comp_id, limit=limit)
        print(f"Tabla encontrada. Equipos extraídos: {len(equipos)}")
        print(f"Tabla encontrada. Partidos extraídos: {len(partidos)}")
        return partidos, equipos, temporada

    finally:
        try:
            driver.quit()
        except Exception:
            pass


def scrape_season(url: str, *, season: str,headless: bool = True, limit: Optional[int] = None):
    return scrape_matches_from_season( url=url, season=season, headless=headless, limit=limit)