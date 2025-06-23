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
---
backend/repositories/partido_repository.py
```py
# backend/repositories/partido_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Tuple
from datetime import date

# Importa tus modelos ORM
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido # Asegura la importación

class PartidoRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_historical_matches_with_stats(self, team_id: str, before_date: date, limit: Optional[int] = None) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """
        Obtiene partidos históricos para un equipo con sus estadísticas, antes de una fecha específica.
        Retorna una lista de tuplas (Partido, EstadisticasPartido).
        """
        query = self.db_session.query(Partido, EstadisticasPartido).\
            outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id).\
            filter(
                or_(Partido.equipo_local_id == team_id, Partido.equipo_visitante_id == team_id),
                Partido.fecha < before_date
            ).\
            order_by(Partido.fecha.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_h2h_matches_with_stats(self, team1_id: str, team2_id: str, before_date: date, limit: Optional[int] = None) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """
        Obtiene enfrentamientos directos (H2H) entre dos equipos con sus estadísticas, antes de una fecha específica.
        Retorna una lista de tuplas (Partido, EstadisticasPartido).
        """
        query = self.db_session.query(Partido, EstadisticasPartido).\
            outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id).\
            filter(
                or_(
                    and_(Partido.equipo_local_id == team1_id, Partido.equipo_visitante_id == team2_id),
                    and_(Partido.equipo_local_id == team2_id, Partido.equipo_visitante_id == team1_id)
                ),
                Partido.fecha < before_date
            ).\
            order_by(Partido.fecha.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_team_home_matches_with_stats(self, team_id: str, before_date: date) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """
        Obtiene partidos históricos donde un equipo fue local, con sus estadísticas.
        """
        query = self.db_session.query(Partido, EstadisticasPartido).\
            outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id).\
            filter(
                Partido.equipo_local_id == team_id,
                Partido.fecha < before_date
            ).\
            order_by(Partido.fecha.desc())
        return query.all()

    # Puedes añadir un método para obtener las estadísticas del partido actual si las necesitaras en las features
    # def get_match_stats_by_id(self, partido_id: str) -> Optional[EstadisticasPartido]:
    #     return self.db_session.query(EstadisticasPartido).filter(EstadisticasPartido.partido_id == partido_id).first()


```
---
backend/repositories/team_repository.py
```py

# backend/repositories/team_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional

# Importa tu modelo ORM Equipo
from domain.models.equipo import Equipo

class TeamRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_teams(self) -> List[Equipo]:
        """Obtiene todos los equipos de la base de datos, ordenados por nombre."""
        return self.db_session.query(Equipo).order_by(Equipo.nombre).all()

    def get_team_by_name(self, name: str) -> Optional[Equipo]:
        """Obtiene un equipo por su nombre."""
        return self.db_session.query(Equipo).filter(Equipo.nombre == name).first()

    def get_team_by_id(self, team_id: str) -> Optional[Equipo]:
        """Obtiene un equipo por su ID."""
        return self.db_session.query(Equipo).filter(Equipo.equipo_id == team_id).first()

```
---
backend/services/prediction_service.py
```py

# backend/services/prediction_service.py
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
# Asegúrate que el tipo de clasificador coincide con tu modelo cargado (.pkl)
# Tu docker-compose.yml apunta a 'modelo_randomforest5.pkl', por lo que usamos RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
# Si tu modelo cargado es MLPClassifier, usa:
# from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional, Tuple, Union # Añadido Union para el type hinting del modelo
from datetime import date

from backend.repositories.partido_repository import PartidoRepository
from backend.repositories.team_repository import TeamRepository
# No es necesario importar Partido o EstadisticasPartido aquí directamente,
# ya que vienen como tuplas desde el repositorio.
# from domain.models.partido import Partido
# from domain.models.estadisticas_partido import EstadisticasPartido

class PredictionService:
    # Esta lista debe ser EXACTAMENTE la que usa tu modelo entrenado.
    # Obtén la lista 'features' de tu script 'entrenar_modelo5.py' (o el que usaste para el modelo final).
    _MODEL_FEATURES = [
        "media_ult10_posesion_local", "media_ult10_posesion_visitante",
        "media_ult10_corners_local", "media_ult10_corners_visitante",
        "media_ult10_tarjetas_amarillas_local", "media_ult10_tarjetas_amarillas_visitante",
        "media_ult10_tarjetas_rojas_local", "media_ult10_tarjetas_rojas_visitante",
        "media_h2h_posesion_local", "media_h2h_posesion_visitante",
        "media_h2h_corners_local", "media_h2h_corners_visitante",
        "media_h2h_tarjetas_amarillas_local", "media_h2h_tarjetas_amarillas_visitante",
        "media_h2h_tarjetas_rojas_local", "media_h2h_tarjetas_rojas_visitante",
        "tendencia_empate_h2h",
        "media_hist_posesion_local", "media_hist_posesion_visitante",
        "media_hist_corners_local", "media_hist_corners_visitante",
        "media_hist_tarjetas_amarillas_local", "media_hist_tarjetas_amarillas_visitante",
        "media_hist_tarjetas_rojas_local", "media_hist_tarjetas_rojas_visitante",
        "media_ult10_diferencia_goles_local", "media_ult10_diferencia_goles_visitante",
        "media_h2h_diferencia_goles_local", "media_h2h_diferencia_goles_visitante",
        "media_hist_diferencia_goles_local", "media_hist_diferencia_goles_visitante",
        "racha_ganados_local_ult5", "racha_ganados_visitante_ult5",
        "diferencia_posesion", "diferencia_corners",
        "diferencia_tarjetas_amarillas", "diferencia_tarjetas_rojas",
        "media_hist_goles_local_a_favor", "media_hist_goles_local_en_contra",
        "racha_empates_local_ult5", "racha_derrotas_local_ult5",
        "racha_empates_visitante_ult5", "racha_derrotas_visitante_ult5",
        "goles_local_ult5_media", "goles_visitante_ult5_media",
        "tendencia_empate_local", "tendencia_empate_visitante"
    ]

    def __init__(self, db_session: Session):
        self.partido_repo = PartidoRepository(db_session)
        self.team_repo = TeamRepository(db_session)

    def _get_match_result(self, partido: Any, team_id: str) -> int:
        """Calcula el resultado (1:victoria, 0:empate, -1:derrota) para un equipo en un partido."""
        if partido.goles_local == partido.goles_visitante:
            return 0  # Empate
        if partido.equipo_local_id == team_id:
            return 1 if partido.goles_local > partido.goles_visitante else -1
        else: # team_id era visitante
            return 1 if partido.goles_visitante > partido.goles_local else -1

    def _calculate_team_match_stats(self, partido: Any, stats: Any, team_id: str) -> Dict[str, Any]:
        """
        Extrae las estadísticas de un partido para un equipo específico,
        manejando si el equipo era local o visitante en ese partido.
        """
        if not stats: # Si no hay estadísticas para este partido, retorna un diccionario con Nones
            return {
                "goles_a_favor": partido.goles_local if partido.equipo_local_id == team_id else partido.goles_visitante,
                "goles_en_contra": partido.goles_visitante if partido.equipo_local_id == team_id else partido.goles_local,
                "posesion": np.nan, "corners": np.nan, "tarjetas_amarillas": np.nan,
                "tarjetas_rojas": np.nan, "es_local": (partido.equipo_local_id == team_id),
                "resultado": self._get_match_result(partido, team_id)
            }
        
        # Lógica para extraer las stats específicas del equipo en cuestión
        if partido.equipo_local_id == team_id:
            return {
                "goles_a_favor": partido.goles_local,
                "goles_en_contra": partido.goles_visitante,
                "posesion": stats.posesion_local,
                "corners": stats.corners_local,
                "tarjetas_amarillas": stats.tarjetas_amarillas_local,
                "tarjetas_rojas": stats.tarjetas_rojas_local,
                "es_local": True,
                "resultado": self._get_match_result(partido, team_id)
            }
        else: # equipo_visitante_id == team_id
            return {
                "goles_a_favor": partido.goles_visitante,
                "goles_en_contra": partido.goles_local,
                "posesion": stats.posesion_visitante,
                "corners": stats.corners_visitante,
                "tarjetas_amarillas": stats.tarjetas_amarillas_visitante,
                "tarjetas_rojas": stats.tarjetas_rojas_visitante,
                "es_local": False,
                "resultado": self._get_match_result(partido, team_id)
            }

    def _get_team_historical_data(self, team_id: str, match_date: date, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Recopila datos históricos de partidos y estadísticas para un equipo,
        transformándolos a un formato uniforme (goles_a_favor, posesion etc. para ESE equipo).
        """
        matches_with_stats = self.partido_repo.get_historical_matches_with_stats(team_id, match_date, limit=limit)
        processed_data = []
        for partido, stats in matches_with_stats:
            processed_data.append(self._calculate_team_match_stats(partido, stats, team_id))
        return processed_data

    def _get_h2h_historical_data(self, team1_id: str, team2_id: str, match_date: date, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Recopila datos históricos de enfrentamientos directos (H2H) entre dos equipos,
        transformándolos a un formato uniforme.
        """
        matches_with_stats = self.partido_repo.get_h2h_matches_with_stats(team1_id, team2_id, match_date, limit=limit)
        processed_data = []
        for partido, stats in matches_with_stats:
            if stats: # Si hay estadísticas para el H2H
                processed_data.append({
                    "local_goles": partido.goles_local,
                    "visitor_goles": partido.goles_visitante,
                    "local_posesion": stats.posesion_local,
                    "visitor_posesion": stats.posesion_visitante,
                    "local_corners": stats.corners_local,
                    "visitor_corners": stats.corners_visitante,
                    "local_tarjetas_amarillas": stats.tarjetas_amarillas_local,
                    "visitor_tarjetas_amarillas": stats.tarjetas_amarillas_visitante,
                    "local_tarjetas_rojas": stats.tarjetas_rojas_local,
                    "visitor_tarjetas_rojas": stats.tarjetas_rojas_visitante,
                    "resultado_local_perspective": self._get_match_result(partido, team1_id), # Resultado desde la perspectiva de team1
                })
            else: # Si no hay stats para un H2H, rellenar con NaNs para mantener la longitud de la lista
                processed_data.append({key: np.nan for key in [
                    "local_goles", "visitor_goles", "local_posesion", "visitor_posesion",
                    "local_corners", "visitor_corners", "local_tarjetas_amarillas",
                    "visitor_tarjetas_amarillas", "local_tarjetas_rojas", "visitor_tarjetas_rojas",
                    "resultado_local_perspective"
                ]})
        return processed_data

    def _calculate_average_stats(self, data: List[Dict[str, Any]], stat_key: str) -> float:
        """Calcula la media de una estadística de una lista de diccionarios de partidos."""
        # Filtra solo valores numéricos válidos (no None o NaN)
        values = [d[stat_key] for d in data if d.get(stat_key) is not None and not np.isnan(d[stat_key])]
        return np.mean(values) if values else np.nan

    def _calculate_average_h2h_stats(self, data: List[Dict[str, Any]], stat_key_local: str, stat_key_visitor: str) -> Tuple[float, float]:
        """Calcula la media de estadísticas locales y visitantes de una lista de diccionarios H2H."""
        local_values = [d[stat_key_local] for d in data if d.get(stat_key_local) is not None and not np.isnan(d[stat_key_local])]
        visitor_values = [d[stat_key_visitor] for d in data if d.get(stat_key_visitor) is not None and not np.isnan(d[stat_key_visitor])]
        return np.mean(local_values) if local_values else np.nan, np.mean(visitor_values) if visitor_values else np.nan

    def _calculate_avg_goal_diff(self, data: List[Dict[str, Any]]) -> float:
        """Calcula la media de la diferencia de goles (goles_a_favor - goles_en_contra) para un equipo en una lista de partidos."""
        diffs = [d["goles_a_favor"] - d["goles_en_contra"] for d in data if d.get("goles_a_favor") is not None and d.get("goles_en_contra") is not None]
        return np.mean(diffs) if diffs else np.nan

    def _calculate_racha(self, data: List[Dict[str, Any]], result_type: int) -> int:
        """Calcula la racha de victorias, empates o derrotas en una lista de partidos."""
        count = 0
        for d in data:
            if d.get("resultado") is not None and d["resultado"] == result_type:
                count += 1
            else:
                break # La racha se rompe si el resultado no es el esperado o no es None
        return count

    def _calculate_features_for_single_match(
        self,
        local_team_id: str,
        visitor_team_id: str,
        match_date: date
    ) -> Optional[pd.DataFrame]:
        """
        Calcula todas las características para un *único* partido,
        replicando la lógica de features_engineering.py pero consultando la DB.
        """
        features = {}

        # --- Recopilar datos históricos ---
        local_ult10_data = self._get_team_historical_data(local_team_id, match_date, limit=10)
        visitor_ult10_data = self._get_team_historical_data(visitor_team_id, match_date, limit=10)
        h2h_data = self._get_h2h_historical_data(local_team_id, visitor_team_id, match_date, limit=10) # team1_id es local_team_id en H2H
        
        # Históricos completos (sin límite)
        local_hist_data = self._get_team_historical_data(local_team_id, match_date)
        visitor_hist_data = self._get_team_historical_data(visitor_team_id, match_date)
        
        # Últimos 5 partidos para rachas (subconjunto de los últimos 10)
        local_ult5_data = local_ult10_data[:5]
        visitor_ult5_data = visitor_ult10_data[:5]


        # --- Fase 1: medias de últimos 10 partidos (local y visitante) ---
        for stat in ["posesion", "corners", "tarjetas_amarillas", "tarjetas_rojas"]:
            features[f"media_ult10_{stat}_local"] = self._calculate_average_stats(local_ult10_data, stat)
            features[f"media_ult10_{stat}_visitante"] = self._calculate_average_stats(visitor_ult10_data, stat)

        # --- Fase 2: medias de últimos 10 enfrentamientos directos (H2H) ---
        for stat in ["posesion", "corners", "tarjetas_amarillas", "tarjetas_rojas"]:
            local_avg, visitor_avg = self._calculate_average_h2h_stats(h2h_data, f"local_{stat}", f"visitor_{stat}")
            features[f"media_h2h_{stat}_local"] = local_avg
            features[f"media_h2h_{stat}_visitante"] = visitor_avg
        
        # Tendencia de empate H2H (usa resultado_local_perspective)
        if h2h_data:
            empates_h2h = sum(1 for d in h2h_data if d.get("resultado_local_perspective") == 0)
            features["tendencia_empate_h2h"] = empates_h2h / len(h2h_data)
        else:
            features["tendencia_empate_h2h"] = np.nan

        # --- Fase 3: medias históricas acumuladas (local y visitante) ---
        for stat in ["posesion", "corners", "tarjetas_amarillas", "tarjetas_rojas"]:
            features[f"media_hist_{stat}_local"] = self._calculate_average_stats(local_hist_data, stat)
            features[f"media_hist_{stat}_visitante"] = self._calculate_average_stats(visitor_hist_data, stat)

        # --- Fase 4: diferencia de goles en todos los contextos ---
        features["media_ult10_diferencia_goles_local"] = self._calculate_avg_goal_diff(local_ult10_data)
        features["media_ult10_diferencia_goles_visitante"] = self._calculate_avg_goal_diff(visitor_ult10_data)

        # Para H2H, usa los arrays de diferencias calculados en _calculate_h2h_historical_stats si es posible
        # o re-calcula las diferencias para la perspectiva H2H aquí.
        # En la implementación actual, h2h_data ya tiene local_goles/visitor_goles.
        h2h_diffs_local = [d["local_goles"] - d["visitor_goles"] for d in h2h_data if d.get("local_goles") is not None and d.get("visitor_goles") is not None]
        h2h_diffs_visitor = [d["visitor_goles"] - d["local_goles"] for d in h2h_data if d.get("local_goles") is not None and d.get("visitor_goles") is not None]
        features["media_h2h_diferencia_goles_local"] = np.mean(h2h_diffs_local) if h2h_diffs_local else np.nan
        features["media_h2h_diferencia_goles_visitante"] = np.mean(h2h_diffs_visitor) if h2h_diffs_visitor else np.nan

        features["media_hist_diferencia_goles_local"] = self._calculate_avg_goal_diff(local_hist_data)
        features["media_hist_diferencia_goles_visitante"] = self._calculate_avg_goal_diff(visitor_hist_data)

        # --- Fase 5: rachas + diferencias de estadísticas + ventaja histórica en casa + tendencias de empate ---
        
        # Rachas de victorias, empates, derrotas (últimos 5)
        features["racha_ganados_local_ult5"] = self._calculate_racha(local_ult5_data, 1)
        features["racha_empates_local_ult5"] = self._calculate_racha(local_ult5_data, 0)
        features["racha_derrotas_local_ult5"] = self._calculate_racha(local_ult5_data, -1)
        
        features["racha_ganados_visitante_ult5"] = self._calculate_racha(visitor_ult5_data, 1)
        features["racha_empates_visitante_ult5"] = self._calculate_racha(visitor_ult5_data, 0)
        features["racha_derrotas_visitante_ult5"] = self._calculate_racha(visitor_ult5_data, -1)

        # Diferencias de estadísticas (basadas en medias ult10)
        # Estas deben calcularse SIEMPRE, incluso si las medias son NaN, el resultado de la diferencia será NaN.
        features["diferencia_posesion"] = features["media_ult10_posesion_local"] - features["media_ult10_posesion_visitante"]
        features["diferencia_corners"] = features["media_ult10_corners_local"] - features["media_ult10_corners_visitante"]
        features["diferencia_tarjetas_amarillas"] = features["media_ult10_tarjetas_amarillas_local"] - features["media_ult10_tarjetas_amarillas_visitante"]
        features["diferencia_tarjetas_rojas"] = features["media_ult10_tarjetas_rojas_local"] - features["media_ult10_tarjetas_rojas_visitante"]
        
        # Media de goles a favor/en contra históricas (solo cuando el equipo fue local)
        # Esta lógica está bien. local_hist_data ya tiene la info de 'es_local'.
        local_home_matches = [d for d in local_hist_data if d.get("es_local")]
        features["media_hist_goles_local_a_favor"] = self._calculate_average_stats(local_home_matches, "goles_a_favor")
        features["media_hist_goles_local_en_contra"] = self._calculate_average_stats(local_home_matches, "goles_en_contra")
        
        # Ojo: la feature "media_hist_goles_local_en_contra" en tu features_engineering.py original
        # parece que se calcula solo para los partidos donde el equipo LOCAL es el local.
        # Pero si tu modelo espera también media_hist_goles_VISITANTE_a_favor y _en_contra,
        # tendrías que replicar la lógica para el equipo visitante.
        # De momento, nos quedamos con las que tienes en _MODEL_FEATURES.

        # Media de goles en últimos 5 partidos (a favor)
        features["goles_local_ult5_media"] = self._calculate_average_stats(local_ult5_data, "goles_a_favor")
        features["goles_visitante_ult5_media"] = self._calculate_average_stats(visitor_ult5_data, "goles_a_favor")

        # Tendencia de empate (últimos 10 partidos)
        # Revisa que 'resultado' está presente en los diccionarios de local_ult10_data
        if local_ult10_data:
            empates_local = sum(1 for d in local_ult10_data if d.get("resultado") == 0)
            features["tendencia_empate_local"] = empates_local / len(local_ult10_data)
        else:
            features["tendencia_empate_local"] = np.nan

        if visitor_ult10_data:
            empates_visitante = sum(1 for d in visitor_ult10_data if d.get("resultado") == 0)
            features["tendencia_empate_visitante"] = empates_visitante / len(visitor_ult10_data)
        else:
            features["tendencia_empate_visitante"] = np.nan


        # Crear DataFrame con una sola fila
        features_df = pd.DataFrame([features])
        
        # Reindexar las columnas para que coincidan con el orden de _MODEL_FEATURES
        # Esto es crucial para el modelo ML
        features_df = features_df.reindex(columns=self._MODEL_FEATURES)

        # Imputar valores NaN si tu modelo lo requiere (ej. con 0 o la media de entrenamiento)
        # ¡Esto debe coincidir con cómo manejaste los NaNs durante el entrenamiento!
        # Asumimos que el modelo fue entrenado con NaNs imputados a 0.
        features_df = features_df.fillna(0) 

        return features_df

    def predict_match_result(
        self,
        local_team_name: str,
        visitor_team_name: str,
        match_date: date,
        # Usamos Union para especificar los posibles tipos del modelo, más robusto que Any
        ml_model: Union[RandomForestClassifier, Any], # Asumiendo que Any cubre otros clasificadores si cambias
        scaler: StandardScaler
    ) -> Tuple[str, Dict[str, float]]:
        """
        Predice el resultado de un partido y sus probabilidades.
        """
        local_team = self.team_repo.get_team_by_name(local_team_name)
        visitor_team = self.team_repo.get_team_by_name(visitor_team_name)

        if not local_team:
            raise ValueError(f"Equipo local '{local_team_name}' no encontrado.")
        if not visitor_team:
            raise ValueError(f"Equipo visitante '{visitor_team_name}' no encontrado.")

        # Calcular las características para el partido
        features_df = self._calculate_features_for_single_match(
            local_team.equipo_id, visitor_team.equipo_id, match_date
        )

        # Si el DataFrame de features está vacío o todos sus valores son NaN (ej. no hay datos históricos suficientes)
        if features_df is None or features_df.empty or features_df.isnull().all().all():
            raise ValueError("No se pudieron generar las características para la predicción. Faltan datos históricos o son insuficientes para ambos equipos.")

        # Escalar las características
        features_scaled = scaler.transform(features_df)

        # Realizar predicción y obtener probabilidades
        predicted_class = ml_model.predict(features_scaled)[0]
        probabilities = ml_model.predict_proba(features_scaled)[0]

        # Mapear la clase predicha a un resultado legible
        result_map = {1: "Victoria Local", 0: "Empate", -1: "Victoria Visitante"}
        
        # Mapear probabilidades a un diccionario legible
        # Asegúrate de que las clases del modelo estén en el orden correcto
        # Esto es CRÍTICO: ml_model.classes_ devuelve un array con el orden de las clases (ej. [-1, 0, 1])
        class_labels = ml_model.classes_ 
        
        prob_dict = {
            result_map.get(label, str(label)): float(prob)
            for label, prob in zip(class_labels, probabilities)
        }
        
        # Asegurarse de que el orden de las probabilidades en prob_dict sea consistente para el frontend
        # Si las clases de ml_model.classes_ son siempre [-1, 0, 1], este orden es consistente.
        ordered_prob_dict = {
            "Victoria Local": prob_dict.get("Victoria Local", 0.0),
            "Empate": prob_dict.get("Empate", 0.0),
            "Victoria Visitante": prob_dict.get("Victoria Visitante", 0.0),
        }

        return result_map.get(predicted_class, "Desconocido"), ordered_prob_dict

```
---
backend/services/team_services.py
```py

# backend/services/team_service.py
from typing import List, Optional
from sqlalchemy.orm import Session

# Importa el repositorio y el esquema de respuesta
from backend.repositories.team_repository import TeamRepository
from backend.schemas import TeamResponse

class TeamService:
    def __init__(self, db_session: Session):
        self.team_repo = TeamRepository(db_session)

    def get_teams_list(self) -> List[TeamResponse]:
        """
        Obtiene la lista de todos los equipos y los formatea como TeamResponse.
        """
        teams = self.team_repo.get_all_teams()
        return [TeamResponse.model_validate(team) for team in teams]

    def get_team_id_by_name(self, team_name: str) -> Optional[str]:
        """
        Busca un equipo por su nombre y retorna su ID si existe.
        """
        team = self.team_repo.get_team_by_name(team_name)
        return team.equipo_id if team else None


```
---
backend/test/test_prediction_api.py
```py

# backend/tests/test_prediction_api.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
import numpy as np
from datetime import date, timedelta
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch

# Importa la aplicación FastAPI y tus modelos ORM
from backend.main import app
from backend.dependencies import get_db_session, get_prediction_pipeline

from domain.models.base import Base
from domain.models.equipo import Equipo
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido
from domain.models.competicion import Competicion
from domain.models.temporada import Temporada

# Cargar variables de entorno para la conexión a la DB de test
load_dotenv()

# --- Configuración para la base de datos de TEST en MySQL ---
TEST_DB_USER = os.getenv("TEST_DB_USER", os.getenv("DB_USER", "admin"))
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD", os.getenv("DB_PASSWORD", "admin"))
TEST_DB_HOST = os.getenv("TEST_DB_HOST", "localhost")
TEST_DB_PORT = os.getenv("TEST_DB_PORT", "3307")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "futbol_tfg_test")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Override de la dependencia de sesión de DB para usar la DB de test ---
def override_get_db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = override_get_db_session

# --- Mocks para el modelo ML (inicialización segura al nivel del módulo) ---
mock_model_instance = MagicMock()
mock_scaler_instance = MagicMock()

# Configura los mocks para que se comporten como tu modelo espera.
mock_model_instance.classes_ = np.array([-1, 0, 1])
mock_model_instance.predict.return_value = np.array([1])
mock_model_instance.predict_proba.return_value = np.array([[0.1, 0.2, 0.7]])

# --- Fixtures de Pytest (DEBEN ESTAR DEFINIDAS AQUÍ, AL PRINCIPIO DEL MÓDULO) ---
@pytest.fixture(name="db_session_pred_test")
def db_session_pred_test_fixture():
    """
    Fixture de pytest que proporciona una sesión de base de datos MySQL limpia para cada test.
    TRUNCA todas las tablas relevantes antes de cada test.
    """
    db = TestingSessionLocal()
    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        db.execute(text("TRUNCATE TABLE estadisticas_partido"))
        db.execute(text("TRUNCATE TABLE partido"))
        db.execute(text("TRUNCATE TABLE temporada"))
        db.execute(text("TRUNCATE TABLE competicion"))
        db.execute(text("TRUNCATE TABLE equipo"))
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_ml_mocks_globally():
    """
    Fixture que parchea las variables globales de modelo y scaler en dependencies.py
    para que apunten a los mocks, y simula la carga de artefactos ML.
    Se ejecuta automáticamente para todos los tests en este módulo.
    """
    with patch('backend.dependencies.ml_model', new=mock_model_instance), \
         patch('backend.dependencies.scaler', new=mock_scaler_instance), \
         patch('backend.dependencies.load_ml_artifacts', MagicMock(return_value=(mock_model_instance, mock_scaler_instance))):
        yield

@pytest.fixture # <--- ¡NUEVA FIXTURE PARA EL CLIENTE DE TEST!
def client():
    """
    Fixture que proporciona una instancia de TestClient para la aplicación FastAPI.
    Pytest inyectará esta instancia en cualquier función de test que la solicite.
    """
    return TestClient(app)

# --- Función auxiliar para cargar datos de prueba (NO ES UNA FIXTURE) ---
def setup_common_data(db_session: Session):
    """
    Carga datos comunes necesarios para la mayoría de los tests de predicción.
    Estos datos son suficientes para que las features se calculen (al menos sin NaNs).
    """
    # Competicion
    comp = Competicion(competicion_id=9, nombre="Premier League", abreviatura="PL")
    db_session.add(comp)
    db_session.commit()

    # Temporada
    temp = Temporada(temporada_id="2023-2024", año_inicio=2023, año_fin=2024, competicion_id=9)
    db_session.add(temp)
    db_session.commit()

    # Equipos
    team_arsenal = Equipo(equipo_id="ARS", nombre="Arsenal", abreviatura="ARS")
    team_spurs = Equipo(equipo_id="TOT", nombre="Tottenham", abreviatura="TOT")
    team_chelsea = Equipo(equipo_id="CHE", nombre="Chelsea", abreviatura="CHE")
    db_session.add_all([team_arsenal, team_spurs, team_chelsea])
    db_session.commit()

    # Generar datos históricos para que las features no sean todas NaN
    today = date.today()
    for i in range(1, 16):
        p = Partido(
            partido_id=f"P_ARS_{i}", fecha=today - timedelta(days=i*10),
            equipo_local_id="ARS", equipo_visitante_id="CHE" if i%2==0 else "TOT",
            goles_local=i%3 + 1, goles_visitante=(i+1)%3, temporada_id="2023-2024", competicion_id=9
        )
        ep = EstadisticasPartido(
            partido_id=f"P_ARS_{i}", posesion_local=50.0 + (i%5), posesion_visitante=50.0 - (i%5),
            corners_local=5 + i%2, corners_visitante=3 + i%3, tarjetas_amarillas_local=1,
            tarjetas_amarillas_visitante=1, tarjetas_rojas_local=0, tarjetas_rojas_visitante=0
        )
        db_session.add_all([p, ep])

    for i in range(1, 16):
        p = Partido(
            partido_id=f"P_TOT_{i}", fecha=today - timedelta(days=i*10 + 5),
            equipo_local_id="TOT", equipo_visitante_id="CHE" if i%2!=0 else "ARS",
            goles_local=(i+1)%3 + 1, goles_visitante=i%3, temporada_id="2023-2024", competicion_id=9
        )
        ep = EstadisticasPartido(
            partido_id=f"P_TOT_{i}", posesion_local=45.0 + (i%5), posesion_visitante=55.0 - (i%5),
            corners_local=4 + i%2, corners_visitante=2 + i%3, tarjetas_amarillas_local=0,
            tarjetas_amarillas_visitante=2, tarjetas_rojas_local=0, tarjetas_rojas_visitante=0
        )
        db_session.add_all([p, ep])
    
    for i in range(1, 11):
        p_h2h_ars = Partido(
            partido_id=f"H2H_ARS_TOT_{i}", fecha=today - timedelta(days=i*30 + 100),
            equipo_local_id="ARS", equipo_visitante_id="TOT",
            goles_local=2 + (i%2), goles_visitante=1 + (i%2), temporada_id="2023-2024", competicion_id=9
        )
        ep_h2h_ars = EstadisticasPartido(
            partido_id=f"H2H_ARS_TOT_{i}", posesion_local=55.0 + (i%3), posesion_visitante=45.0 - (i%3),
            corners_local=6, corners_visitante=2, tarjetas_amarillas_local=1,
            tarjetas_amarillas_visitante=1, tarjetas_rojas_local=0, tarjetas_rojas_visitante=0
        )
        db_session.add_all([p_h2h_ars, ep_h2h_ars])

        p_h2h_tot = Partido(
            partido_id=f"H2H_TOT_ARS_{i}", fecha=today - timedelta(days=i*30 + 150),
            equipo_local_id="TOT", equipo_visitante_id="ARS",
            goles_local=1 + (i%2), goles_visitante=2 + (i%2), temporada_id="2023-2024", competicion_id=9
        )
        ep_h2h_tot = EstadisticasPartido(
            partido_id=f"H2H_TOT_ARS_{i}", posesion_local=40.0 + (i%3), posesion_visitante=60.0 - (i%3),
            corners_local=3, corners_visitante=5, tarjetas_amarillas_local=0,
            tarjetas_amarillas_visitante=2, tarjetas_rojas_local=0, tarjetas_rojas_visitante=0
        )
        db_session.add_all([p_h2h_tot, ep_h2h_tot])
        
    db_session.commit()


# --- Funciones de Test ---
def test_predict_match_success_mocked_ml_pipeline(client, db_session_pred_test: Session):
    """
    Test que mockea el pipeline ML (modelo y scaler) y permite
    que la lógica de cálculo de features se ejecute realmente.
    """
    mock_scaler_instance.transform.return_value = np.array([[0.5] * 47])

    setup_common_data(db_session_pred_test)

    request_body = {
        "local_team_name": "Arsenal",
        "visitor_team_name": "Tottenham",
        "match_date": "2024-05-15"
    }
    response = client.post("/predict", json=request_body)

    assert response.status_code == 200
    data = response.json()
    assert data["predicted_result"] == "Victoria Local"
    assert data["probabilities"]["Victoria Local"] == pytest.approx(0.7)
    assert data["probabilities"]["Empate"] == pytest.approx(0.2)
    assert data["probabilities"]["Victoria Visitante"] == pytest.approx(0.1)

    mock_model_instance.predict.assert_called_once()
    mock_scaler_instance.transform.assert_called_once()


def test_predict_match_team_not_found(client, db_session_pred_test: Session):
    """
    Test que verifica el manejo de error cuando un equipo no se encuentra.
    """
    setup_common_data(db_session_pred_test)

    request_body = {
        "local_team_name": "EquipoInexistente",
        "visitor_team_name": "Tottenham",
        "match_date": "2024-05-15"
    }
    response = client.post("/predict", json=request_body)
    assert response.status_code == 400
    assert "Equipo local 'EquipoInexistente' no encontrado." in response.json()["detail"]


def test_predict_match_insufficient_historical_data(client, db_session_pred_test: Session):
    """
    Test que verifica el comportamiento de la API cuando no hay suficientes datos históricos
    para calcular las features (ej. equipos nuevos o partidos muy antiguos).
    Según la Opción A, la API debe devolver 200 OK y una predicción (basada en features imputadas a 0).
    """
    # 1. Preparar datos mínimos: solo añadir los equipos, sin historial de partidos.
    team_new = Equipo(equipo_id="NEW", nombre="Equipo Nuevo", abreviatura="NEW")
    team_old = Equipo(equipo_id="OLD", nombre="Equipo Viejo", abreviatura="OLD")
    db_session_pred_test.add_all([team_new, team_old])
    db_session_pred_test.commit()

    # 2. Definir el cuerpo de la solicitud
    request_body = {
        "local_team_name": "Equipo Nuevo",
        "visitor_team_name": "Equipo Viejo",
        "match_date": "2024-05-15"
    }

    # 3. Realizar la solicitud a la API
    response = client.post("/predict", json=request_body)

    # 4. Asertar el comportamiento esperado (según Opción A: 200 OK)
    assert response.status_code == 200 # <--- ¡CAMBIO CRUCIAL AQUÍ!
    
    # Opcional: También puedes verificar el contenido de la respuesta si es relevante
    data = response.json()
    assert "predicted_result" in data
    assert "probabilities" in data
    # Si sabes qué predicción da tu modelo para un vector de ceros, puedes asertarla aquí.
    # Por ejemplo, si un vector de ceros siempre predice "Empate" con 0.5 de prob:
    # assert data["predicted_result"] == "Empate"
    # assert data["probabilities"]["Empate"] == pytest.approx(0.5)


```
---
backend/test/test_teams_api.py
```py

    # backend/tests/test_teams_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# Importa la aplicación FastAPI y tus modelos ORM
from backend.main import app
from backend.dependencies import get_db_session
from domain.models.base import Base # Necesario para crear/dropear tablas
from domain.models.equipo import Equipo # Modelo que vamos a testear

# Cargar variables de entorno para la conexión a la DB de test
load_dotenv()

# --- Configuración para la base de datos de TEST en MySQL ---
# Usaremos una base de datos MySQL específica para tests para aislar los datos.
# Estas variables se leerán de .env o del entorno del Docker Compose si lo configuras
TEST_DB_USER = os.getenv("TEST_DB_USER", os.getenv("DB_USER", "admin"))
TEST_DB_PASS = os.getenv("TEST_DB_PASS", os.getenv("DB_PASS", "admin"))
TEST_DB_HOST = os.getenv("TEST_DB_HOST", os.getenv("DB_HOST", "localhost"))
TEST_DB_PORT = os.getenv("TEST_DB_PORT", os.getenv("DB_PORT", "3307")) # Usar el puerto mapeado por Docker Compose
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "futbol_TFG_test") # Nombre de la DB de test

SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
)

# Crea un engine y sessionmaker para la DB de test
# Es crucial que la DB `futbol_TFG_test` exista en tu servidor MySQL.
# Puedes crearla manualmente o añadir un script para ello.
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Override de la dependencia de sesión de DB para usar la DB de test ---
def override_get_db_session():
    """
    Dependencia que proporciona una sesión de DB para los tests, conectándose a MySQL de test.
    """
    db = TestingSessionLocal()
    try:
        yield db # El test se ejecuta aquí
    finally:
        db.close()

# Aplica el override a la dependencia global de FastAPI
app.dependency_overrides[get_db_session] = override_get_db_session

# Cliente de test para la aplicación FastAPI
client = TestClient(app)

@pytest.fixture(name="db_session_test")
def db_session_test_fixture():
    """
    Fixture de pytest que proporciona una sesión de base de datos limpia para cada test.
    TRUNCA las tablas y carga datos mínimos.
    """
    db = TestingSessionLocal()
    try:
        # Limpiar tablas antes de cada test (¡cuidado con la tabla de producción!)
        # Es importante TRUNCATE y no DROP_ALL/CREATE_ALL si quieres reusar la DB.
        # Asegúrate de que tu DB de test (`futbol_TFG_test`) solo tenga las tablas necesarias.
        db.execute("TRUNCATE TABLE equipo") # Limpia la tabla equipo
        db.commit() # Commit de la limpieza

        yield db # El test se ejecuta aquí

        # Opcional: limpiar de nuevo al final, pero TRUNCATE al inicio suele ser suficiente
        # db.execute("TRUNCATE TABLE equipo")
        # db.commit()
    finally:
        db.close()

def test_get_teams_empty(db_session_test: Session):
    """
    Verifica que el endpoint /teams retorna una lista vacía si no hay equipos.
    """
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == []

def test_get_teams_with_data(db_session_test: Session):
    """
    Verifica que el endpoint /teams retorna los equipos correctamente.
    """
    # Insertar algunos equipos de prueba directamente en la DB de test
    team1 = Equipo(equipo_id="FCB", nombre="FC Barcelona", abreviatura="BAR")
    team2 = Equipo(equipo_id="RMA", nombre="Real Madrid", abreviatura="RMA")
    team3 = Equipo(equipo_id="ATM", nombre="Atlético de Madrid", abreviatura="ATM")
    db_session_test.add(team1)
    db_session_test.add(team2)
    db_session_test.add(team3)
    db_session_test.commit()

    response = client.get("/teams")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Verificar que los datos se devuelven correctamente y ordenados por nombre
    expected_names = ["Atlético de Madrid", "FC Barcelona", "Real Madrid"]
    actual_names = [t["name"] for t in data]
    assert actual_names == expected_names

    assert data[0]["team_id"] == "ATM"
    assert data[0]["abreviatura"] == "ATM"


```
---
backend/main.py
```py

# backend/main.py (VERSION FINAL - para Tarea 2.5)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Tuple
from datetime import date

# Importaciones de tus módulos del backend
from backend.dependencies import get_db_session, load_ml_artifacts, get_prediction_pipeline
from backend.services.team_service import TeamService
from backend.services.prediction_service import PredictionService # ¡NUEVA IMPORTACIÓN!
from backend.schemas import TeamResponse, PredictionRequest, PredictionResponse

# Importaciones de los tipos de modelos ML para type hinting
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

# --- Configuración de la aplicación FastAPI ---
app = FastAPI(
    title="API de Predicción de Partidos de Fútbol",
    description="API para predecir resultados de partidos de fútbol usando Machine Learning.",
    version="1.0.0"
)

# Configurar CORS (ajusta origins según tu frontend)
origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    # Añade aquí la URL de tu frontend en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "API de Predicción de Fútbol iniciada. Visita /docs para la documentación."}

@app.get("/teams", response_model=List[TeamResponse])
async def get_teams(db_session: Session = Depends(get_db_session)):
    """
    Obtiene una lista de todos los equipos disponibles en la base de datos.
    """
    team_service = TeamService(db_session)
    teams = team_service.get_teams_list()
    return teams

@app.post("/predict", response_model=PredictionResponse) # Ya no es 501 NOT IMPLEMENTED
async def predict_match(
    request: PredictionRequest,
    db_session: Session = Depends(get_db_session),
    ml_pipeline: Tuple[MLPClassifier, StandardScaler] = Depends(get_prediction_pipeline)
):
    """
    Predice el resultado de un partido entre dos equipos dados.
    """
    ml_model, scaler = ml_pipeline
    prediction_service = PredictionService(db_session)

    try:
        predicted_result_str, probabilities = prediction_service.predict_match_result(
            request.local_team_name,
            request.visitor_team_name,
            request.match_date or date.today(), # Usa la fecha actual si no se proporciona
            ml_model,
            scaler
        )
        return PredictionResponse(
            predicted_result=predicted_result_str,
            probabilities=probabilities
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado en /predict: {e}") # Para depuración
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor: {e}")

# --- Eventos de la aplicación ---
@app.on_event("startup")
async def startup_event():
    print("Aplicación FastAPI iniciada. Cargando recursos...")
    load_ml_artifacts()
    print("Modelo ML y Scaler cargados (si las rutas son correctas y los archivos existen).")

@app.on_event("shutdown")
async def shutdown_event():
    print("Aplicación FastAPI cerrada.")
```
---


