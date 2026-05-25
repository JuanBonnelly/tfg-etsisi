import os
import random
import re
import sys
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup, Comment
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.scraper_utils import make_driver


REQUEST_TIMEOUTS = (5, 12)
REQUEST_MAX_RETRIES = 3
REQUEST_BACKOFF = 1.6
SLEEP_AFTER_REQUEST = (0.15, 0.45)

SELENIUM_WAIT = 20
SLEEP_AFTER_LOAD = 0.8
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _to_number(text: str):
    if text is None:
        return None

    text = text.strip().lower().replace("%", "").replace(",", ".").replace("—", "-").replace("–", "-")

    match = re.match(r"^\s*(\d+)\s+of\s+(\d+)\s*$", text)
    if match:
        try:
            return float(match.group(1))
        except Exception:
            pass

    match_number = re.search(r"(\d+(\.\d+)?)", text)
    if match_number:
        try:
            return float(match_number.group(1))
        except Exception:
            pass

    try:
        return float(text)
    except Exception:
        try:
            return float(int(text))
        except Exception:
            return None


def _uncomment_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    parts = [html]

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if "<table" in comment or "<div" in comment:
            parts.append(str(comment))

    return "\n".join(parts)


def _find_section_row(soup: BeautifulSoup, title_contains: str):
    target = _norm(title_contains)

    for row in soup.find_all("tr"):
        header = row.find("th")
        if not header or not header.has_attr("colspan"):
            continue

        title = _norm(header.get_text(strip=True))
        if target in title:
            return row

    return None


def _two_tds_from_next_row(section_row):
    if not section_row:
        return None, None

    next_rows = section_row.find_next_siblings("tr", limit=1)
    if not next_rows:
        return None, None

    tds = next_rows[0].find_all("td")
    if len(tds) < 2:
        return None, None

    return tds[0], tds[1]


def _extract_td_value(td):
    if td is None:
        return None

    text = td.get_text(" ", strip=True)
    return _to_number(text)


def _fallback_cards_and_corners_full(soup: BeautifulSoup, out: dict):
    for row in soup.find_all("tr"):
        header = row.find("th")
        if not header or not header.has_attr("colspan"):
            continue

        title = _norm(header.get_text(strip=True))
        if "cards" in title:
            next_rows = row.find_next_siblings("tr", limit=1)
            if next_rows:
                tds = next_rows[0].find_all("td")
                try:
                    out["tarjetas_amarillas_local"] = out["tarjetas_amarillas_local"] or len(
                        tds[0].find_all("span", class_="yellow_card")
                    )
                    out["tarjetas_amarillas_visitante"] = out["tarjetas_amarillas_visitante"] or len(
                        tds[1].find_all("span", class_="yellow_card")
                    )
                    out["tarjetas_rojas_local"] = out["tarjetas_rojas_local"] or len(
                        tds[0].find_all("span", class_="red_card")
                    )
                    out["tarjetas_rojas_visitante"] = out["tarjetas_rojas_visitante"] or len(
                        tds[1].find_all("span", class_="red_card")
                    )
                except Exception:
                    pass
            break

    extras_div = soup.find("div", id="team_stats_extra")
    if extras_div:
        for row in extras_div.find_all("div"):
            header = row.find("div", string=lambda text: text and "Corners" in text)
            if header:
                corners_local_div = header.find_previous("div")
                corners_visitante_div = header.find_next("div")
                try:
                    if out["corners_local"] is None:
                        out["corners_local"] = int((corners_local_div.get_text(strip=True) or "0").split()[0])
                    if out["corners_visitante"] is None:
                        out["corners_visitante"] = int((corners_visitante_div.get_text(strip=True) or "0").split()[0])
                except Exception:
                    pass
                break


