# TFG de Juan

¡Excelente! He analizado en profundidad ambos documentos que has proporcionado. Tu trabajo hasta la fecha es realmente notable, y la documentación es exhaustiva, lo cual facilita enormemente mi labor como tutor. A continuación, te presento una síntesis refinada del estado actual de tu proyecto, combinando la información de ambos enfoques, junto con un plan de acción y sugerencias detalladas para las fases restantes.

---

### **Informe de Tutoría Detallado: Proyecto de Predicción de Resultados de Fútbol con ML**

**1. Evaluación General y Contexto del Proyecto**

Tu Trabajo de Fin de Grado aborda una necesidad real y relevante: la ausencia de herramientas gratuitas y accesibles para predecir resultados de partidos de fútbol. El objetivo de desarrollar una página web interactiva, potenciada por un modelo de Machine Learning entrenado con datos de la Premier League, es claro, conciso y perfectamente alineado con las competencias de Ingeniería del Software. La multidisciplinariedad del proyecto (bases de datos, backend, frontend, ML, DevOps) lo hace ideal para un TFG, demostrando tu capacidad para integrar diversas disciplinas.

**2. Arquitectura del Sistema y Tecnologías Seleccionadas**

La pila tecnológica seleccionada es coherente y bien justificada, equilibrando pragmatismo con la adopción de buenas prácticas modernas:

*   **Base de Datos (MySQL):** Elección sólida y pragmática basada en tu familiaridad y la naturaleza estructurada de los datos deportivos.
*   **Backend (Python):** Acertada decisión por su coherencia con el ML y la simplicidad de la infraestructura.
*   **Frontend (Angular):** Una elección eficiente dada tu experiencia, permitiendo alta productividad.
*   **Machine Learning (Python con Scikit-learn):** Estándar y muy adecuado para el alcance de un TFG, ofreciendo gran versatilidad.
*   **Infraestructura y Control de Versiones (Docker, Git/GitHub, ClickUp):** Demuestra una gestión profesional del proyecto, con herramientas estándar de la industria que garantizan reproducibilidad, colaboración y organización.
*   **Patrón de Diseño (Domain-Driven Design - DDD):** La aplicación de DDD es un valor añadido significativo. La creación de una estructura `dominio/modelos` y una superclase base para ORM es un excelente punto de partida. Para la memoria, será crucial profundizar en cómo los principios clave del DDD (Entidades, Objetos de Valor, Agregados, Servicios de Dominio, Repositorios y Lenguaje Ubicuo) se han traducido en la implementación del código y las reglas de negocio.

**3. Estado del Trabajo Realizado (Logros Detallados)**

El progreso documentado es **excepcional** y sienta una base muy sólida para las próximas fases. Has demostrado una gran proactividad y rigor en la documentación.

*   **Infraestructura de Desarrollo y DDD:**
    *   Has configurado un entorno robusto con **Docker**, incluyendo **MinIO** para el almacenamiento local de archivos HTML y una instancia de **MySQL** con un usuario dedicado (`futbol_TFG`). Esto asegura un entorno aislado y reproducible.
    *   La organización del código bajo **DDD** (`dominio/modelos`, `infra/`) y la herencia de una clase base ORM para tus modelos demuestran una comprensión avanzada de la arquitectura de software.
*   **Modelado de Datos (ER y ORM):**
    *   El **Modelo Entidad-Relación (MER)** está bien definido y documentado, con entidades claras como `Competición`, `Temporada`, `Equipo`, `Partido` y `EstadísticasPartido`.
    *   Has justificado perfectamente la **doble relación de `Partido` con `Equipo`** (local/visitante) y la **denormalización controlada de `competicion_id`** en `Partido` por motivos de rendimiento y simplificación de consultas. Estas son decisiones pragmáticas y bien pensadas.
    *   La implementación con **SQLAlchemy (ORM)** y la creación de **pruebas unitarias** para validar las relaciones ORM (`test_equipo.py`, `test_partido.py`, `test_estadistica_partido.py`, `test_integracion_modelo.py`) son prácticas excelentes que aseguran la integridad del modelo de datos en el código.
*   **Scraping de Datos Históricos (Extracción y Carga):**
    *   Ante los bloqueos de **fbref.com**, tu solución de **descargar HTMLs y procesarlos localmente con MinIO** es una muestra de ingenio y adaptabilidad. Esto te ha permitido avanzar sin depender de una fuente online inestable.
    *   El scraping está **modularizado** (`scraper_partidos.py` separa extracción de inserción), y has logrado extraer datos de una temporada completa (380 partidos, 20 equipos de Premier League).
    *   La corrección del `partido_id` a `String(20)` y la gestión de la inserción de datos (deshabilitando/habilitando restricciones de clave foránea) demuestran un manejo práctico de MySQL.
    *   Las **pruebas unitarias** para los scrapers (`test_scraper_partidos_db.py`, `test_scraper_estadisticas_db.py`) garantizan la fiabilidad de la ingesta de datos.
*   **Generación del Dataset y Preprocesamiento de Datos para ML:**
    *   El script `generarDataset.py` consolida la información de múltiples tablas, creando un dataset plano ideal para ML.
    *   La definición de la columna `resultado` (1, 0, -1) para una **clasificación multiclase** es fundamental y simplifica el problema.
    *   La **ingeniería de características** es uno de tus mayores fuertes: `features_engineering.py` calcula métricas históricas de últimos partidos (`media_ultX`), enfrentamientos directos (`media_h2h`), tendencias de empates, rachas, etc. Esto es crucial para la calidad del modelo.
    *   El manejo de nulos, la **división temporal** (entrenamiento hasta 2023, prueba con 2024) y la **normalización/escalado** para el MLP son pasos correctos de preprocesamiento.
*   **Entrenamiento de Modelos de Machine Learning:**
    *   Has seguido un **proceso iterativo y metódico**, lo cual es excelente.
    *   **Random Forest (RF) Evolución:**
        *   **RF v1 (baseline):** `accuracy` ~40-41%.
        *   **RF v2 (históricos):** `accuracy` ~44%.
        *   **RF v3 (10-match/H2H, GridSearchCV):** `accuracy` ~43%. (Slight dip, but better tuning).
        *   **RF v4 (enriquecido):** `accuracy` ~54.2%, identificando el problema de **predicción de empates**.
        *   **RF v5 (enfoque en empates):** Incorporó `tendencia_empate_h2h`, `tendencia_empate_local/visitante`, `RandomOverSampler`, `shuffling`, y se adoptó **F1-macro** como métrica principal. Alcanzó `accuracy` ~56.4%, `F1-macro` ~0.467, pero el `recall` de empates siguió siendo bajo (~0.07).
    *   **MLPClassifier:** Tu decisión de explorar redes neuronales es acertada para la diversidad y para intentar capturar relaciones no lineales.
        *   **MLP v1:** Entrenado con 45 características, balanceo de clases (`class_weight='balanced'`, SMOTE), normalización y GridSearchCV para hiperparámetros.
        *   **Resultados MLP v1:** `accuracy` ~53.5%, `F1-macro` ~0.497. Lo más importante: el **`F1-score` para empates fue de 0.26 (recall 0.23, precision 0.29)**. ¡Esto es un avance significativo en la detección de empates respecto a los RF!
    *   **Experimentos con "mover empates":** Has llevado a cabo experimentos útiles para entender el impacto de la composición de los datos (aunque los modelos resultantes no sean para uso final).
    *   La documentación de tus resultados y la persistencia de los modelos (`.pkl`) es impecable.

