# Predicción de resultados de fútbol

Este proyecto busca predecir resultados de partidos de fútbol a partir de datos históricos obtenidos desde FBref. Para ello se parte de un proceso completo que incluye la recogida de datos, su almacenamiento en base de datos, la construcción y enriquecimiento del dataset, el entrenamiento de varios modelos de machine learning y la integración del modelo final en una aplicación web.

A partir del histórico de partidos y estadísticas se generan variables que intentan reflejar el estado de los equipos antes de enfrentarse. Con esas variables se prueban y comparan distintos modelos de clasificación, hasta seleccionar una versión final basada en MLPClassifier. Ese modelo es el que después utiliza la aplicación para mostrar predicciones y explicaciones mediante SHAP.


## Inicio rápido

Si solo se quiere ejecutar la aplicación y probar una predicción, la forma recomendada es utilizar Docker Compose para levantar el backend y la base de datos, y npm para levantar el frontend.

1. Levantar backend y base de datos con Docker Compose: `docker compose down -v` ,`docker compose up --build`
2. Entrar en la carpeta del frontend: `cd tfg-frontend`
3. Instalar dependencias del frontend: `npm install`
4. Levantar Angular: `npm start`
5. Abrir en el navegador: `http://localhost:4200`
6. El backend queda disponible en `http://localhost:8000` la documentación interactiva de la API puede consultarse en `http://localhost:8000/docs`

## Estructura del proyecto

```text
backend/         API en FastAPI y lógica de predicción
domain/          Modelos ORM de la base de datos
infra/           Conexión a BD, generación de datasets y scripts de ML
scraper/         Scripts de scraping de partidos y estadísticas
modelos/         Modelos entrenados y artefactos .pkl
data/            Datasets generados y ficheros auxiliares
docker/          Configuración de Docker
tfg-frontend/    Frontend desarrollado con Angular
```


## Tecnologías utilizadas

En el proyecto se han utilizado principalmente:

- Python
- FastAPI
- SQLAlchemy
- MySQL
- scikit-learn
- SHAP
- Selenium
- BeautifulSoup
- Angular
- Docker y Docker Compose


## Cómo funciona el proyecto

El flujo general del sistema es el siguiente:

1. Se obtienen datos de partidos y estadísticas mediante scraping de FBref.
2. Esos datos se almacenan en una base de datos MySQL.
3. A partir de la base de datos se genera un dataset base.
4. El dataset se enriquece con nuevas variables calculadas a partir del histórico.
5. Se entrenan distintos modelos de machine learning.
6. El modelo final se guarda en formato `.pkl`.
7. El backend carga ese modelo y genera predicciones.
8. El frontend permite al usuario consultar esas predicciones desde la aplicación web.


## Scraping

La recogida de datos se hace principalmente mediante scraping sobre FBref.

Los scripts principales son:
- `scraper/scraper_all.py` coordina todo el proceso.
- `scraper/scraper_partido.py` accede a la página de una competición y temporada y extrae los partidos.
- `scraper/scraper_estadisticas.py` entra en cada partido y extrae estadísticas más detalladas.
- `scraper/scraper_utils.py` prepara el navegador usado por Selenium.

Por un lado se obtienen los datos básicos de cada partido:

- fecha,
- equipo local,
- equipo visitante,
- goles,
- competición,
- temporada,
- identificador del partido.

Después, para cada partido, se intentan extraer estadísticas como:

- posesión,
- tiros,
- tiros a puerta,
- córners,
- tarjetas amarillas,
- tarjetas rojas.

Durante el desarrollo también se utilizaron algunos HTML descargados manualmente para analizar la estructura de ciertas páginas y facilitar la depuración, pero el flujo final se basa en scraping en vivo con Selenium.


## Base de datos

Los datos obtenidos por el scraper se guardan en una base de datos MySQL. Esta base de datos es importante no solo para almacenar información, sino también para que el backend pueda construir las variables necesarias antes de hacer una predicción.

Las entidades principales del proyecto están modeladas en la carpeta `domain/` y representan, entre otras cosas:

- competiciones,
- temporadas,
- equipos,
- partidos,
- estadísticas de partido.


## Generación del dataset

Una vez cargados los datos en la base de datos, se construye un dataset para entrenamiento.

El script principal de esta fase es:

- `infra/database/generarDataset.py`

Este dataset base recoge la información histórica de partidos y estadísticas y sirve como punto de partida para el entrenamiento.


## Enriquecimiento del dataset

Después del dataset base, se aplica una fase de ingeniería de variables para obtener un dataset más útil para los modelos.

El script principal es:

- `infra/ml/features_engineering.py`

En esta fase se generan variables derivadas como, por ejemplo:

- medias de los últimos partidos,
- medias históricas,
- enfrentamientos directos,
- rachas de victorias, empates y derrotas,
- diferencias entre estadísticas de local y visitante,
- medias de goles a favor y en contra,
- tendencias de empate.

El resultado es un dataset enriquecido que ya se utiliza para entrenar los modelos de machine learning.


## Entrenamiento y modelo final

A lo largo del proyecto se probaron distintos modelos, principalmente:

- Random Forest
- MLPClassifier

El modelo final usado por la aplicación está en:

- `modelos/mlpclassifier/modelo_mlp_final.pkl`

Además, para explicar las predicciones se utiliza:

- `modelos/mlpclassifier/explainer_mlp_final.pkl`

Estos archivos son los que utiliza el backend para realizar las predicciones y generar las explicaciones.