def _parse_stats_from_html(html: str) -> Optional[dict]:
    html_uncommented = _uncomment_html(html)
    soup = BeautifulSoup(html_uncommented, "html.parser")

    out = {
        "posesion_local": None,
        "posesion_visitante": None,
        "tiros_local": None,
        "tiros_visitante": None,
        "tiros_puerta_local": None,
        "tiros_puerta_visitante": None,
        "corners_local": None,
        "corners_visitante": None,
        "tarjetas_amarillas_local": None,
        "tarjetas_amarillas_visitante": None,
        "tarjetas_rojas_local": None,
        "tarjetas_rojas_visitante": None,
    }

    section_possession = _find_section_row(soup, "possession")
    td_local, td_visitante = _two_tds_from_next_row(section_possession)
    if td_local and td_visitante:
        out["posesion_local"] = _extract_td_value(td_local)
        out["posesion_visitante"] = _extract_td_value(td_visitante)

    section_shots_on_target = _find_section_row(soup, "shots on target")
    td_local, td_visitante = _two_tds_from_next_row(section_shots_on_target)
    if td_local and td_visitante:
        text_local = td_local.get_text(" ", strip=True).lower()
        text_visitante = td_visitante.get_text(" ", strip=True).lower()

        match_local = re.search(r"(\d+)\s+of\s+(\d+)", text_local)
        match_visitante = re.search(r"(\d+)\s+of\s+(\d+)", text_visitante)

        if match_local:
            out["tiros_puerta_local"] = float(match_local.group(1))
            out["tiros_local"] = float(match_local.group(2))
        else:
            out["tiros_puerta_local"] = _to_number(text_local)

        if match_visitante:
            out["tiros_puerta_visitante"] = float(match_visitante.group(1))
            out["tiros_visitante"] = float(match_visitante.group(2))
        else:
            out["tiros_puerta_visitante"] = _to_number(text_visitante)

    if out["tiros_local"] is None or out["tiros_visitante"] is None:
        section_shots = _find_section_row(soup, "shots")
        td_local, td_visitante = _two_tds_from_next_row(section_shots)
        if td_local and td_visitante:
            if out["tiros_local"] is None:
                out["tiros_local"] = _extract_td_value(td_local)
            if out["tiros_visitante"] is None:
                out["tiros_visitante"] = _extract_td_value(td_visitante)

    section_corners = _find_section_row(soup, "corner")
    td_local, td_visitante = _two_tds_from_next_row(section_corners)
    if td_local and td_visitante:
        out["corners_local"] = _extract_td_value(td_local)
        out["corners_visitante"] = _extract_td_value(td_visitante)

    _fallback_cards_and_corners_full(soup, out)

    if all(value is None for value in out.values()):
        return None

    return out


def _fetch_html_requests(url: str) -> Optional[str]:
    backoff = 1.0

    for _ in range(REQUEST_MAX_RETRIES):
        try:
            response = requests.get(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept-Encoding": "gzip, deflate, br",
                },
                timeout=REQUEST_TIMEOUTS,
            )
            if response.status_code == 200 and response.text:
                time.sleep(random.uniform(*SLEEP_AFTER_REQUEST))
                return response.text
        except Exception:
            pass

        time.sleep(backoff)
        backoff *= REQUEST_BACKOFF

    return None


def _fetch_html_selenium(url: str) -> Optional[str]:
    driver = make_driver(headless=False)

    try:
        driver.get(url)

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
            time.sleep(0.3)
        except Exception:
            pass

        start_time = time.time()
        while time.time() - start_time < SELENIUM_WAIT:
            title = (driver.title or "").strip()
            body_text = ""

            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            except Exception:
                pass

            if title and "un momento" not in title.lower():
                break

            if any(keyword in body_text for keyword in ("possession", "shots", "corners", "estadísticas", "tiros")):
                break

            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.2)
                driver.execute_script("window.scrollTo(0, 0);")
            except Exception:
                pass

            time.sleep(0.4)

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(SLEEP_AFTER_LOAD)
        return driver.page_source

    except Exception:
        return None

    finally:
        try:
            driver.quit()
        except Exception:
            pass


def scrape_estadisticas(match_id: str) -> Optional[dict]:
    url = f"https://fbref.com/en/matches/{match_id}"

    html = _fetch_html_selenium(url)
    if html:
        parsed = _parse_stats_from_html(html)
        if parsed:
            return parsed

    html = _fetch_html_requests(url)
    if html:
        parsed = _parse_stats_from_html(html)
        if parsed:
            return parsed

    return None