---
backend/dependencies.py
```py

# backend/dependencies.py
import joblib
import os
from sklearn.neural_network import MLPClassifier # Importa el tipo de tu modelo
from sklearn.preprocessing import StandardScaler # Importa el tipo de tu scaler
from sqlalchemy.orm import Session
from typing import Optional, Tuple

# Importa tu función de conexión a la base de datos
from infra.database.mysql_connect import get_session

# Rutas a los modelos ML (se obtienen de las variables de entorno de Docker Compose)
ML_MODEL_PATH = os.getenv("ML_MODEL_PATH")
SCALER_PATH = os.getenv("SCALER_PATH")

# Variables globales para almacenar el modelo y el scaler cargados
ml_model: Optional[MLPClassifier] = None
scaler: Optional[StandardScaler] = None

def load_ml_artifacts():
    """
    Carga el modelo de ML y el scaler una única vez al inicio de la aplicación.
    """
    global ml_model, scaler
    if ml_model is None or scaler is None:
        try:
            print(f"Cargando modelo ML desde: {ML_MODEL_PATH}")
            ml_model = joblib.load(ML_MODEL_PATH)
            print(f"Cargando scaler desde: {SCALER_PATH}")
            scaler = joblib.load(SCALER_PATH)
            print("Modelo ML y Scaler cargados exitosamente.")
        except FileNotFoundError as e:
            print(f"ERROR: Archivo de modelo o scaler no encontrado. Verifica las rutas en docker-compose.yml y Dockerfile.backend. Error: {e}")
            raise RuntimeError(f"Error al cargar recursos ML: {e}. Asegúrate de que los archivos existan en el path esperado dentro del contenedor.")
        except Exception as e:
            print(f"ERROR: Error inesperado al cargar recursos ML: {e}")
            raise RuntimeError(f"Error inesperado al cargar recursos ML: {e}")
    return ml_model, scaler

def get_db_session() -> Session:
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Asegura que la sesión se cierra automáticamente después de la solicitud.
    """
    session = get_session()
    try:
        yield session
    finally:
        session.close()

def get_prediction_pipeline() -> Tuple[MLPClassifier, StandardScaler]:
    """
    Dependencia de FastAPI que proporciona el modelo ML y el scaler cargados.
    Debe ser llamada después de que `load_ml_artifacts` haya inicializado las variables globales.
    """
    if ml_model is None or scaler is None:
        raise RuntimeError("Modelo ML o Scaler no disponibles. Verificar logs de startup.")
    return ml_model, scaler

```
---


