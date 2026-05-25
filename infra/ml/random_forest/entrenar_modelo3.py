import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV

# Tercera iteración del modelo Random Forest.
# Mantiene el dataset enriquecido e incorpora una búsqueda de hiperparámetros con GridSearchCV.

df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

features = [col for col in df.columns if col.startswith("media_")]
X = df[features]
y = df["resultado"]

X_train = X[df["fecha"].dt.year < 2024]
y_train = y[df["fecha"].dt.year < 2024]

X_test = X[df["fecha"].dt.year == 2024]
y_test = y[df["fecha"].dt.year == 2024]

print(f"\nPartidos para entrenamiento: {len(X_train)}")
print(f"Partidos para prueba: {len(X_test)}")

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'max_features': ['sqrt', 'log2']
}

m_base = RandomForestClassifier(random_state=42)

grid_search = GridSearchCV(m_base, param_grid, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

mejor_modelo = grid_search.best_estimator_
y_pred = mejor_modelo.predict(X_test)

print("\n Resultados del mejor modelo encontrado:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))
print("\n Mejor configuración encontrada:")
print(grid_search.best_params_)

os.makedirs("modelos", exist_ok=True)
joblib.dump(mejor_modelo, "modelos/random_forest/modelo_randomforest3.pkl")
print(" Modelo guardado como 'modelos/random_forest/modelo_randomforest3.pkl'")
