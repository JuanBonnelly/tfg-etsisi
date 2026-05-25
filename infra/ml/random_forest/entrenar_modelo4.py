import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Cuarta iteración del modelo Random Forest.
# Fija una configuración concreta a partir de la búsqueda realizada en la versión anterior.

df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

df = df.dropna(subset=["resultado"])
features = [col for col in df.columns if col.startswith(("media_ult10_", "media_h2h_", "media_hist_"))]
df = df.dropna(subset=features)

df_train = df[df["fecha"].dt.year < 2024]
df_test = df[df["fecha"].dt.year == 2024]

X_train = df_train[features]
y_train = df_train["resultado"]

X_test = df_test[features]
y_test = df_test["resultado"]

print(f"\nPartidos para entrenamiento: {len(X_train)}")
print(f"Partidos para prueba: {len(X_test)}")

modelo = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    max_features="sqrt",
    min_samples_split=2,
    random_state=42
)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
print("\n Resultados del modelo versión 4 del RandomForest :")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

os.makedirs("modelos", exist_ok=True)
joblib.dump(modelo, "modelos/random_forest/modelo_randomforest4.pkl")
print(" Modelo guardado como 'modelos/random_forest/modelo_randomforest4.pkl'")