**4. Partes Pendientes por Desarrollar y Recomendaciones**

Con la sólida base que tienes, las próximas fases se centran en la integración y el despliegue del sistema completo.

*   **4.1. Backend de la API (Servicio Python para Predicciones)**
    *   **Estado:** Se ha utilizado Flask para scripts, pero no como API REST completa.
    *   **Recomendación Clave:** Si bien Flask es funcional, **te sugiero encarecidamente evaluar FastAPI** para la implementación de tu API.
        *   **Ventajas de FastAPI:** Mayor rendimiento (asíncrono con ASGI), validación automática de datos con Pydantic (más robustez), y generación automática de documentación interactiva (OpenAPI/Swagger UI), lo que es profesional y muy útil para el TFG. Dado que ya usas Python y Docker, la curva de aprendizaje no debería ser un impedimento.
    *   **Implementación Propuesta (aplicable a Flask o FastAPI):**
        *   **Diseño de Endpoints:** Al menos `/api/predict` (POST, recibe equipos, fecha opcional) y `/api/teams` (GET, lista de equipos para el frontend).
        *   **Lógica de Predicción:**
            *   **Validación de Entrada:** Asegurar que los equipos existen en la BD.
            *   **Cálculo de Características:** Consulta la BD para obtener las estadísticas históricas (últimos X partidos, H2H) y calcular las características (medias, etc.) exactamente como en `features_engineering.py`.
            *   **Carga del Modelo:** Cargar el modelo final entrenado (`.pkl`) una única vez al inicio del servidor.
            *   **Predicción:** Aplicar la normalización/escalado (si el MLP es el modelo final) e invocar `model.predict()` y `model.predict_proba()`.
            *   **Formato de Respuesta:** Convertir la predicción numérica a un formato legible (ej., "Victoria local", "Empate"), incluyendo probabilidades.
        *   **CORS:** Habilitar CORS para permitir peticiones desde el frontend (que estará en un origen diferente).
    *   **Secuencia de Tareas:**
        1.  Decidir el framework (FastAPI/Flask).
        2.  Configurar la estructura básica del backend y la conexión con SQLAlchemy.
        3.  Implementar `/api/teams` para que el frontend pueda obtener la lista de equipos.
        4.  Crear la lógica de cálculo de características (en una capa de servicio/dominio) que consulte la BD y prepare el vector de entrada para el modelo.
        5.  Integrar la carga del modelo ML en la inicialización del backend.
        6.  Implementar `/api/predict` con la lógica de validación, preparación de features, invocación del modelo y formateo de respuesta.
        7.  Realizar pruebas unitarias y manuales de los endpoints.

*   **4.2. Frontend Web en Angular (Interfaz de Usuario)**
    *   **Estado:** Pendiente de implementación.
    *   **Requerimientos:** Interfaz intuitiva para seleccionar equipos y visualizar la predicción.
    *   **Implementación Propuesta:**
        *   **Componente Principal:** Un `PredictionComponent` para el formulario y el área de resultados.
        *   **Selección de Equipos:** Dropdowns pre-rellenados con datos de `/api/teams`.
        *   **Servicio Angular:** Un `PredictionService` para manejar las llamadas `HttpClient` al backend.
        *   **Visualización:** Mostrar el resultado 1X2 de forma destacada (texto, iconos, colores). Si el backend devuelve probabilidades, visualizarlas (ej., gráfico de barras simple).
        *   **Manejo de Estado/Errores:** Indicadores de carga, mensajes de error.
        *   **Diseño:** Priorizar la claridad y usabilidad.
    *   **Secuencia de Tareas:**
        1.  Generar el proyecto Angular y los componentes/servicios necesarios.
        2.  Diseñar la plantilla HTML del `PredictionComponent`.
        3.  Implementar `PredictionService` para comunicarse con `/api/teams` y `/api/predict`.
        4.  Conectar el componente con el servicio para cargar equipos y disparar predicciones.
        5.  Implementar la visualización de la predicción.
        6.  Realizar pruebas manuales de la interfaz completa (Angular + Backend).

*   **4.3. Integración del Modelo de ML en la Aplicación Web**
    *   **Estado:** El modelo está entrenado y guardado, el backend está por implementar.
    *   **Requerimientos:** Asegurar que el pipeline de datos (Frontend -> Backend -> Modelo -> Backend -> Frontend) funcione sin problemas.
    *   **Consideraciones:**
        *   **Disponibilidad del Modelo:** El archivo `.pkl` debe estar en la imagen Docker del backend. Verificar compatibilidad de versiones de scikit-learn.
        *   **Consistencia de Datos:** Asegurarse de que la base de datos MySQL tenga los datos históricos actualizados (incluyendo 2024 para cálculo de características).
        *   **Pruebas de Integración:** Realizar pruebas end-to-end con datos reales conocidos para verificar el flujo completo.
        *   **Despliegue con Docker Compose:** Configurar un `docker-compose.yml` que orqueste MySQL, el backend Python (con el modelo), y el frontend Angular (servido por Nginx). Esto permitirá levantar todo el sistema con un único comando.
    *   **Secuencia de Tareas:**
        1.  Modificar Dockerfile del backend para incluir el modelo `.pkl` y dependencias ML.
        2.  Construir las imágenes Docker actualizadas para backend y frontend.
        3.  Definir el `docker-compose.yml` con todos los servicios y configuraciones de red.
        4.  Realizar pruebas end-to-end completas (`docker-compose up` y testear la interfaz).
        5.  Documentar el proceso de despliegue.

*   **4.4. Mejora Continua en la Predicción de Empates (Clase Minoritaria)**
    *   **Estado:** Has hecho avances significativos con el MLPClassifier, pero sigue siendo un desafío.
    *   **Importancia:** Mejorar la predicción de empates es clave para la utilidad del sistema y un diferenciador del TFG.
    *   **Estrategias de Mejora (si el tiempo lo permite):**
        *   **Interpretación del Modelo (SHAP):** **¡Esta es mi recomendación más fuerte!** Implementa **SHAP (SHapley Additive exPlanations)** para el modelo final (especialmente si es el MLP). SHAP puede revelar qué características (`media_h2h_goles`, `tendencia_empate_local`, etc.) están influyendo más en la predicción de empates (tanto para los aciertos como para los errores).
            *   **Implementación:** Calcular valores SHAP en el backend (cuando se hace la predicción) y devolverlos al frontend.
            *   **Visualización en Frontend:** Utilizar componentes Angular (`shap-explainers` NPM package) o una visualización personalizada para mostrar el `force_plot` de SHAP al usuario. Esto transformaría tu herramienta de una "caja negra" a un sistema transparente que explica *por qué* predice un resultado.
        *   **Algoritmos Más Potentes:** Experimentar con `XGBoost` o `LightGBM`. Estos modelos suelen ofrecer un rendimiento superior en datos tabulares y tienen funcionalidades para manejar el desbalance de clases.
        *   **Ajuste Fino de Umbrales:** Si el modelo final es probabilístico, puedes experimentar con diferentes umbrales para la clase "empate" para optimizar su recall sin sacrificar demasiada precisión general.
        *   **Nuevas Características:** Explorar indicadores adicionales como la "diferencia de nivel" entre equipos (basado en posiciones en tabla, valor de mercado, etc.) o métricas más granulares de rendimiento.
        *   **Expansión de Datos:** Si es viable, incluir más temporadas de la Premier League o incorporar datos de La Liga (que ya has scrapeado) para aumentar el número de ejemplos de empates.
    *   **Secuencia de Tareas:**
        1.  Implementar la generación de valores SHAP en el backend para el modelo final.
        2.  Analizar los resultados de SHAP para obtener *insights* sobre la predicción de empates.
        3.  (Opcional) Experimentar con XGBoost o ajustar umbrales.
        4.  (Opcional) Generar nuevas características relacionadas con empates.
        5.  Documentar todas las iteraciones y los aprendizajes en la memoria del TFG.

