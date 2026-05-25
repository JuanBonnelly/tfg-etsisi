import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Versión inicial de Random Forest.
# Usa únicamente estadísticas directas del partido como linea base del modelo.

df = pd.read_csv("data/dataset_partidos.csv", parse_dates=["fecha"])

df["anio"] = df["fecha"].dt.year
df_train = df[df["anio"] <= 2023].copy()
df_test = df[df["anio"] == 2024].copy()

print(f"Partidos para entrenamiento: {len(df_train)}")
print(f"Partidos para prueba: {len(df_test)}")

features = [
    "posesion_local", "posesion_visitante",
    "corners_local", "corners_visitante",
    "tarjetas_amarillas_local", "tarjetas_amarillas_visitante",
    "tarjetas_rojas_local", "tarjetas_rojas_visitante"
]

X_train = df_train[features]
y_train = df_train["resultado"]

X_test = df_test[features]
y_test = df_test["resultado"]

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

print("\n Resultados del modelo:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

os.makedirs("modelos", exist_ok=True)
joblib.dump(modelo, "modelos/random_forest/modelo_randomforest.pkl")
print("\nModelo guardado en 'modelos/random_forest/modelo_randomforest.pkl'")