---
backend/schemas.py
```py

        from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import date

# --- Schemas para Equipo (lectura) ---
class TeamResponse(BaseModel):
    equipo_id: str = Field(..., description="ID único del equipo (ej. 'ARS', 'RMA')")
    nombre: str = Field(..., description="Nombre completo del equipo (ej. 'Arsenal')")
    abreviatura: str = Field(..., description="Abreviatura del equipo (ej. 'ARS')")

    class Config:
        from_attributes = True  # Usado en Pydantic v2 en lugar de orm_mode = True


# --- Schemas para Predicción ---
class PredictionRequest(BaseModel):
    local_team_name: str = Field(..., alias="equipo_local", description="Nombre del equipo local")
    visitor_team_name: str = Field(..., alias="equipo_visitante", description="Nombre del equipo visitante")
    match_date: Optional[date] = Field(None, description="Fecha del partido (opcional, para contexto histórico de features)")

    class Config:
        populate_by_name = True  # Permite usar los aliases al crear instancias con nombre de campos originales


class PredictionResponse(BaseModel):
    predicted_result: str = Field(..., description="Resultado predicho: 'Victoria Local', 'Empate' o 'Victoria Visitante'")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades de cada resultado (Victoria Local, Empate, Victoria Visitante)")

    # Descomenta si implementas explicaciones SHAP
    # shap_values: Optional[Dict[str, float]] = None
    # base_value: Optional[float] = None


```
---