**5. Gestión del Proyecto y Documentación**

*   **Continuar Buenas Prácticas:** Mantener la disciplina con Git/GitHub (commits, ramas) y ClickUp (gestión de tareas).
*   **Pruebas Exhaustivas:** Extender los tests unitarios al backend (endpoints, preprocesamiento) y al frontend (componentes, servicios). Realizar pruebas de integración y funcionales.
*   **Memoria del TFG:** Tu rigor en la documentación previa es una ventaja enorme. Continúa detallando todas las decisiones (por qué Flask/FastAPI, cómo se aplica DDD, por qué ciertas métricas ML, por qué SHAP, etc.). Incluye una **tabla comparativa final de los modelos ML** (como la que te proporcioné en mi primera respuesta, pero rellenando todos los campos con tus resultados finales).

**6. Próximos Pasos Priorizados para el Desarrollo**

Considerando tu progreso, te sugiero el siguiente plan de trabajo priorizado:

1.  **Backend de la API (2-3 semanas):**
    *   **Decisión clave:** Evaluar y elegir **FastAPI** sobre Flask si buscas una solución más moderna y optimizada para APIs de ML.
    *   Implementar `/api/teams` y `/api/predict` (validación, preparación de features, invocación del modelo, formateo de respuesta).
    *   **Integrar la lógica de cálculo de características de `features_engineering.py` en el backend.**
    *   **Cargar el modelo ML (`.pkl`) de forma eficiente** al inicio del servidor.
    *   Pruebas unitarias de la API.
2.  **Frontend Web en Angular (3-4 semanas):**
    *   Desarrollar `PredictionComponent` y `PredictionService`.
    *   Implementar la UI para la selección de equipos y la visualización de resultados.
    *   Conectar el frontend con el backend (`HttpClient`).
    *   Pruebas unitarias y manuales del frontend.
3.  **Integración Completa y Despliegue con Docker Compose (1-2 semanas):**
    *   Asegurar el flujo de datos completo (Frontend -> Backend -> Modelo -> DB -> Frontend).
    *   Configurar `docker-compose.yml` para orquestar todos los servicios (MySQL, Backend, Frontend).
    *   Realizar pruebas end-to-end exhaustivas.
4.  **Refinamiento y Interpretabilidad del Modelo ML (Continuo / 1-2 semanas dedicadas):**
    *   **PRIORIDAD ALTA:** Implementar la **interpretación con SHAP** en el backend para el modelo final.
    *   Explorar cómo visualizar las explicaciones SHAP en Angular (componentes `shap-explainers` o personalizados).
    *   Analizar los insights de SHAP para entender mejor los patrones de empates y posibles nuevas características.
    *   (Opcional) Si el tiempo permite, experimentar brevemente con XGBoost para ver si mejora significativamente la predicción de empates.
5.  **Redacción de la Memoria del TFG (Continuo / 2-3 semanas intensivas al final):**
    *   Consolidar toda la documentación, decisiones, resultados y diagramas.
    *   Enfatizar el proceso iterativo, la solución del scraping y el manejo del desafío de los empates.
    *   Detallar la implementación de DDD y las justificaciones técnicas.

---

**Preguntas para Nuestra Próxima Interacción:**

Para que podamos avanzar de la manera más efectiva, me gustaría que reflexiones sobre lo siguiente:

1.  **Framework para el Backend:** ¿Qué te parecen las ventajas de FastAPI sobre Flask para este proyecto? ¿Te gustaría explorarlo o prefieres mantenerte con Flask por familiaridad y simplicidad en el contexto de un TFG?
2.  **Implementación de DDD:** ¿Has identificado ya los principales *Agregados* y *Servicios de Dominio* en tu modelo? ¿Cómo planeas aplicar los principios de los *Repositorios* para abstraer la persistencia de datos del dominio?
3.  **Visualización de Predicciones y Explicaciones (SHAP):** ¿Tienes alguna idea preliminar sobre cómo te gustaría presentar la predicción 1X2, las probabilidades y, si lo implementas, las explicaciones SHAP al usuario final en la interfaz de Angular? ¿Qué información consideras más relevante para el usuario?

---

docker-compose.yml

```yml
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: mysql_db
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=futbol_TFG
    ports:
      - "3307:3306"
    volumes:
      - db_data:/var/lib/mysql

  minio:
    image: minio/minio
    container_name: minio
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    command: server /data --console-address ":9001"

volumes:
  db_data: {}
  minio_data: {}

```

---
domain/models/base.py

```py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

```
---
domain/models/competicion.py
```py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from domain.models.base import Base

class Competicion(Base):
    __tablename__ = 'competicion'

    competicion_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    abreviatura = Column(String(10), nullable=False)

    # Relación con Temporada
    temporadas = relationship("Temporada", back_populates="competicion")

    def __repr__(self):
        return f"<Competicion(id={self.competicion_id}, nombre={self.nombre} , abreviatura={self.abreviatura})>"



```

---
domain/models/equipo.py
```py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from domain.models.base import Base

class Equipo(Base):
    __tablename__ = "equipo"

    equipo_id = Column(String(20), primary_key=True, nullable=False)    
    nombre = Column(String(100), nullable=False)
    abreviatura = Column(String(10), nullable=False)

    # Relaciones con Partido
    partidos_local = relationship("Partido", back_populates="equipo_local", foreign_keys='Partido.equipo_local_id')
    partidos_visitante = relationship("Partido", back_populates="equipo_visitante", foreign_keys='Partido.equipo_visitante_id')
    # Temporalmente sin foreing_keys
    
    
    def __repr__(self):
        return f"<Equipo(id={self.equipo_id}, nombre='{self.nombre}', abreviatura='{self.abreviatura}')>"



```


---
domain/models/estadisticas_partido_csv.py
```py
from sqlalchemy import Column, String, Float, Integer
from domain.models.base import Base

class EstadisticasPartidoCSV(Base):
    __tablename__ = 'estadisticas_partido_csv'


    partido_id = Column(String(20), primary_key=True)
    equipo_id = Column(String(20), primary_key=True)

    posesion = Column('posesion', Float)
    corners = Column('corners', Integer)
    amarillas = Column('amarillas', Integer)
    rojas = Column('rojas', Integer)


```