## Backend

El backend está desarrollado con FastAPI y su fichero principal es:

- `backend/main.py`

El backend se encarga de:

- cargar el modelo entrenado,
- recuperar la información necesaria desde la base de datos,
- construir las variables del partido que se quiere predecir,
- ejecutar la predicción,
- devolver probabilidades,
- y generar explicaciones con SHAP.

El backend no trabaja únicamente con el modelo entrenado. Antes de hacer una predicción necesita consultar el histórico almacenado en la base de datos para construir las variables de entrada del partido solicitado.

Por eso, para que la aplicación funcione correctamente, se necesita:

- El modelo final ya entrenado,
- La base de datos ya poblada.


## Frontend

El frontend está desarrollado con Angular y se encuentra en:

- `tfg-frontend/`

La base del proyecto frontend fue generada inicialmente con Angular CLI y a partir de ahí se desarrolló la interfaz.

Su función es permitir al usuario:

- Seleccionar un equipo local,
- Seleccionar un equipo visitante,
- Elegir una fecha,
- Solicitar una predicción al backend,
- Ver el resultado con sus probabilidades y explicaciones.


## Estado de la entrega

El proyecto se entrega con:

- Un dump de la base de datos en `docker/mysql/initdb/`,
- El modelo final ya entrenado en modelos/mlpclassifier/modelo_mlp_final.pkl;
- El explainer utilizado para las explicaciones SHAP en modelos/mlpclassifier/explainer_mlp_final.pkl;
- Un archivo .env.example como plantilla de variables de entorno para ejecución local del backend.

Esto permite ejecutar directamente la aplicación sin necesidad de repetir el scraping ni el entrenamiento completo.

Cuando MySQL se inicializa por primera vez con Docker Compose, ejecuta automáticamente los scripts y dumps incluidos en `docker/mysql/initdb/`. De esta forma, la base de datos queda cargada con la información necesaria para que la aplicación funcione.

La base de datos ya poblada es necesaria porque el backend utiliza el histórico almacenado para construir las variables del partido a predecir. El modelo `.pkl` se usa después para obtener la predicción final.

Para reconstruir la base de datos desde cero, se recomienda ejecutar:

docker compose down -v
docker compose up --build

El parámetro -v elimina el volumen anterior de MySQL y permite que el dump vuelva a cargarse desde cero.

Si se ejecuta el proyecto mediante Docker Compose, no es necesario crear un archivo `.env`, ya que las variables de entorno necesarias para el backend están definidas directamente en `docker-compose.yml`.

El archivo `.env.example` se incluye únicamente como plantilla para la ejecución local del backend fuera de Docker.

Para ejecutar el backend localmente, se debe copiar `.env.example` y renombrarlo como `.env`.


## Requisitos previos

Para ejecutar el proyecto es necesario disponer de:

- Python 3.9 o superior
- Node.js y npm
- Docker y Docker Compose
- Google Chrome instalado, si se quiere ejecutar el scraper con Selenium


## Instalación de dependencias

### Backend
La forma recomendada de ejecutar el backend es mediante Docker Compose, ya que de esta forma también se levanta la base de datos MySQL y se cargan automáticamente las variables necesarias para el funcionamiento de la aplicación.

La ejecución local del backend es opcional. Si se desea ejecutar el backend fuera de Docker, primero se debe crear un archivo .env en la raíz del proyecto a partir del archivo .env.example.
Desde la raíz del proyecto:

```bash
pip install -r requirements.txt
```

Si se quiere usar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

Desde `tfg-frontend/`:

```bash
npm install
```

## Cómo ejecutar el proyecto

### Levantar backend y base de datos

La forma recomendada es utilizar Docker Compose.

Desde la raíz del proyecto:

```bash
docker compose down -v
docker compose up --build
```

Esto levanta:

- MySQL
- backend FastAPI
- La base de datos futbol_TFG
- Carga automaticamente el dump incluido en docker/mysql/initdb/.

El backend queda disponible en http://localhost:8000


La documentación interactiva de la API está en http://localhost:8000/docs


### Levantar el frontend

Desde la carpeta `tfg-frontend/`:

```bash
npm start
```

o, según la configuración disponible:

```bash
ng serve
```

El frontend queda disponible en http://localhost:4200


## Cómo probar la aplicación

Una vez levantado todo:

1. Acceder al frontend en `http://localhost:4200`
2. Seleccionar equipo local
3. Seleccionar equipo visitante
4. Elegir una fecha
5. Consultar la predicción

La aplicación mostrara:

- resultado predicho,
- probabilidad de victoria local,
- probabilidad de empate,
- probabilidad de victoria visitante,
- y explicación de las variables más influyentes.

## Scripts importantes

### Scraper
- `scraper/scraper_all.py`
- `scraper/scraper_partido.py`
- `scraper/scraper_estadisticas.py`
- `scraper/scraper_utils.py`

### Dataset y machine learning
- `infra/database/generarDataset.py`
- `infra/ml/features_engineering.py`

### Backend
- `backend/main.py`

### Modelo final
- `modelos/mlpclassifier/modelo_mlp_final.pkl`
- `modelos/mlpclassifier/explainer_mlp_final.pkl`


## Observaciones finales

- El scraping depende de la estructura HTML de FBref, por lo que puede requerir ajustes si la web cambia.
- La aplicación puede ejecutarse directamente sin repetir scraping ni entrenamiento, siempre que se mantengan la base de datos cargada y los modelos entrenados.