# My FastAPI Project

Este proyecto es una aplicación desarrollada en **FastAPI** que está dockerizada y lista para ejecutarse tanto en local 
como usando Docker y Docker Compose. A continuación, se detallan las instrucciones para arrancar la aplicación, cómo 
acceder a la base de datos, y una breve explicación de los diferentes módulos que componen el proyecto.

## Requisitos Previos
- **Python 3.8+**
- **Poetry** (para la gestión de dependencias en local)
- **Docker** (para ejecutar la aplicación en un contenedor)
- **Docker Compose** (si deseas ejecutar varios servicios en conjunto)

## Arranque de la Aplicación en Local

### 1. Clonar el Repositorio 
```bash\ngit clone https://github.com/tu-usuario/tu-repositorio.git\ncd tu-repositorio\n```
### 2. Instalar Dependencias
Asegúrate de tener `poetry` instalado y luego ejecuta: ```bash\npoetry install\n```
### 3. Ejecutar la Aplicación
Una vez instaladas las dependencias, puedes arrancar la aplicación con el siguiente comando:
```poetry run uvicorn app.main:app --reload``` Esto ejecutará el servidor en `http://127.0.0.1:8000` con 
recarga automática cuando cambies el código.
## Arranque de la Aplicación Usando Docker
### 1. Construir la Imagen de Docker
```docker build -t my-fastapi-app```
### 2. Ejecutar el Contenedor
```docker run -d -p 8000:8000 my-fastapi-app``` 
La aplicación ahora estará corriendo en `http://localhost:8000`
## Usando Docker Compose
Ejecutar Docker Compose```docker-compose up --build```
Esto levantará la aplicación junto con cualquier otro servicio definido en el archivo `docker-compose.yml`
## Acceso a la Base de Datos
Si estás usando SQLite (como se describe en el proyecto):
- El archivo de la base de datos SQLite estará en la carpeta `bd/` dentro del proyecto.
- Para acceder a la base de datos, puedes usar herramientas como [DB Browser for SQLite](https://sqlitebrowser.org/) o 
cualquier otro cliente SQLite. Para acceder desde dentro del contenedor, puedes ejecutar:```docker exec -it <container_id> sqlite3 /app/db/predictions.db```
## Estructura del Proyecto
El proyecto está dividido en varios módulos para mantener la lógica organizada y modular:
- **`app/main.py`**: El punto de entrada de la aplicación. Aquí se inicializa FastAPI y se configuran los routers.
- **`app/routers/`**: Contiene los routers que definen los endpoints de la API. Cada router gestiona un conjunto de endpoints relacionados con una funcionalidad específica:
- - **`csv_upload_router`**: Router que maneja la subida de archivos CSV.  
- - **`model_router`**: Router que maneja el entrenamiento del modelo y las predicciones usando el modelo de Machine Learning entrenado.
- **`app/services/`**: Contiene la lógica de negocio y las operaciones que no están directamente relacionadas con la presentación de la API, como el manejo de archivos, preprocesamiento de datos, y entrenamiento del modelo:
- - **`data_processing.py`**: Módulo que realiza la carga y el preprocesamiento de los datos antes de su uso.
- - **`linear_regression.py`**: Módulo encargado del entrenamiento y predicción usando el modelo de regresión lineal.
- - **`data/`**: Carpeta donde se almacenan los archivos subidos.
- - **`db/`**: Carpeta donde se almacena la base de datos.
- - **`ml_models/`**: Carpeta donde se almacenan las diferentes versiones de los modelos entrenados.
## Tests
### 1. Ejecutar los Tests
Para ejecutar los tests, puedes usar el siguiente comando:```poetry run pytest```
### 2. Ejecutar los Tests con Coverage
Para ejecutar los tests y generar un informe de cobertura, usa el siguiente comando:```poetry run pytest --cov=app 
--cov-report=term-missing``` Este comando hará lo siguiente:
- `--cov=app`: Mide la cobertura de código en el módulo `app`.
- `--cov-report=term-missing`: Muestra en la terminal las líneas de código que no fueron cubiertas por los tests.
### 3. Ver el Informe de Cobertura HTML
Si deseas generar un informe de cobertura en formato HTML, puedes usar el siguiente comando:```poetry run pytest 
--cov=app --cov-report=html```El informe HTML se generará en un directorio llamado `htmlcov`. Puedes abrir el archivo 
`index.html` en un navegador para ver un desglose visual de la cobertura de código.