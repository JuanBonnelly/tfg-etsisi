import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from imblearn.over_sampling import RandomOverSampler
import joblib
import os

# Cargar el dataset enriquecido
df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

# Selección de columnas predictoras
features = [col for col in df.columns if col.startswith((
    "media_ult10_", "media_h2h_", "media_hist_",
    "diferencia_", "racha_", "media_hist_goles_" , "tendencia_empate_"
))]
# Mostrar variables seleccionadas
print("\nVariables predictoras utilizadas:")
for col in features:
    print(f" - {col}")
    
# Filtrado de datos completos
df = df.dropna(subset=["resultado"] + features)

# División en conjunto de entrenamiento y prueba
df_train = df[df["fecha"].dt.year < 2024]
df_test = df[df["fecha"].dt.year == 2024]

X_train = df_train[features]
y_train = df_train["resultado"]
X_test = df_test[features]
y_test = df_test["resultado"]

print(f"\nPartidos para entrenamiento: {len(X_train)}")
print(f"Partidos para prueba: {len(X_test)}")

# Aplicar oversampling para balancear clases del entrenamiento
ros = RandomOverSampler(random_state=42)
X_train_bal, y_train_bal = ros.fit_resample(X_train, y_train)

# Barajar el conjunto de entrenamiento
X_train_bal, y_train_bal = shuffle(X_train_bal, y_train_bal, random_state=42)

print(f"Partidos para entrenamiento (después de oversampling): {len(X_train_bal)}")

# Crear scaler sobre el X_train_bal ya balanceado
scaler = StandardScaler()
scaler.fit(X_train_bal)

# Definición del modelo con GridSearchCV
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

# Entrenar el modelo usando los datos balanceados y barajados
grid_search.fit(X_train_bal, y_train_bal)
model = grid_search.best_estimator_

# Evaluación del modelo
y_pred = model.predict(X_test)

print("\n Resultados del modelo (Random Forest v5):")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Macro Score:", f1_score(y_test, y_pred, average='macro'))

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

print("\n Mejor configuración encontrada:")
print(grid_search.best_params_)

# Guardar el modelo entrenado
os.makedirs("modelos", exist_ok=True)
joblib.dump(model, "modelos/random_forest/modelo_randomforest5.pkl")
print(" Modelo guardado como 'modelos/random_forest/modelo_randomforest5.pkl'")
joblib.dump(scaler, "modelos/random_forest/scaler_randomforest5.pkl")
print("Scaler guardado como 'modelos/random_forest/scaler_randomforest5.pkl'")
