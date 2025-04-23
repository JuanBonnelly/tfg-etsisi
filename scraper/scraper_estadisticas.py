import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bs4 import BeautifulSoup
from domain.models.estadisticas_partido import EstadisticasPartido
from infra.minio.minio_client import create_minio_client


def scrape_estadisticas(match_id: str) -> EstadisticasPartido | None:
    client = create_minio_client()

    try:
        obj = client.get_object("fbref", "estadisticas_partido.html")
        html = obj.read().decode("utf-8")
    except Exception as e:
        print(f" Error al acceder al archivo: {e}")
        return None

    soup = BeautifulSoup(html, "html.parser")
    estadisticas = EstadisticasPartido(partido_id=match_id)

    filas = soup.find_all("tr")
    for fila in filas:
        th = fila.find("th")
        if not th or not th.has_attr("colspan"):
            continue

        titulo = th.get_text(strip=True).lower()

        if "posesión" in titulo:
            tds = fila.find_next_siblings("tr", limit=1)[0].find_all("td")
            try:
                estadisticas.posesion_local = float(tds[0].get_text(strip=True).replace("%", ""))
                estadisticas.posesion_visitante = float(tds[1].get_text(strip=True).replace("%", ""))
            except:
                pass

        elif "disparos a puerta" in titulo:
            siguiente = fila.find_next_siblings("tr", limit=1)
            if siguiente:
                try:
                    divs_local = siguiente[0].find_all("td")[0].find_all("div")
                    divs_visitante = siguiente[0].find_all("td")[1].find_all("div")
                    texto_local = divs_local[0].get_text(strip=True).lower()
                    estadisticas.tiros_puerta_local = int(texto_local.split("of")[0].strip())
                    estadisticas.tiros_local = int(texto_local.split("of")[1].split("—")[0].strip())
                    texto_visitante = divs_visitante[0].get_text(strip=True).lower()
                    estadisticas.tiros_puerta_visitante = int(texto_visitante.split("of")[0].split()[-1])
                    estadisticas.tiros_visitante = int(texto_visitante.split("of")[1].strip())
                except:
                    pass

        elif "tarjetas" in titulo:
            siguiente = fila.find_next_siblings("tr", limit=1)
            if siguiente:
                tds = siguiente[0].find_all("td")
                try:
                    estadisticas.tarjetas_amarillas_local = len(tds[0].find_all("span", class_="yellow_card"))
                    estadisticas.tarjetas_amarillas_visitante = len(tds[1].find_all("span", class_="yellow_card"))
                    estadisticas.tarjetas_rojas_local = len(tds[0].find_all("span", class_="red_card"))
                    estadisticas.tarjetas_rojas_visitante = len(tds[1].find_all("span", class_="red_card"))
                except:
                    pass

        # === Tiros de esquina ===
    extras_div = soup.find("div", id="team_stats_extra")
    if extras_div:
        filas_extra = extras_div.find_all("div")
        for fila in filas_extra:
            th = fila.find("div", string=lambda text: text and "Tiro de esquina" in text)
            if th:
                cornerlocal_div = th.find_previous("div")
                cornervisitante_div = th.find_next("div")
                try:
                    estadisticas.corners_local = int(cornerlocal_div.get_text(strip=True))
                    estadisticas.corners_visitante = int(cornervisitante_div.get_text(strip=True))
                except Exception as e:
                    print(f" Error al procesar córners: {e}")
                break  

    print(f" Estadísticas extraídas correctamente para {match_id}")
    return estadisticas

if __name__ == "__main__":
    partidos_prueba = ["3adf2aa7"]

    for i, match_id in enumerate(partidos_prueba, start=1):
        estadisticas = scrape_estadisticas(match_id)
        if estadisticas:
            print(f"\n[{i}] Estadísticas para el partido {match_id}")
            print(f"  Posesión:       Local {estadisticas.posesion_local}% | Visitante {estadisticas.posesion_visitante}%")
            print(f"  Tiros:          Local {estadisticas.tiros_local} | Visitante {estadisticas.tiros_visitante}")
            print(f"  Tiros a puerta: Local {estadisticas.tiros_puerta_local} | Visitante {estadisticas.tiros_puerta_visitante}")
            print(f"  Córners:        Local {estadisticas.corners_local} | Visitante {estadisticas.corners_visitante}")
            print(f"  Amarillas:      Local {estadisticas.tarjetas_amarillas_local} | Visitante {estadisticas.tarjetas_amarillas_visitante}")
            print(f"  Rojas:          Local {estadisticas.tarjetas_rojas_local} | Visitante {estadisticas.tarjetas_rojas_visitante}")
        else:
            print(f"\n[{i}]  No se pudieron obtener estadísticas para el partido {match_id}")
