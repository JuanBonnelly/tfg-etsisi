import os

import joblib
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle

# Quinta iteración del modelo Random Forest.
# Se añaden variables, incorpora balanceo de clases y ajusta hiperparámetros con GridSearchCV.

df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

features = [col for col in df.columns if col.startswith((
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
    "posesion_local",
    "posesion_visitante",
    "corners_local",
    "corners_visitante",
    "tarjetas_amarillas_local",
    "tarjetas_amarillas_visitante",
    "tarjetas_rojas_local",
    "tarjetas_rojas_visitante"
))]

print("\nVariables predictoras utilizadas:")
for col in features:
    print(f" - {col}")
    
df = df.dropna(subset=["resultado"] + features)

df_train = df[df["fecha"].dt.year < 2024]
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

print(f"Partidos para entrenamiento después de Oversampling: {len(X_train_bal)}")

param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [5, 10, 15],
    "max_features": ["sqrt", "log2"],
    "min_samples_split": [2, 5],
    "class_weight": ["balanced"]
}

grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=5,
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train_bal, y_train_bal)
modelo = grid_search.best_estimator_

y_pred = modelo.predict(X_test)

print("\n Resultados del modelo versión 5 del RandomForest:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Macro Score:", f1_score(y_test, y_pred, average='macro'))

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

print("\n Mejor configuración encontrada:")
print(grid_search.best_params_)

#os.makedirs("modelos", exist_ok=True)
#joblib.dump(modelo, "modelos/random_forest/modelo_randomforest5.pkl")
#print(" Modelo guardado como 'modelos/random_forest/modelo_randomforest5.pkl'")
