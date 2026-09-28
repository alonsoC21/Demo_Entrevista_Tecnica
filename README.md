# Pruebas Técnicas - Desarrollo Web (Full-Stack)

> Aplicación web unificada que combina un generador de rutas de aprendizaje y un dashboard analítico de progreso estudiantil, construida con FastAPI, SQLite, Vanilla JS y TailwindCSS.

Esta página reúne las dos funcionalidades de la prueba técnica en **una sola aplicación**: una pestaña para generar una ruta recomendada de cursos y otra para visualizar el progreso de estudio con KPIs y una gráfica semanal.

## Estructura

```
unified-app/
├── main.py            # FastAPI: ambas APIs + serving del frontend
├── database.py        # Inicializa SQLite y genera los datos de prueba
├── requirements.txt   # Dependencias Python
├── .gitignore         # Excluye database.db y .venv
└── static/
    ├── index.html     # Página única con pestañas
    ├── app.js         # Lógica de pestañas + ambas funcionalidades
    └── style.css      # Estilos (timeline, pestañas, dashboard)
```

## Instrucciones de ejecución

Todo se sirve desde **un único servidor** en el puerto 8000.

1. Navega a la carpeta del proyecto:

        cd unified-app

2. Crea un entorno virtual e instala las dependencias *(requerido en sistemas con PEP 668, como Homebrew Python)*:

        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt

3. Inicializa la base de datos (crea `database.db` con los datos de prueba; **borra y regenera** los datos si ya existía):

        python database.py

4. Inicia el servidor:

        python -m uvicorn main:app --reload

5. Abre **http://localhost:8000** — usa las pestañas del header para alternar entre **«Generar Ruta»** y **«Mi Progreso»**. La API interactiva está en `/docs`.

## Funcionalidades

- **Generar Ruta** — Selecciona un área (Tecnología, Ventas, Salud) y un nivel (Básico, Intermedio) y recibe una secuencia de hasta 3 cursos ordenados en un timeline. Endpoint: `POST /api/rutas`.
- **Mi Progreso** — KPIs de cursos terminados, racha de días y horas de los últimos 7 días, más una gráfica de barras. Endpoint: `GET /api/progreso/{user_id}` (datos de prueba: usuario `1`).

## Notas

- Ejecuta siempre los comandos **desde `unified-app/`**: `database.db` y `static/` se resuelven respecto al directorio de trabajo.
- `python database.py` es destructivo: limpia y regenera la semilla con fechas relativas al día actual.

---

## Autor
**Alonso Pardo Córdova**
*Estudiante de Ingeniería en Sistemas Computacionales | Escuela Superior de Cómputo (ESCOM), IPN*
