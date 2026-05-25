import os

import joblib
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle

# Segunda iteración del modelo MLPClassifier.
# Prueba experimental con escalado, balanceo de clases y reasignación de los empates del conjunto de prueba al entrenamiento.
df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

features = [col for col in df.columns if col.startswith((
    "media_ult10_", "media_h2h_", "media_hist_",
    "diferencia_", "racha_", "media_hist_goles_", "tendencia_empate_"
))]

print("\nVariables predictoras utilizadas:")
for col in features:
    print(f" - {col}")


df = df.dropna(subset=["resultado"] + features)

df_train = df[df["fecha"].dt.year < 2024]
df_test = df[df["fecha"].dt.year == 2024]


empates_test = df_test[df_test["resultado"] == 0].copy()
df_test = df_test[df_test["resultado"] != 0]
df_train = pd.concat([df_train, empates_test], ignore_index=True)

X_train = df_train[features]
y_train = df_train["resultado"]
X_test = df_test[features]
y_test = df_test["resultado"]

print(f"\nEmpates movidos a entrenamiento: {len(empates_test)}")
print(f"Total entrenamiento: {len(X_train)}")
print(f"Total prueba: {len(X_test)}")


ros = RandomOverSampler(random_state=42)
X_train_bal, y_train_bal = ros.fit_resample(X_train, y_train)
X_train_bal, y_train_bal = shuffle(X_train_bal, y_train_bal, random_state=42)

print(f"Partidos para entrenamiento después de oversampling: {len(X_train_bal)}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_bal)
X_test_scaled = scaler.transform(X_test)


param_grid = {
    'hidden_layer_sizes': [(50,), (100,), (100, 50), (50, 30), (150, 100, 50)],
    'activation': ['relu', 'tanh'],
    'solver': ['adam'],
    'alpha': [0.00001, 0.0001],
    'learning_rate': ['constant', 'adaptive']
}

grid_search = GridSearchCV(
    estimator=MLPClassifier(max_iter=3000, early_stopping=True, n_iter_no_change=20, random_state=42),
    param_grid=param_grid,
    scoring='f1_macro',
    cv=5,
    verbose=1,
    n_jobs=-1
)

grid_search.fit(X_train_scaled, y_train_bal)
modelo = grid_search.best_estimator_

y_pred = modelo.predict(X_test_scaled)

print("\nResultados del modelo version 2 de MLPClassifier:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Macro Score:", f1_score(y_test, y_pred, average='macro'))

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

print("\nMejor configuración encontrada:")
print(grid_search.best_params_)

os.makedirs("modelos/mlpclassifier", exist_ok=True)
joblib.dump(modelo, "modelos/mlpclassifier/modelo_mlp2.pkl")
joblib.dump(scaler, "modelos/mlpclassifier/scaler_mlp2.pkl")
print("Modelo guardado como 'modelos/mlpclassifier/modelo_mlp2.pkl'")
print("Scaler guardado como 'modelos/mlpclassifier/scaler_mlp2.pkl'")
