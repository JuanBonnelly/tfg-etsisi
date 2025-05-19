import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# Cargar el dataset enriquecido
df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

# Filtrar por año
df["anio"] = df["fecha"].dt.year
df_train = df[df["anio"] <= 2023].copy()
df_test = df[df["anio"] == 2024].copy()

print(f"Partidos para entrenamiento: {len(df_train)}")
print(f"Partidos para prueba: {len(df_test)}")

# Seleccionar variables (features) que empiezan por "media_"
features = [col for col in df.columns if col.startswith("media_")]

X_train = df_train[features]
y_train = df_train["resultado"]

X_test = df_test[features]
y_test = df_test["resultado"]

# Entrenar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Predicciones y evaluación
y_pred = modelo.predict(X_test)

print("\n Resultados del modelo (Random Forest v2):")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

# Guardar modelo
os.makedirs("modelos", exist_ok=True)
joblib.dump(modelo, "modelos/modelo_randomforest3.pkl")
print("\nModelo guardado en 'modelos/modelo_randomforest3.pkl'")