---
src/index.html
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>TfgFrontend</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root></app-root>
</body>
</html>

```
---
---
src/main.ts
```ts
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

bootstrapApplication(App, appConfig)
  .catch((err) => console.error(err));

```
---
---
src/styles.scss
```scss
/* You can add global styles to this file, and also import other style files */

```
---
---
src/app/app.config.ts
```ts
import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection, importProvidersFrom  } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient() 
  ]
};

```
---
---
src/app/app.html
```html
<!-- src/app/app.html -->
<app-prediction-interface></app-prediction-interface>
```
---
---
src/app/app.routes.ts
```ts
import { Routes } from '@angular/router';

export const routes: Routes = [];

```
---
---
src/app/app.scss
```scss

```
---
---
src/app/app.spec.ts
```ts
import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Hello, tfg-frontend');
  });
});

```
---
---
src/app/app.ts
```ts
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PredictionInterfaceComponent } from './components/prediction-interface/prediction-interface';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,  PredictionInterfaceComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected title = 'tfg-frontend';
}

```
---
---
src/app/components/prediction-interface/prediction-interface.html
```html
<!-- src/app/components/prediction-interface/prediction-interface.html -->


<div class="container">
  <h1>Predictor de Partidos de Fútbol</h1>
  
  <!-- El formulario llama a onSubmit() cuando se envía. #predictionForm es una referencia local. -->
  <form (ngSubmit)="onSubmit()" #predictionForm="ngForm">
    <div class="form-row">
      <!-- Selector Equipo Local -->
      <div class="form-group">
        <label for="homeTeam">Equipo Local</label>
        <!-- [(ngModel)] conecta este select con la variable selectedHomeTeamName -->
        <select id="homeTeam" name="homeTeam" [(ngModel)]="selectedHomeTeamName" required>
          <option [ngValue]="null" disabled>Selecciona un equipo</option>
          <!-- *ngFor recorre la lista de equipos para crear las opciones -->
          <option *ngFor="let team of teams" [value]="team.nombre">{{ team.nombre }}</option>
        </select>
      </div>

      <span class="vs-separator">VS</span>

      <!-- Selector Equipo Visitante -->
      <div class="form-group">
        <label for="awayTeam">Equipo Visitante</label>
        <select id="awayTeam" name="awayTeam" [(ngModel)]="selectedAwayTeamName" required>
          <option [ngValue]="null" disabled>Selecciona un equipo</option>
          <option *ngFor="let team of teams" [value]="team.nombre">{{ team.nombre }}</option>
        </select>
      </div>
    </div>
    
    <div class="form-row">
      <!-- Selector de Fecha -->
      <div class="form-group date-group">
        <label for="predictionDate">Fecha del Partido</label>
        <input type="date" id="predictionDate" name="predictionDate" [(ngModel)]="predictionDate" required>
      </div>
    </div>

    <!-- El botón se deshabilita si el formulario no es válido o si está cargando -->
    <button type="submit" [disabled]="!predictionForm.form.valid || isLoading">
      <span *ngIf="!isLoading">Predecir Resultado</span>
      <span *ngIf="isLoading">Prediciendo...</span>
    </button>
  </form>

  <!-- Contenedor de Resultados y Errores -->
  <div class="results-area">
    <!-- Mensaje de Error (solo se muestra si errorMessage tiene un valor) -->
    <div *ngIf="errorMessage" class="error-message">
      <p><strong>Error:</strong> {{ errorMessage }}</p>
    </div>

    <!-- Resultados (solo se muestra si predictionResult tiene un valor) -->
    <div *ngIf="predictionResult" class="results-container">
      <h2>Resultado de la Predicción</h2>
      <div class="prediction-winner">
        {{ predictionResult.predicted_result }}
      </div>
      <div class="probabilities">
        <h3>Probabilidades</h3>
        <p>Victoria Local (1): <strong>{{ (predictionResult.probabilities['Victoria Local'] * 100).toFixed(1) }}%</strong></p>
        <p>Empate (X): <strong>{{ (predictionResult.probabilities['Empate'] * 100).toFixed(1) }}%</strong></p>
        <p>Victoria Visitante (2): <strong>{{ (predictionResult.probabilities['Victoria Visitante'] * 100).toFixed(1) }}%</strong></p>
      </div>
    </div>
  </div>
