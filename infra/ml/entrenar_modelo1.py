import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import joblib
import os

# Cargar el dataset
df = pd.read_csv("data/dataset_partidos.csv", parse_dates=["fecha"])

# Filtrar por año para dividir entrenamiento y prueba
df["anio"] = df["fecha"].dt.year
df_train = df[df["anio"] <= 2023].copy()
df_test = df[df["anio"] == 2024].copy()

print(f"Partidos para entrenamiento: {len(df_train)}")
print(f"Partidos para prueba: {len(df_test)}")

# Selección de variables
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

# Entrenar modelo Random Forest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Evaluación del modelo
y_pred = modelo.predict(X_test)

print("\n Resultados del modelo:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

# Guardar modelo como .pkl
os.makedirs("modelos", exist_ok=True)
joblib.dump(modelo, "modelos/modelo_randomforest.pkl")
print("\nModelo guardado en 'modelos/modelo_randomforest.pkl'")
