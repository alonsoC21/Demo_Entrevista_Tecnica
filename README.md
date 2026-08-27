# Pruebas Técnicas - Desarrollo Web (Full-Stack)

> Repositorio de pruebas técnicas para desarrollo web full-stack. Contiene dos proyectos interactivos: un algoritmo de recomendación de rutas de aprendizaje y un dashboard analítico de progreso estudiantil construidos con FastAPI, SQLite, Vanilla JS y TailwindCSS.

Este repositorio contiene dos proyectos desarrollados como demostración de habilidades técnicas para la posición de becario en desarrollo web. Ambas aplicaciones son soluciones *full-stack* que abarcan desde el diseño y la interacción en el frontend, hasta la lógica de negocio y gestión de datos en el backend.

## 📂 Estructura del Repositorio

El repositorio se divide en dos proyectos independientes:

1. **`learning-path-generator/`**: Una herramienta de recomendación de cursos basada en criterios de selección.
2. **`dashboard-elearning/`**: Un panel de control (Dashboard) que extrae y visualiza métricas de estudio de una base de datos relacional.

---

## Proyecto 1: Generador de Rutas de Aprendizaje 

Una aplicación web de una sola pantalla que permite a los usuarios seleccionar sus intereses y nivel de experiencia para recibir una ruta secuencial de 3 cursos recomendados, demostrando lógica de filtrado y algoritmos de clasificación básicos.

### 🛠️ Stack Tecnológico
* **Backend:** Python, FastAPI, Pydantic (para validación de esquemas).
* **Frontend:** HTML5, Vanilla JavaScript, TailwindCSS (vía CDN), CSS puro para el diseño del *timeline*.
* **Arquitectura:** Monolito donde FastAPI sirve los archivos estáticos directamente.

###  Instrucciones de Ejecución

1. Navega a la carpeta del proyecto:

        cd learning-path-generator

2. Instala las dependencias necesarias:

        pip install fastapi uvicorn pydantic

3. Ejecuta el servidor backend con Uvicorn:

        uvicorn main:app --reload

4. Abre tu navegador y visita: **[http://localhost:8000](http://localhost:8000)** (El frontend se sirve automáticamente en la raíz gracias a `StaticFiles`).

---

## Proyecto 2: Dashboard de Progreso Estudiantil 

Un panel analítico que muestra el avance de un estudiante a través de KPIs (Cursos Terminados, Racha de Días, Horas Totales) y una gráfica interactiva, extrayendo los datos desde una base de datos relacional.

###  Stack Tecnológico
* **Backend:** Python, FastAPI, SQLite3 (con consultas SQL nativas).
* **Frontend:** HTML5, Vanilla JavaScript, CSS3 puro, Chart.js (vía CDN).
* **Arquitectura:** Cliente-Servidor (API RESTful separada del Frontend).

###  Instrucciones de Ejecución

Este proyecto requiere ejecutar el backend y el frontend por separado.

**Paso 1: Configurar y levantar el Backend**

1. Abre una terminal y navega a la carpeta del backend:

        cd dashboard-elearning/backend

2. Instala las dependencias:

        pip install -r requirements.txt

3. Inicializa la base de datos (esto creará `database.db` y generará los datos de prueba simulados con fechas actualizadas):

        python database.py

4. Inicia el servidor backend:

        uvicorn main_2:app --reload

   *(La API quedará corriendo en el puerto 8000, con CORS habilitado).*

**Paso 2: Levantar el Frontend**

1. Abre una **nueva terminal** (dejando el backend corriendo) y navega a la carpeta del frontend:

        cd dashboard-elearning/frontend

2. Levanta un servidor HTTP de Python para servir los archivos web:

        python -m http.server 8080

3. Abre tu navegador y visita: **[http://localhost:8080](http://localhost:8080)**.

---

##  Notas para el despliegue local
Se recomienda agregar un archivo `.gitignore` en la raíz del repositorio con el siguiente contenido para evitar subir archivos autogenerados o de caché a GitHub:

    __pycache__/
    *.db

*(Nota: La base de datos `.db` es ignorada intencionalmente ya que el script `database.py` la inicializa localmente de forma automática).*

---

##  Autor
**Alonso Pardo Córdova**
*Estudiante de Ingeniería en Sistemas Computacionales | Escuela Superior de Cómputo (ESCOM), IPN*