</div>

```
---
---
src/app/components/prediction-interface/prediction-interface.scss
```scss
/* src/app/components/prediction-interface/prediction-interface.scss  */

// Definimos los colores como variables de SASS (con $)
$primary-color: #007bff;
$success-color: #28a745;
$error-color: #dc3545;
$light-gray: #f8f9fa;
$gray: #6c757d;
$border-radius: 8px;
$box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

.container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  
  h1 {
    text-align: center;
    color: #333;
    margin-bottom: 2rem;
  }
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  
  .vs-separator {
    font-size: 1.5rem;
    font-weight: bold;
    color: $gray;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  flex-grow: 1;

  label {
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #555;
  }

  select, input[type="date"] {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: $border-radius;
    font-size: 1rem;
    transition: border-color 0.2s;

    &:focus {
      outline: none;
      border-color: $primary-color;
      box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
    }
  }
}

.date-group {
  flex-grow: 0;
  width: 100%;
}

button[type="submit"] {
  padding: 1rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background-color: $primary-color;
  border: none;
  border-radius: $border-radius;
  cursor: pointer;
  transition: background-color 0.2s;

  // Ahora 'darken' puede funcionar porque $primary-color es un color real para SASS
  &:hover:not(:disabled) {
    background-color: darken($primary-color, 10%);
  }

  &:disabled {
    background-color: lighten($primary-color, 20%); // Usamos lighten para el estado deshabilitado
    cursor: not-allowed;
  }
}