---
domain/models/estadisticas_partido.py
```py

from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from domain.models.base import Base


class EstadisticasPartido(Base):
    __tablename__ = 'estadisticas_partido'

    estadisticas_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    partido_id = Column(String(20), ForeignKey('partido.partido_id'), nullable=False, unique=True)
    #partido_id = Column(String(20), nullable=False, unique=True)    para pruebas sin foreing_keys
    posesion_local = Column(Float, nullable=True)
    posesion_visitante = Column(Float, nullable=True)
    
    # de momento vamos a dejar los tiros fuera en el futuro los añadiremos
    #tiros_local = Column(Integer, nullable=True)
    #tiros_visitante = Column(Integer, nullable=True)

    #tiros_puerta_local = Column(Integer, nullable=True)
    #tiros_puerta_visitante = Column(Integer, nullable=True)

    corners_local = Column(Integer, nullable=True)
    corners_visitante = Column(Integer, nullable=True)

    tarjetas_amarillas_local = Column(Integer, nullable=True)
    tarjetas_amarillas_visitante = Column(Integer, nullable=True)

    tarjetas_rojas_local = Column(Integer, nullable=True)
    tarjetas_rojas_visitante = Column(Integer, nullable=True)

    # Relación 1:1 con Partido
    partido = relationship("Partido", back_populates="estadisticas")

    def __repr__(self):
        return f"<EstadisticasPartido(id={self.estadisticas_id}, partido_id={self.partido_id})>"


```


---
domain/models/partido.py
```py
from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from domain.models.base import Base
from domain.models.equipo import Equipo
from domain.models.temporada import Temporada      
from domain.models.competicion import Competicion

class Partido(Base):
    __tablename__ = 'partido'

    partido_id = Column(String(20), primary_key=True, nullable=False)
    fecha = Column(Date, nullable=False)

    equipo_local_id = Column(String(20), ForeignKey('equipo.equipo_id'), nullable=False)
    equipo_visitante_id = Column(String(20), ForeignKey('equipo.equipo_id'), nullable=False)


    # Temporariamente sin foreing_keys para pruebas
    #equipo_local_id = Column(String(20),  nullable=False)
    #equipo_visitante_id = Column(String(20),  nullable=False)

    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)

    temporada_id = Column(String(9), ForeignKey('temporada.temporada_id'), nullable=False)
    competicion_id = Column(Integer, ForeignKey('competicion.competicion_id'), nullable=False)
    
    
    # Temporariamente sin foreing_keys para pruebas
    #temporada_id = Column(String(9),nullable=False)
    #competicion_id = Column(Integer, nullable=False)


    # Relaciones ORM
    equipo_local = relationship("Equipo", foreign_keys=[equipo_local_id])
    equipo_visitante = relationship("Equipo", foreign_keys=[equipo_visitante_id])
    temporada = relationship("Temporada")
    competicion = relationship("Competicion")
    estadisticas = relationship("EstadisticasPartido", uselist=False, back_populates="partido")


    def __repr__(self):
        return (
            f"<Partido(id={self.partido_id}, fecha={self.fecha}, "
            f"local={self.equipo_local_id}, visitante={self.equipo_visitante_id}, "
            f"goles_local={self.goles_local}, goles_visitante={self.goles_visitante}, "
            f"temporada_id={self.temporada_id}, competicion_id={self.competicion_id})>"
        )


```


---
domain/models/temporada.py
```py
from sqlalchemy import Column, Integer, ForeignKey, String, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from domain.models.base import Base  
from domain.models.competicion import Competicion

class Temporada(Base):
    __tablename__ = 'temporada'

    temporada_id = Column(String(9), primary_key=True, nullable=False)
    año_inicio = Column(Integer, nullable=False)
    año_fin = Column(Integer, nullable=False)
    
    
    # pruebas sin foreing_keys
    #competicion_id = Column(Integer, nullable=False)
    
    
    # FK hacia Competición
    competicion_id = Column(Integer, ForeignKey('competicion.competicion_id'), nullable=False)

    # Relación inversa con Partido
    partidos = relationship("Partido", back_populates="temporada")

    # Relación directa con Competición
    competicion = relationship("Competicion", back_populates="temporadas")
    __table_args__ = (
        PrimaryKeyConstraint('temporada_id', 'competicion_id'),
    )
    
    def __repr__(self):
        return f"<Temporada(id={self.temporada_id}, {self.año_inicio}-{self.año_fin}, competicion_id={self.competicion_id})>"


```


---
infra/database/auxestadisticas.py
```py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import text
from infra.database.mysql_connect import get_session
import csv


def insertar_estadisticas_csv():
    session = get_session()

    with open("data/datosFbref/fbref_stats_202505141135.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insert_query = text("""
                INSERT INTO estadisticas_partido_csv (
                    partido_id, equipo_id, posesion, corners, amarillas, rojas
                ) VALUES (:partido_id, :equipo_id, :posesion, :corners, :amarillas, :rojas)
            """)
            session.execute(insert_query, {
                'partido_id': row["match_id"],
                'equipo_id': row["team_id"],
                'posesion': float(row["team_match_possession"] or 0),
                'corners': int(row["team_match_corners"] or 0),
                'amarillas': int(row["team_match_yellow_cards"] or 0),
                'rojas': int(row["team_match_red_cards"] or 0)
            })

    session.commit()
    session.close()
    print(" Datos insertados en estadisticas_partido_csv con SQLAlchemy.")

if __name__ == "__main__":
    insertar_estadisticas_csv()



```


---
infra/database/bdestadisticas.py
```py
    import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import and_
from sqlalchemy.orm import aliased
from infra.database.mysql_connect import get_session
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido
from domain.models.estadisticas_partido_csv import EstadisticasPartidoCSV

def main():
    session = get_session()

    e1 = aliased(EstadisticasPartidoCSV)
    e2 = aliased(EstadisticasPartidoCSV)

    query = (
        session.query(
            Partido.partido_id,
            e1.posesion.label("posesion_local"),
            e2.posesion.label("posesion_visitante"),
            e1.corners.label("corners_local"),
            e2.corners.label("corners_visitante"),
            e1.amarillas.label("tarjetas_amarillas_local"),
            e2.amarillas.label("tarjetas_amarillas_visitante"),
            e1.rojas.label("tarjetas_rojas_local"),
            e2.rojas.label("tarjetas_rojas_visitante"),
        )
        .outerjoin(e1, and_(Partido.partido_id == e1.partido_id, Partido.equipo_local_id == e1.equipo_id))
        .outerjoin(e2, and_(Partido.partido_id == e2.partido_id, Partido.equipo_visitante_id == e2.equipo_id))
    )

    for row in query.all():
        estadistica = EstadisticasPartido(
            partido_id=row.partido_id,
            posesion_local=row.posesion_local,
            posesion_visitante=row.posesion_visitante,
            corners_local=row.corners_local,
            corners_visitante=row.corners_visitante,
            tarjetas_amarillas_local=row.tarjetas_amarillas_local,
            tarjetas_amarillas_visitante=row.tarjetas_amarillas_visitante,
            tarjetas_rojas_local=row.tarjetas_rojas_local,
            tarjetas_rojas_visitante=row.tarjetas_rojas_visitante,
        )
        session.add(estadistica)  #  Esto debe estar dentro del bucle

    session.commit()
    session.close()
    print(" Datos insertados correctamente en estadisticas_partido.")

if __name__ == "__main__":
    main()


```

