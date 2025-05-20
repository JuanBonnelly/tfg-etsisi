import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# Cargar el dataset
df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

# Filtrar partidos con datos completos
df = df.dropna(subset=["resultado"])
features = [col for col in df.columns if col.startswith(("media_ult10_", "media_h2h_", "media_hist_"))]
df = df.dropna(subset=features)

# División temporal: entrenamiento hasta 2023, prueba con 2024
df_train = df[df["fecha"].dt.year < 2024]
df_test = df[df["fecha"].dt.year == 2024]

X_train = df_train[features]
y_train = df_train["resultado"]

X_test = df_test[features]
y_test = df_test["resultado"]

print(f"\nPartidos para entrenamiento: {len(X_train)}")
print(f"Partidos para prueba: {len(X_test)}")

# Hiperparámetros óptimos de modelo4
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    max_features="sqrt",
    min_samples_split=2,
    random_state=42
)
model.fit(X_train, y_train)

# Predicciones y evaluación
y_pred = model.predict(X_test)
print("\n Resultados del modelo (Random Forest v4):")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

# Guardar modelo
os.makedirs("modelos", exist_ok=True)
joblib.dump(model, "modelos/modelo_randomforest4.pkl")
print(" Modelo guardado como 'modelos/modelo_randomforest4.pkl'")