.results-area {
  margin-top: 2rem;
  text-align: center;
}

.message {
  padding: 1rem;
  border-radius: $border-radius;
  margin-bottom: 1rem;
  border: 1px solid;
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

.results-container {
  background-color: $light-gray;
  border-color: #ddd;
  
  .prediction-winner {
    font-size: 2rem;
    font-weight: bold;
    color: $primary-color;
    margin-bottom: 1rem;
  }
  
  .probabilities {
    h3 {
      margin-bottom: 0.5rem;
    }
    p {
      margin: 0.25rem 0;
      color: $gray;
    }
  }
}

// Spinner de carga con CSS puro
.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: $primary-color; // Sigue funcionando con variables de SASS
  animation: spin 1s ease infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
```
---
---
src/app/components/prediction-interface/prediction-interface.spec.ts
```ts
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictionInterfaceComponent } from './prediction-interface';

describe('PredictionInterface', () => {
  let component: PredictionInterfaceComponent;
  let fixture: ComponentFixture<PredictionInterfaceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictionInterfaceComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictionInterfaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

```
---
---
src/app/components/prediction-interface/prediction-interface.ts
```ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// Importa los modelos que necesitaremos (aunque solo sea para tipado)
import { Team, PredictionRequest, PredictionResponse } from '../../models/api.models';
// Importa el servicio que vamos a usar
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-prediction-interface',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './prediction-interface.html',
  styleUrl: './prediction-interface.scss'
})
// Implementamos la interfaz OnInit para usar el gancho de ciclo de vida ngOnInit
export class PredictionInterfaceComponent implements OnInit {

