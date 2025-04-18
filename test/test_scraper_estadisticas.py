import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.scraper_partido import scrape_partidos
from scraper.scraper_estadisticas import scrape_estadisticas

if __name__ == "__main__":
    print("\nObteniendo 10 partidos de Premier League 2022-2023...")
    partidos = scrape_partidos()

    print("\nExtrayendo estadísticas de esos partidos...")
    estadisticas = scrape_estadisticas(partidos)

    print("\nMostrando resumen de los 10 partidos + estadísticas:\n")
    for i, partido in enumerate(partidos, start=1):
        match_id = partido.get("match_id")
        stats = next((e for e in estadisticas if e["match_id"] == match_id), None)

        print(f"[{i}] {partido.get('date')} - {partido.get('home_team')} vs {partido.get('away_team')}")
        print(f"Resultado: {partido.get('home_team_score')} - {partido.get('away_team_score')}")
        print(f"URL: {partido.get('match_url')}")
        print("Estadísticas:")

        if stats:
            for clave, valor in stats.items():
                if clave != "match_id":
                    print(f"   {clave}: {valor}")
            print("Estadísticas asociadas correctamente.")
        else:
            print("No se encontraron estadísticas para este partido.")

        print("-" * 60)
