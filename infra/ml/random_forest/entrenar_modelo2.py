import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Segunda iteración del modelo Random Forest.
# Sustituye el dataset base por el dataset enriquecido y utiliza variables históricas tipo media_*.

df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

df["anio"] = df["fecha"].dt.year
df_train = df[df["anio"] <= 2023].copy()
df_test = df[df["anio"] == 2024].copy()

print(f"Partidos para entrenamiento: {len(df_train)}")
print(f"Partidos para prueba: {len(df_test)}")

features = [col for col in df.columns if col.startswith("media_")]

X_train = df_train[features]
y_train = df_train["resultado"]

X_test = df_test[features]
y_test = df_test["resultado"]

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

print("\n Resultados del modelo versión 2 RandomForest:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

os.makedirs("modelos", exist_ok=True)
joblib.dump(modelo, "modelos/random_forest/modelo_randomforest2.pkl")
print("\nModelo guardado en 'modelos/random_forest/modelo_randomforest2.pkl'")