---
infra/database/generarDataset.py
```py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
from infra.database.mysql_connect import get_engine  
from dotenv import load_dotenv

# Cargar variables del entorno
load_dotenv()

# Crear motor de conexión a MySQL
engine = get_engine()

# Consulta SQL
query = """
SELECT 
    p.partido_id,
    p.fecha,
    el.nombre AS nombre_equipo_local,
    ev.nombre AS nombre_equipo_visitante,
    p.goles_local,
    p.goles_visitante,
    ep.posesion_local,
    ep.posesion_visitante,
    ep.corners_local,
    ep.corners_visitante,
    ep.tarjetas_amarillas_local,
    ep.tarjetas_amarillas_visitante,
    ep.tarjetas_rojas_local,
    ep.tarjetas_rojas_visitante,
    t.temporada_id AS temporada,
    c.nombre AS competicion
FROM partido p
JOIN estadisticas_partido ep ON p.partido_id = ep.partido_id
JOIN equipo el ON p.equipo_local_id = el.equipo_id
JOIN equipo ev ON p.equipo_visitante_id = ev.equipo_id
JOIN temporada t ON p.temporada_id = t.temporada_id
JOIN competicion c ON p.competicion_id = c.competicion_id;
"""

# Leer la consulta en un DataFrame
df = pd.read_sql(query, engine)

# Crear la variable objetivo "resultado"
df["resultado"] = df.apply(
    lambda row: 1 if row.goles_local > row.goles_visitante
    else -1 if row.goles_local < row.goles_visitante
    else 0,
    axis=1
)

# Eliminar posibles duplicados por partido_id
df.drop_duplicates(subset="partido_id", keep="first", inplace=True)
df.sort_values(by="fecha", inplace=True)

# Crear carpeta 'data/' si no existe
os.makedirs("data", exist_ok=True)

# Guardar el CSV
df.to_csv("data/dataset_partidos.csv", index=False, encoding="utf-8")
print("Dataset generado correctamente en 'data/dataset_partidos.csv'")

```

---
infra/database/mysql_connect.py
```py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables desde el .env
load_dotenv()

# Leer credenciales desde variables de entorno
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# Crear el engine y el sessionmaker a nivel global
url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(url)
Session = sessionmaker(bind=engine)

# Funciones accesibles desde otros módulos
def get_engine():
    return engine

def get_session():
    return Session()


```

---
infra/database/testprueba.py
```py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import csv
from datetime import datetime
from infra.database.mysql_connect import get_session
from domain.models.competicion import Competicion
from domain.models.equipo import Equipo
from domain.models.temporada import Temporada
from domain.models.partido import Partido

# Rutas de los CSV
csv_competitions = "data/datosFbref/fbref_competitions_202505141101.csv"
csv_teams = "data/datosFbref/fbref_teams_202505141059.csv"
csv_seasons = "data/datosFbref/fbref_seasons_202505141100.csv"
csv_matches = "data/datosFbref/fbref_matches_202505141101.csv"

def abreviar_equipo(nombre):
    if not nombre or not nombre.strip():
        return "UNK"
    palabras = nombre.strip().split()
    if len(nombre) <= 4:
        return nombre.upper()
    elif len(palabras) == 1:
        return nombre[:3].upper()
    else:
        abrev = ''.join(p[0].upper() for p in palabras if p.lower() not in ['fc', 'cf', 'cd', 'de'])
        return abrev if abrev else "UNK"

def main():
    session = get_session()

    #  Insertar COMPETICIONES (solo última ocurrencia por ID)
    with open(csv_competitions, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        ultima_competicion = {}
        for row in reader:
            comp_id = row["competition_id"]
            ultima_competicion[comp_id] = row

        for comp_id, row in ultima_competicion.items():
            nombre = row["competition_name"]
            abreviatura = abreviar_equipo(nombre)
            competicion = Competicion(
                competicion_id=comp_id,
                nombre=nombre,
                abreviatura=abreviatura
            )
            session.add(competicion)

    # 🏟 Insertar EQUIPOS
    with open(csv_teams, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nombre = row["name"]
            equipo = Equipo(
                equipo_id=row["team_id"],
                nombre=nombre,
                abreviatura=abreviar_equipo(nombre)
            )
            session.add(equipo)

    #  Insertar TEMPORADAS
    with open(csv_seasons, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            temporada = Temporada(
                competicion_id=row["competition_id"],
                temporada_id=row["season"],
                año_inicio=row["starting_year"],
                año_fin=row["ending_year"]
            )
            session.add(temporada)

    #  Insertar PARTIDOS
    with open(csv_matches, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            partido = Partido(
                partido_id=row["match_id"],
                fecha=datetime.fromisoformat(row["start_datetime"]),
                equipo_local_id=row["home_team_id"],
                equipo_visitante_id=row["away_team_id"],
                goles_local=int(row["home_goals"]),
                goles_visitante=int(row["away_goals"]),
                competicion_id=row["competition_id"],
                temporada_id=row["season"]
            )
            session.add(partido)

    #  Guardar cambios
    session.commit()
    session.close()
    print(" Todos los datos han sido cargados correctamente.")

if __name__ == "__main__":
    main()


```


---
infra/minio/minio_client.py
```py

from minio import Minio

def create_minio_client():
    client = Minio(
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    return client



```


---
infra/ml/mlpclassifier/entrenar_modelo_mlpclassifier1.py
```py
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


```


---
infra/ml/mlpclassifier/entrenar_modelo_mlpclassifier2.py
```py

import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
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

# Mover empates del test al train
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

# ------------------- OVERSAMPLING -------------------
ros = RandomOverSampler(random_state=42)
X_train_bal, y_train_bal = ros.fit_resample(X_train, y_train)
X_train_bal, y_train_bal = shuffle(X_train_bal, y_train_bal, random_state=42)

print(f"Partidos para entrenamiento (después de oversampling): {len(X_train_bal)}")

# ------------------- NORMALIZACIÓN ------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_bal)
X_test_scaled = scaler.transform(X_test)

# ----------------- DEFINICIÓN DEL MODELO ------------------
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
model = grid_search.best_estimator_

# ----------------- EVALUACIÓN ------------------
y_pred = model.predict(X_test_scaled)

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
joblib.dump(model, "modelos/mlpclassifier/modelo_mlp2.pkl")
joblib.dump(scaler, "modelos/mlpclassifier/scaler_mlp2.pkl")
print("Modelo guardado como 'modelos/mlpclassifier/modelo_mlp2.pkl'")
print("Scaler guardado como 'modelos/mlpclassifier/scaler_mlp2.pkl'")

```