  // Creamos una propiedad para guardar los equipos
  teams: Team[] = [];
  predictionResult: PredictionResponse | null = null; // Almacenará el resultado de la predicción

   // --- Propiedades para el estado del formulario (vinculadas con ngModel) ---
  selectedHomeTeamName: string | null = null;
  selectedAwayTeamName: string | null = null;
  // Fecha de hoy en formato YYYY-MM-DD para el input de fecha
  predictionDate: string = new Date().toISOString().split('T')[0];

  // --- Propiedades para la Experiencia de Usuario (UX) ---
  isLoading = false; // Para mostrar un spinner o deshabilitar el botón
  errorMessage: string | null = null; // Para mostrar mensajes de error

  // Paso 1: Inyectamos el ApiService en el constructor.
  // Angular se encarga de crear la instancia y pasárnosla.
  constructor(private apiService: ApiService) { }

  // Paso 2: ngOnInit se ejecuta automáticamente una vez cuando el componente se inicializa.
  // Es el lugar perfecto para cargar datos iniciales.
  ngOnInit(): void {
    console.log('Componente inicializado. Llamando a getTeams()...');

    this.apiService.getTeams().subscribe({
      // Esto se ejecuta si la llamada a la API tiene éxito
      next: (data) => {
        this.teams = data;
      },
      // Esto se ejecuta si hay un error en la llamada
      error: (err) => {
        console.error('¡ERROR! No se pudieron obtener los equipos:', err);
        // Aquí podríamos mostrar un mensaje de error al usuario en el futuro
      }
    });
  }
  // --- Método que se ejecuta al enviar el formulario ---
  onSubmit(): void {
    // 1. Validaciones básicas en el frontend
    if (!this.selectedHomeTeamName || !this.selectedAwayTeamName) {
      this.errorMessage = 'Por favor, selecciona ambos equipos.';
      return;
    }
    if (this.selectedHomeTeamName === this.selectedAwayTeamName) {
      this.errorMessage = 'El equipo local y el visitante no pueden ser el mismo.';
      return;
    }

    // 2. Preparar el estado para una nueva petición
    this.isLoading = true;
    this.errorMessage = null;
    this.predictionResult = null;

    // 3. Crear el objeto de la petición para la API
    const request: PredictionRequest = {
      local_team_name: this.selectedHomeTeamName,
      visitor_team_name: this.selectedAwayTeamName,
      match_date: this.predictionDate
    };

    // 4. Llamar al servicio de la API
    this.apiService.predictMatch(request).subscribe({
      next: (response) => {
        // ¡Éxito! Guardamos el resultado y paramos la carga
        this.predictionResult = response;
        this.isLoading = false;
      },
      error: (err) => {
        // ¡Error! Mostramos el mensaje del backend y paramos la carga
        console.error('Error en la predicción:', err);
        // El error.error.detail es donde FastAPI suele poner los mensajes de HTTPException
        this.errorMessage = err.error?.detail || 'Ocurrió un error inesperado al predecir.';
        this.isLoading = false;
      }
    });
  }
}
```
---
---
src/app/models/api.models.ts
```ts
// src/app/models/api.models.ts

