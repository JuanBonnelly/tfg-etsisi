# inspector.py
import joblib

# Asegúrate de que esta ruta es la correcta a tu scaler
SCALER_PATH = "modelos/random_forest/scaler_randomforest5.pkl"

print(f"--- Inspeccionando el scaler en: {SCALER_PATH} ---")

try:
    scaler = joblib.load(SCALER_PATH)
    
    # Los scalers de scikit-learn guardan los nombres de las features
    # con las que fueron ajustados en el atributo `feature_names_in_`
    if hasattr(scaler, 'feature_names_in_'):
        feature_names = scaler.feature_names_in_
        
        print("\n--- ¡LISTA DE FEATURES DEFINITIVA OBTENIDA DEL SCALER! ---")
        # Imprimimos la lista en un formato fácil de copiar y pegar
        print("[")
        for name in feature_names:
            print(f"    '{name}',")
        print("]")
        
        print(f"\n--- TOTAL: {len(feature_names)} features ---")
        
    else:
        print("ERROR: Este scaler no tiene el atributo 'feature_names_in_'. ¿Se guardó con una versión antigua de scikit-learn?")

except FileNotFoundError:
    print(f"ERROR: No se pudo encontrar el archivo del scaler en '{SCALER_PATH}'. Verifica la ruta.")
except Exception as e:
    print(f"Ocurrió un error al cargar o inspeccionar el scaler: {e}")