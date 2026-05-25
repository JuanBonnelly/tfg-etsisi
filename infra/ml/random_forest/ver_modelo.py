import os

import joblib
import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Inspección del modelo Random Forest final y visualización de importancia de variables.
MODELO_PATH = "modelos/random_forest/modelo_randomforest5.pkl"
DATASET_PATH = "data/dataset_partidos_enriquecido.csv"

if not os.path.exists(MODELO_PATH):
    raise FileNotFoundError(f"No se encontró el modelo en {MODELO_PATH}")

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"No se encontró el dataset en {DATASET_PATH}")

modelo = joblib.load(MODELO_PATH)
print(f"\nModelo cargado: {MODELO_PATH}")
print(f"Tipo: {type(modelo)}")

df = pd.read_csv(DATASET_PATH)
features = [col for col in df.columns if col.startswith((
    "media_ult10_",
    "media_h2h_",
    "media_hist_",
    "diferencia_",
    "racha_",
    "tendencia_empate_",
))]

if hasattr(modelo, "feature_importances_"):
    importancias = modelo.feature_importances_
    importancia_df = pd.DataFrame({
        "feature": features,
        "importancia": importancias,
    }).sort_values(by="importancia", ascending=False)

    print("\nImportancia de variables:")
    print(importancia_df.to_string(index=False))

    plt.figure(figsize=(10, 6))
    importancia_df.sort_values("importancia").plot.barh(x="feature", y="importancia", legend=False)
    plt.title("Importancia de variables (Random Forest)")
    plt.xlabel("Importancia relativa")
    plt.tight_layout()

    os.makedirs("graficas", exist_ok=True)
    plt.savefig("graficas/importancia_variables_modelo5.png", dpi=300)
    print("Gráfico guardado en 'graficas/importancia_variables_modelo5.png'")
else:
    print("Este modelo no tiene el atributo 'feature_importances_'.")