---
infra/ml/mlpclassifier/entrenar_modelo_mlpclassifier3.py
```py
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
import joblib
import os

# ------------------ CARGA DE DATOS ------------------
df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

features = [col for col in df.columns if col.startswith((
    "media_ult10_", "media_h2h_", "media_hist_",
    "diferencia_", "racha_", "media_hist_goles_", "tendencia_empate_"
))]

print("\nVariables predictoras utilizadas:")
for col in features:
    print(f" - {col}")

# Eliminar filas con valores nulos
df = df.dropna(subset=["resultado"] + features)

# ------------------ DIVISIÓN TEMPORAL ------------------
df_train = df[df["fecha"].dt.year < 2024]
df_test = df[df["fecha"].dt.year == 2024]

# Mover empates del test al train
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

# ------------------- OVERSAMPLING -------------------
ros = RandomOverSampler(random_state=42)
X_train_bal, y_train_bal = ros.fit_resample(X_train, y_train)
X_train_bal, y_train_bal = shuffle(X_train_bal, y_train_bal, random_state=42)

print(f"Partidos para entrenamiento (después de oversampling): {len(X_train_bal)}")

# ------------------- NORMALIZACIÓN ------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_bal)
X_test_scaled = scaler.transform(X_test)

# ----------------- DEFINICIÓN DEL MODELO ------------------
param_grid = {
    'hidden_layer_sizes': [(100,), (100, 50), (150, 100, 50), (200, 100)],
    'activation': ['relu', 'tanh'],
    'solver': ['adam', 'lbfgs'],
    'alpha': [1e-5, 1e-4, 1e-3],
    'learning_rate': ['constant', 'adaptive'],
    'learning_rate_init': [0.001, 0.01]
}

grid_search = GridSearchCV(
    estimator=MLPClassifier(max_iter=3000, early_stopping=True, n_iter_no_change=30, random_state=42),
    param_grid=param_grid,
    scoring='f1_macro',
    cv=5,
    verbose=1,
    n_jobs=-1
)

grid_search.fit(X_train_scaled, y_train_bal)
model = grid_search.best_estimator_

# ----------------- EVALUACIÓN ------------------
y_pred = model.predict(X_test_scaled)

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
#os.makedirs("modelos/mlpclassifier", exist_ok=True)
#joblib.dump(model, "modelos/mlpclassifier/modelo_mlp3.pkl")
#joblib.dump(scaler, "modelos/mlpclassifier/scaler_mlp3.pkl")
#print("Modelo guardado como 'modelos/mlpclassifier/modelo_mlp3.pkl'")
#print("Scaler guardado como 'modelos/mlpclassifier/scaler_mlp3.pkl'")


```


---
infra/ml/random_forest/entrenar_modelo1.py
```py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import joblib
import os

# Cargar el dataset
df = pd.read_csv("data/dataset_partidos.csv", parse_dates=["fecha"])

# Filtrar por año para dividir entrenamiento y prueba
df["anio"] = df["fecha"].dt.year
df_train = df[df["anio"] <= 2023].copy()
df_test = df[df["anio"] == 2024].copy()

print(f"Partidos para entrenamiento: {len(df_train)}")
print(f"Partidos para prueba: {len(df_test)}")

# Selección de variables
features = [
    "posesion_local", "posesion_visitante",
    "corners_local", "corners_visitante",
    "tarjetas_amarillas_local", "tarjetas_amarillas_visitante",
    "tarjetas_rojas_local", "tarjetas_rojas_visitante"
]

X_train = df_train[features]
y_train = df_train["resultado"]

X_test = df_test[features]
y_test = df_test["resultado"]

# Entrenar modelo Random Forest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Evaluación del modelo
y_pred = modelo.predict(X_test)

print("\n Resultados del modelo:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

# Guardar modelo como .pkl
os.makedirs("modelos", exist_ok=True)
joblib.dump(modelo, "modelos/random_forest/modelo_randomforest.pkl")
print("\nModelo guardado en 'modelos/random_forest/modelo_randomforest.pkl'")



```

---
infra/ml/random_forest/entrenar_modelo2.py
```py

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
joblib.dump(modelo, "modelos/random_forest/modelo_randomforest3.pkl")
print("\nModelo guardado en 'modelos/random_forest/modelo_randomforest3.pkl'")



```

---
infra/ml/random_forest/entrenar_modelo3.py
```py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import os

# Cargar dataset enriquecido
df = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])

# Filtrar y preparar columnas
features = [col for col in df.columns if col.startswith("media_")]
X = df[features]
y = df["resultado"]

# Separar en entrenamiento (hasta 2023) y prueba (2024)
X_train = X[df["fecha"].dt.year < 2024]
y_train = y[df["fecha"].dt.year < 2024]

X_test = X[df["fecha"].dt.year == 2024]
y_test = y[df["fecha"].dt.year == 2024]

print(f"\nPartidos para entrenamiento: {len(X_train)}")
print(f"Partidos para prueba: {len(X_test)}")

# Definir parámetros para Grid Search
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'max_features': ['sqrt', 'log2']
}

# Crear el clasificador base
clf = RandomForestClassifier(random_state=42)

# Ejecutar Grid Search
grid_search = GridSearchCV(clf, param_grid, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

# Evaluar el mejor modelo encontrado
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

# Guardar el modelo
os.makedirs("modelos", exist_ok=True)
joblib.dump(mejor_modelo, "modelos/random_forest/modelo_randomforest3.pkl")
print(" Modelo guardado como 'modelos/random_forest/modelo_randomforest3.pkl'")



```
---
infra/ml/random_forest/entrenar_modelo4.py
```py

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
joblib.dump(model, "modelos/random_forest/modelo_randomforest4.pkl")
print(" Modelo guardado como 'modelos/random_forest/modelo_randomforest4.pkl'")



```
---
infra/ml/random_forest/entrenar_modelo5.py
```py

import pandas as pd
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



```

---
infra/ml/random_forest/ver_modelo.py
```py

import joblib
import os
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')  # Fuerza uso sin GUI (evita error Tcl)
import matplotlib.pyplot as plt

# Ruta al modelo que quieres analizar
MODELO_PATH = "modelos/random_forest/modelo_randomforest5.pkl"

# Ruta al dataset que se usó para entrenar el modelo
DATASET_PATH = "data/dataset_partidos_enriquecido.csv"

# ================= CARGAR MODELO ====================
if not os.path.exists(MODELO_PATH):
    print(f" No se encontró el modelo en {MODELO_PATH}")
    exit()

modelo = joblib.load(MODELO_PATH)
print(f"\n Modelo cargado: {MODELO_PATH}")
print(f"Tipo: {type(modelo)}")

# ================= CARGAR DATASET ===================
if not os.path.exists(DATASET_PATH):
    print(f" No se encontró el dataset en {DATASET_PATH}")
    exit()

df = pd.read_csv(DATASET_PATH)
features = [col for col in df.columns if col.startswith((
    "media_ult10_", "media_h2h_", "media_hist_",
    "diferencia_", "racha_", "media_hist_goles_", "tendencia_empate_"
))]


# ================= INFO DEL MODELO ==================
if hasattr(modelo, "feature_importances_"):
    importancias = modelo.feature_importances_
    importancia_df = pd.DataFrame({
        "feature": features,
        "importancia": importancias
    }).sort_values(by="importancia", ascending=False)

    print("\n Importancia de variables:")
    print(importancia_df.to_string(index=False))

    # ======== VISUALIZACIÓN ==========
    plt.figure(figsize=(10, 6))
    importancia_df.sort_values("importancia").plot.barh(x="feature", y="importancia", legend=False)
    plt.title("Importancia de variables (Random Forest)")
    plt.xlabel("Importancia relativa")
    plt.tight_layout()
    # Crear carpeta si no existe
    os.makedirs("graficas", exist_ok=True)

    # Guardar imagen
    plt.savefig("graficas/importancia_variables_modelo5.png", dpi=300)
    print("Gráfico guardado en 'graficas/importancia_variables_modelo5.png'")


else:
    print(" Este modelo no tiene atributo 'feature_importances_' (¿no es un árbol?).")



```