export interface Team {
  equipo_id: string;
  nombre: string;
  abreviatura: string;
}

export interface PredictionRequest {
  local_team_name: string;
  visitor_team_name: string;
  match_date: string; // Formato 'YYYY-MM-DD'
}

export interface PredictionResponse {
  predicted_result: string; // 'Victoria Local', 'Empate', o 'Victoria Visitante'
  probabilities: {
    'Victoria Local': number;
    'Empate': number;
    'Victoria Visitante': number;
  };
}
```
---
---
src/app/services/api.spec.ts
```ts
import { TestBed } from '@angular/core/testing';

import { Api } from './api';

describe('Api', () => {
  let service: Api;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Api);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

```
---
---
src/app/services/api.ts
```ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Importamos los modelos de datos que definimos en la Tarea 3.1
import { Team, PredictionRequest, PredictionResponse } from '../models/api.models';

@Injectable({
  providedIn: 'root' // Esto hace que el servicio esté disponible en toda la aplicación
})
export class ApiService {

  // La URL base de nuestro backend. ¡Asegúrate de que tu backend corre en el puerto 8000!
  private readonly apiUrl = 'http://localhost:8000';

  // Angular nos "inyecta" el cliente HTTP a través del constructor.
  // Esto es la magia de la Inyección de Dependencias.
  constructor(private http: HttpClient) { }

  /**
   * Obtiene la lista completa de equipos desde el endpoint /teams.
   * @returns Un Observable que emitirá un array de objetos Team.
   */
  getTeams(): Observable<Team[]> {
    // Hacemos una petición GET a http://localhost:8000/teams
    // El <Team[]> le dice a TypeScript qué tipo de datos esperamos recibir.
    return this.http.get<Team[]>(`${this.apiUrl}/teams`);
  }

  /**
   * Envía una petición de predicción al endpoint /predict.
   * @param request El objeto con los datos del partido a predecir.
   * @returns Un Observable que emitirá un objeto PredictionResponse.
   */
  predictMatch(request: PredictionRequest): Observable<PredictionResponse> {
    // Hacemos una petición POST a http://localhost:8000/predict
    // El segundo argumento 'request' se enviará como el cuerpo (body) de la petición en formato JSON.
    return this.http.post<PredictionResponse>(`${this.apiUrl}/predict`, request);
  }
}
```
---