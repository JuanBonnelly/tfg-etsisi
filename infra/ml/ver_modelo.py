import joblib
import os
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')  # Fuerza uso sin GUI (evita error Tcl)
import matplotlib.pyplot as plt

# Ruta al modelo que quieres analizar
MODELO_PATH = "modelos/modelo_randomforest4.pkl"

# Ruta al dataset que se usó para entrenar el modelo
DATASET_PATH = "data/dataset_partidos_enriquecido.csv"

# ================= CARGAR MODELO ====================
if not os.path.exists(MODELO_PATH):
    print(f" No se encontró el modelo en {MODELO_PATH}")
    exit()

modelo = joblib.load(MODELO_PATH)
print(f"\n Modelo cargado: {MODELO_PATH}")
print(f"Tipo: {type(modelo)}")

# ================= CARGAR DATASET ===================
if not os.path.exists(DATASET_PATH):
    print(f" No se encontró el dataset en {DATASET_PATH}")
    exit()

df = pd.read_csv(DATASET_PATH)
features = [col for col in df.columns if col.startswith("media_")]

# ================= INFO DEL MODELO ==================
if hasattr(modelo, "feature_importances_"):
    importancias = modelo.feature_importances_
    importancia_df = pd.DataFrame({
        "feature": features,
        "importancia": importancias
    }).sort_values(by="importancia", ascending=False)

    print("\n Importancia de variables:")
    print(importancia_df.to_string(index=False))

    # ======== VISUALIZACIÓN ==========
    plt.figure(figsize=(10, 6))
    importancia_df.sort_values("importancia").plot.barh(x="feature", y="importancia", legend=False)
    plt.title("Importancia de variables (Random Forest)")
    plt.xlabel("Importancia relativa")
    plt.tight_layout()
    # Crear carpeta si no existe
    os.makedirs("graficas", exist_ok=True)

    # Guardar imagen
    plt.savefig("graficas/importancia_variables_modelo4.png", dpi=300)
    print("Gráfico guardado en 'graficas/importancia_variables_modelo4.png'")


else:
    print(" Este modelo no tiene atributo 'feature_importances_' (¿no es un árbol?).")