---
infra/ml/features_engineering.py
```py

import pandas as pd
import numpy as np
import os
from tqdm import tqdm

# Cargar el dataset original
df = pd.read_csv("data/dataset_partidos.csv", parse_dates=["fecha"])
df.sort_values(by="fecha", inplace=True)
df.reset_index(drop=True, inplace=True)

# Columnas estadísticas a promediar
estadisticas = [
    "posesion_local", "posesion_visitante",
    "corners_local", "corners_visitante",
    "tarjetas_amarillas_local", "tarjetas_amarillas_visitante",
    "tarjetas_rojas_local", "tarjetas_rojas_visitante"
]

# Crear nuevas columnas para las medias
for var in estadisticas:
    df[f"media_ult10_{var}"] = np.nan  # se rellenarán después

# Recorremos cada partido para calcular las medias históricas
for i, row in tqdm(df.iterrows(), total=len(df)):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    # Partidos anteriores del equipo local
    ultimos_local = df[
        ((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    # Partidos anteriores del equipo visitante
    ultimos_visitante = df[
        ((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    # Pruebas que funciona correctamente 
    if equipo_local == "Arsenal" and equipo_visitante == "Tottenham":
        print(fecha_actual)
        print("Últimos 10 Arsenal:", ultimos_local[["fecha", "nombre_equipo_local", "nombre_equipo_visitante"]])
        print("Últimos 10 Tottenham:", ultimos_visitante[["fecha", "nombre_equipo_local", "nombre_equipo_visitante"]])

    # Calcular medias para cada variable
    for var in estadisticas:
        if "local" in var:
            valores = ultimos_local[var].dropna()
        else:
            valores = ultimos_visitante[var].dropna()

        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_ult10_{var}"] = media

# ---------------SEGUNDA FASE: añadir medias de últimos 10 enfrentamientos directos----------------
h2h_vars = estadisticas  # mismas estadísticas
df["tendencia_empate_h2h"] = np.nan

# Crear nuevas columnas para enfrentamientos directos
for var in h2h_vars:
    df[f"media_h2h_{var}"] = np.nan

# Recorremos nuevamente para calcular enfrentamientos directos
for i, row in tqdm(df.iterrows(), total=len(df), desc="H2H"):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    # Buscar últimos 10 enfrentamientos entre ambos equipos antes de la fecha actual
    enfrentamientos = df[
        (
            ((df["nombre_equipo_local"] == equipo_local) & (df["nombre_equipo_visitante"] == equipo_visitante)) |
            ((df["nombre_equipo_local"] == equipo_visitante) & (df["nombre_equipo_visitante"] == equipo_local))
        ) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    # Pruebas que funciona correctamente
    if equipo_local == "Arsenal" and equipo_visitante == "Tottenham":
        print(fecha_actual)
        print("H2H Arsenal-Tottenham:", enfrentamientos[["fecha", "nombre_equipo_local", "nombre_equipo_visitante"]])
    
    # Calcular medias
    for var in h2h_vars:
        valores = enfrentamientos[var].dropna()
        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_h2h_{var}"] = media

    # Calcular tendencia de empate en los últimos H2H
    if not enfrentamientos.empty:
        empates_h2h = (enfrentamientos["resultado"] == 0).sum()
        df.at[i, "tendencia_empate_h2h"] = empates_h2h / len(enfrentamientos)
    else:
        df.at[i, "tendencia_empate_h2h"] = np.nan

# -------- TERCERA FASE: medias históricas acumuladas -----
for var in estadisticas:
    df[f"media_hist_{var}"] = np.nan

print(" Añadiendo medias históricas acumuladas por equipo...")

for i, row in tqdm(df.iterrows(), total=len(df), desc="Histórico"):
    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    partidos_local = df[
        ((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) &
        (df["fecha"] < fecha_actual)
    ]

    partidos_visitante = df[
        ((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) &
        (df["fecha"] < fecha_actual)
    ]

    for var in estadisticas:
        if "local" in var:
            valores = partidos_local[var].dropna()
        else:
            valores = partidos_visitante[var].dropna()

        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_hist_{var}"] = media

# ----------------CUARTA FASE: diferencia de goles en todos los contextos---------------------
print(" Calculando diferencias de goles...")

# Añadir columnas vacías
for prefijo in ["media_ult10", "media_h2h", "media_hist"]:
    df[f"{prefijo}_diferencia_goles_local"] = np.nan
    df[f"{prefijo}_diferencia_goles_visitante"] = np.nan

for i, row in tqdm(df.iterrows(), total=len(df), desc="Diferencia Goles"):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    # Últimos 10 partidos
    ult_local = df[((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) & (df["fecha"] < fecha_actual)].sort_values(by="fecha", ascending=False).head(10)
    ult_visit = df[((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) & (df["fecha"] < fecha_actual)].sort_values(by="fecha", ascending=False).head(10)

    def diferencia(partidos, equipo):
        difs = []
        for _, p in partidos.iterrows():
            if p["nombre_equipo_local"] == equipo:
                difs.append(p["goles_local"] - p["goles_visitante"])
            elif p["nombre_equipo_visitante"] == equipo:
                difs.append(p["goles_visitante"] - p["goles_local"])
        return np.mean(difs) if difs else np.nan

    df.at[i, "media_ult10_diferencia_goles_local"] = diferencia(ult_local, equipo_local)
    df.at[i, "media_ult10_diferencia_goles_visitante"] = diferencia(ult_visit, equipo_visitante)

    # H2H
    h2h = df[
        (
            ((df["nombre_equipo_local"] == equipo_local) & (df["nombre_equipo_visitante"] == equipo_visitante)) |
            ((df["nombre_equipo_local"] == equipo_visitante) & (df["nombre_equipo_visitante"] == equipo_local))
        ) & (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    df.at[i, "media_h2h_diferencia_goles_local"] = diferencia(h2h, equipo_local)
    df.at[i, "media_h2h_diferencia_goles_visitante"] = diferencia(h2h, equipo_visitante)

    # Históricos
    hist_local = df[((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) & (df["fecha"] < fecha_actual)]
    hist_visit = df[((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) & (df["fecha"] < fecha_actual)]

    df.at[i, "media_hist_diferencia_goles_local"] = diferencia(hist_local, equipo_local)
    df.at[i, "media_hist_diferencia_goles_visitante"] = diferencia(hist_visit, equipo_visitante)

# ----------------QUINTA FASE: rachas + diferencias de estadísticas ---------------------
print(" Añadiendo rachas y diferencias de estadísticas...")

# Inicializar nuevas columnas
df["racha_ganados_local_ult5"] = np.nan
df["racha_ganados_visitante_ult5"] = np.nan
df["diferencia_posesion"] = df["posesion_local"] - df["posesion_visitante"]
df["diferencia_corners"] = df["corners_local"] - df["corners_visitante"]
df["diferencia_tarjetas_amarillas"] = df["tarjetas_amarillas_local"] - df["tarjetas_amarillas_visitante"]
df["diferencia_tarjetas_rojas"] = df["tarjetas_rojas_local"] - df["tarjetas_rojas_visitante"]
df["media_hist_goles_local_a_favor"] = np.nan
df["media_hist_goles_local_en_contra"] = np.nan
df["racha_empates_local_ult5"] = np.nan
df["racha_derrotas_local_ult5"] = np.nan
df["racha_empates_visitante_ult5"] = np.nan
df["racha_derrotas_visitante_ult5"] = np.nan
df["goles_local_ult5_media"] = np.nan
df["goles_visitante_ult5_media"] = np.nan
df["tendencia_empate_local"] = np.nan
df["tendencia_empate_visitante"] = np.nan



for i, row in tqdm(df.iterrows(), total=len(df), desc="Rachas y diferencias"):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    ult5_local = df[
        ((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(5)

    ult5_visit = df[
        ((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(5)

    def ganados(partidos, equipo):
        count = 0
        for _, p in partidos.iterrows():
            if p["resultado"] == 1 and p["nombre_equipo_local"] == equipo:
                count += 1
            elif p["resultado"] == -1 and p["nombre_equipo_visitante"] == equipo:
                count += 1
        return count

    df.at[i, "racha_ganados_local_ult5"] = ganados(ult5_local, equipo_local)
    df.at[i, "racha_ganados_visitante_ult5"] = ganados(ult5_visit, equipo_visitante)

    # Históricos del equipo local solo jugando en casa
    partidos_local_en_casa = df[
        (df["nombre_equipo_local"] == equipo_local) & (df["fecha"] < fecha_actual)
    ]
    df.at[i, "media_hist_goles_local_a_favor"] = partidos_local_en_casa["goles_local"].mean() if not partidos_local_en_casa.empty else np.nan
    df.at[i, "media_hist_goles_local_en_contra"] = partidos_local_en_casa["goles_visitante"].mean() if not partidos_local_en_casa.empty else np.nan

        # Nuevas funciones auxiliares
    def empates(partidos, equipo):
        count = 0
        for _, p in partidos.iterrows():
            if p["resultado"] == 0 and (p["nombre_equipo_local"] == equipo or p["nombre_equipo_visitante"] == equipo):
                count += 1
        return count

    def derrotas(partidos, equipo):
        count = 0
        for _, p in partidos.iterrows():
            if p["resultado"] == -1 and p["nombre_equipo_local"] == equipo:
                count += 1
            elif p["resultado"] == 1 and p["nombre_equipo_visitante"] == equipo:
                count += 1
        return count

    # Nuevas variables: rachas de empates y derrotas
    df.at[i, "racha_empates_local_ult5"] = empates(ult5_local, equipo_local)
    df.at[i, "racha_derrotas_local_ult5"] = derrotas(ult5_local, equipo_local)
    df.at[i, "racha_empates_visitante_ult5"] = empates(ult5_visit, equipo_visitante)
    df.at[i, "racha_derrotas_visitante_ult5"] = derrotas(ult5_visit, equipo_visitante)

    # Nuevas variables: media de goles en últimos 5 partidos
    df.at[i, "goles_local_ult5_media"] = ult5_local.apply(
        lambda p: p["goles_local"] if p["nombre_equipo_local"] == equipo_local else p["goles_visitante"],
        axis=1
    ).mean()
    
    df.at[i, "goles_visitante_ult5_media"] = ult5_visit.apply(
        lambda p: p["goles_visitante"] if p["nombre_equipo_visitante"] == equipo_visitante else p["goles_local"],
        axis=1
    ).mean()


    # % de empates en los últimos 10 partidos
    ult10_local = df[((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) & (df["fecha"] < fecha_actual)].sort_values(by="fecha", ascending=False).head(10)
    ult10_visit = df[((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) & (df["fecha"] < fecha_actual)].sort_values(by="fecha", ascending=False).head(10)

    empate_local = (ult10_local["resultado"] == 0).sum()
    empate_visit = (ult10_visit["resultado"] == 0).sum()

    df.at[i, "tendencia_empate_local"] = empate_local / len(ult10_local) if len(ult10_local) > 0 else np.nan
    df.at[i, "tendencia_empate_visitante"] = empate_visit / len(ult10_visit) if len(ult10_visit) > 0 else np.nan




# Verificar columnas esperadas en el dataset enriquecido
columnas_esperadas = [
    "media_ult10_diferencia_goles_local", "media_ult10_diferencia_goles_visitante",
    "media_h2h_diferencia_goles_local", "media_h2h_diferencia_goles_visitante",
    "media_hist_diferencia_goles_local", "media_hist_diferencia_goles_visitante"
]

print("\n Verificando columnas de diferencia de goles...")
faltantes = [col for col in columnas_esperadas if col not in df.columns]

if not faltantes:
    print(" Todas las columnas de diferencia de goles están presentes.")
else:
    print(" Faltan columnas en el dataset:", faltantes)

# Opcional: mostrar valores de ejemplo
print("\n Ejemplo de diferencias de goles y rachas (últimos 5 partidos):")
print(df[[
    "fecha", "nombre_equipo_local", "nombre_equipo_visitante",
    "media_ult10_diferencia_goles_local", "media_ult10_diferencia_goles_visitante",
    "racha_ganados_local_ult5", "racha_empates_local_ult5", "racha_derrotas_local_ult5",
    "racha_ganados_visitante_ult5", "racha_empates_visitante_ult5", "racha_derrotas_visitante_ult5",
    "goles_local_ult5_media", "goles_visitante_ult5_media"
]].tail(5))


# Crear carpeta de salida
os.makedirs("data", exist_ok=True)

# Guardar el nuevo dataset enriquecido
df.to_csv("data/dataset_partidos_enriquecido.csv", index=False)
print("Dataset enriquecido guardado como 'data/dataset_partidos_enriquecido.csv'")


```
requirements.txt
```txt


argon2-cffi==23.1.0
argon2-cffi-bindings==21.2.0
beautifulsoup4==4.13.3
bs4==0.0.2
certifi==2025.1.31
cffi==1.17.1
charset-normalizer==3.4.1
cloudscraper==1.2.71
colorama==0.4.6
contourpy==1.3.2
cycler==0.12.1
fake-useragent==2.2.0
fonttools==4.58.0
greenlet==3.1.1
idna==3.10
imbalanced-learn==0.13.0
joblib==1.5.0
kiwisolver==1.4.8
matplotlib==3.10.3
minio==7.2.15
mysql-connector-python==9.2.0
numpy==2.2.4
packaging==25.0
pandas==2.2.3
pillow==11.2.1
pycparser==2.22
pycryptodome==3.22.0
PyMySQL==1.1.1
pyparsing==3.2.3
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
pytz==2025.2
requests==2.32.3
requests-toolbelt==1.0.0
scikit-learn==1.6.1
scipy==1.15.3
six==1.17.0
sklearn-compat==0.1.3
soupsieve==2.6
SQLAlchemy==2.0.40
threadpoolctl==3.6.0
tqdm==4.67.1
typing_extensions==4.13.1
tzdata==2025.2
urllib3==2.4.0

```
