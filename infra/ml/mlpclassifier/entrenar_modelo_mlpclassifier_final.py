import os

import joblib
import pandas as pd
import shap
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle

# Modelo final MLPClassifier.
# Entrena el modelo definitivo con variables históricas, derivadas y estadísticas base del partido.

DATASET_PATH = "data/dataset_partidos_enriquecido.csv"

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"No se encontró el dataset en '{DATASET_PATH}'")

df = pd.read_csv(DATASET_PATH, parse_dates=["fecha"])
print(f"Dataset cargado con {len(df)} filas.")

features = [
    "posesion_local",
    "posesion_visitante",
    "corners_local",
    "corners_visitante",
    "tarjetas_amarillas_local",
    "tarjetas_amarillas_visitante",
    "tarjetas_rojas_local",
    "tarjetas_rojas_visitante",
    "media_ult10_posesion_local",
    "media_ult10_posesion_visitante",
    "media_ult10_corners_local",
    "media_ult10_corners_visitante",
    "media_ult10_tarjetas_amarillas_local",
    "media_ult10_tarjetas_amarillas_visitante",
    "media_ult10_tarjetas_rojas_local",
    "media_ult10_tarjetas_rojas_visitante",
    "tendencia_empate_h2h",
    "media_h2h_posesion_local",
    "media_h2h_posesion_visitante",
    "media_h2h_corners_local",
    "media_h2h_corners_visitante",
    "media_h2h_tarjetas_amarillas_local",
    "media_h2h_tarjetas_amarillas_visitante",
    "media_h2h_tarjetas_rojas_local",
    "media_h2h_tarjetas_rojas_visitante",
    "media_hist_posesion_local",
    "media_hist_posesion_visitante",
    "media_hist_corners_local",
    "media_hist_corners_visitante",
    "media_hist_tarjetas_amarillas_local",
    "media_hist_tarjetas_amarillas_visitante",
    "media_hist_tarjetas_rojas_local",
    "media_hist_tarjetas_rojas_visitante",
    "media_ult10_diferencia_goles_local",
    "media_ult10_diferencia_goles_visitante",
    "media_h2h_diferencia_goles_local",
    "media_h2h_diferencia_goles_visitante",
    "media_hist_diferencia_goles_local",
    "media_hist_diferencia_goles_visitante",
    "racha_ganados_local_ult5",
    "racha_ganados_visitante_ult5",
    "diferencia_posesion",
    "diferencia_corners",
    "diferencia_tarjetas_amarillas",
    "diferencia_tarjetas_rojas",
    "media_hist_goles_local_a_favor",
    "media_hist_goles_local_en_contra",
    "racha_empates_local_ult5",
    "racha_derrotas_local_ult5",
    "racha_empates_visitante_ult5",
    "racha_derrotas_visitante_ult5",
    "goles_local_ult5_media",
    "goles_visitante_ult5_media",
    "tendencia_empate_local",
    "tendencia_empate_visitante",
]

print("\nVariables predictoras utilizadas:")
for col in features:
    print(f" - {col}")

print(f"\nSe utilizarán {len(features)} features para el entrenamiento.")

df = df.dropna(subset=["resultado"] + features)

df_train = df[df["fecha"].dt.year <= 2023]
df_test = df[df["fecha"].dt.year == 2024]

X_train = df_train[features]
y_train = df_train["resultado"]
X_test = df_test[features]
y_test = df_test["resultado"]

print(f"\nPartidos para entrenamiento: {len(X_train)}")
print(f"Partidos para prueba: {len(X_test)}")

ros = RandomOverSampler(random_state=42)
X_train_bal, y_train_bal = ros.fit_resample(X_train, y_train)
X_train_bal, y_train_bal = shuffle(X_train_bal, y_train_bal, random_state=42)

print(f"Partidos para entrenamiento después de oversampling: {len(X_train_bal)}")

param_grid = {
    "hidden_layer_sizes": [(50,), (100,), (100, 50)],
    "activation": ["relu", "tanh"],
    "solver": ["adam"],
    "alpha": [0.0001, 0.001],
    "learning_rate": ["constant", "adaptive"],
}

print("\nBuscando la mejor configuración para MLPClassifier...")
grid_search = GridSearchCV(
    estimator=MLPClassifier(
        max_iter=2000,
        early_stopping=True,
        random_state=42,
    ),
    param_grid=param_grid,
    scoring="f1_macro",
    cv=5,
    verbose=1,
    n_jobs=-1,
)

grid_search.fit(X_train_bal, y_train_bal)
modelo = grid_search.best_estimator_

print("\nMejor configuración encontrada:")
print(grid_search.best_params_)

y_pred = modelo.predict(X_test)

print("\nResultados del modelo final (MLPClassifier):")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"F1 Macro Score: {f1_score(y_test, y_pred, average='macro'):.4f}")

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

print("\nCreando explicador SHAP")
X_train_summary = shap.sample(X_train_bal, 100, random_state=42)
explainer = shap.KernelExplainer(modelo.predict_proba, X_train_summary)
print("Explicador SHAP creado.")

print("\nArtefactos preparados para guardarse, pero no se guardarán en esta prueba.")
MODEL_PATH = "modelos/mlpclassifier/modelo_mlp_final.pkl"
EXPLAINER_PATH = "modelos/mlpclassifier/explainer_mlp_final.pkl"

os.makedirs("modelos/mlpclassifier", exist_ok=True)
joblib.dump(modelo, MODEL_PATH)
joblib.dump(explainer, EXPLAINER_PATH)
print("\nArtefactos guardados correctamente.")
print(f"Modelo guardado en: {MODEL_PATH}")
print(f"Explicador guardado en: {EXPLAINER_PATH}")