import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from imblearn.over_sampling import RandomOverSampler
import joblib
import os

# ------------------ CARGA DE DATOS ------------------
df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

# Selección de variables predictoras
features = [col for col in df.columns if col.startswith((
    "media_ult10_", "media_h2h_", "media_hist_",
    "diferencia_", "racha_", "media_hist_goles_", "tendencia_empate_"
))]

print("\nVariables predictoras utilizadas:")
for col in features:
    print(f" - {col}")

# Eliminar filas con valores nulos en target o variables
df = df.dropna(subset=["resultado"] + features)

# ------------------ DIVISIÓN TEMPORAL ------------------
df_train = df[df["fecha"].dt.year < 2024]
df_test = df[df["fecha"].dt.year == 2024]

X_train = df_train[features]
y_train = df_train["resultado"]
X_test = df_test[features]
y_test = df_test["resultado"]

print(f"\nPartidos para entrenamiento: {len(X_train)}")
print(f"Partidos para prueba: {len(X_test)}")

# ------------------- OVERSAMPLING -------------------
ros = RandomOverSampler(random_state=42)
X_train_bal, y_train_bal = ros.fit_resample(X_train, y_train)
X_train_bal, y_train_bal = shuffle(X_train_bal, y_train_bal, random_state=42)

print(f"Partidos para entrenamiento (después de oversampling): {len(X_train_bal)}")

# ----------------- DEFINICIÓN DEL MODELO ------------------
param_grid = {
    'hidden_layer_sizes': [(50,), (100,), (100, 50)],
    'activation': ['relu', 'tanh'],
    'solver': ['adam'],
    'alpha': [0.0001, 0.001],
    'learning_rate': ['constant', 'adaptive']
}

grid_search = GridSearchCV(
    estimator=MLPClassifier(
        max_iter=2000,
        early_stopping=True,
        random_state=42
    ),
    param_grid=param_grid,
    scoring='f1_macro',
    cv=5,
    verbose=1,
    n_jobs=-1
)

grid_search.fit(X_train_bal, y_train_bal)
model = grid_search.best_estimator_

# ----------------- EVALUACIÓN ------------------
y_pred = model.predict(X_test)

print("\nResultados del modelo (MLPClassifier):")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Macro Score:", f1_score(y_test, y_pred, average='macro'))

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

print("\nMejor configuración encontrada:")
print(grid_search.best_params_)

# -------------- GUARDADO OPCIONAL ----------------------
os.makedirs("modelos/mlpclassifier", exist_ok=True)
joblib.dump(model, "modelos/mlpclassifier/modelo_mlp1.pkl")
print("Modelo guardado como 'modelos/mlpclassifier/modelo_mlp1.pkl'")
