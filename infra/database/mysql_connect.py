import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables desde el .env
load_dotenv()

def get_mysql_connection():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

    try:
        engine = create_engine(url)
        connection = engine.connect()
        print("Conexión a la base de datos establecida correctamente.")
        return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

def main():
    conn = get_mysql_connection()
    query = """SELECT * FROM futbol_TFG.test"""
    if conn:
        result = conn.execute(text(query))
        print("Tablas existentes:")
        for row in result:
            print(row)
        conn.close()

if __name__ == "__main__":
    main()

