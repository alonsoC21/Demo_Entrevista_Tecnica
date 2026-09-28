# SPEC — App unificada (Generador de Rutas + Dashboard de Progreso)

## Objetivo

Una sola aplicación web (`unified-app/`) que ofrezca las dos funcionalidades actuales en una única página, servida por **un único proceso FastAPI en el puerto 8000**:

1. **Generar Ruta** — formulario (área + nivel) que devuelve una secuencia de hasta 3 cursos en un timeline.
2. **Mi Progreso** — KPIs (cursos terminados, racha, horas 7 días) + gráfica Chart.js, desde SQLite.

Al terminar, se **eliminan** `learning-path-generator/` y `dashboard-elearning/` y se reescribe el `README.md` raíz.

## Decisiones ya tomadas

| Tema | Decisión |
|---|---|
| Ubicación | Carpeta nueva `unified-app/` (no reutilizar las existentes como base viva) |
| Navegación | Header con 2 pestañas/vistas; sin recarga de página (cambio de vista en cliente) |
| Servidor | 1 solo Uvicorn en `:8000`; FastAPI sirve API **y** estáticos |
| CORS | **Se elimina** (mismo origen ya no lo requiere; el fetch del dashboard pasará a ruta relativa) |
| Limpieza | Borrar ambos proyectos originales en la misma tarea, tras verificación |
| Idioma | Todo el texto de UI, comentarios y docs en español |

## Estructura objetivo

```
unified-app/
├── main.py            # FastAPI: rutas de API + mount de estáticos (al final)
├── database.py        # init de SQLite + seed (idéntico al actual, solo cambia cwd implícito)
├── requirements.txt   # fastapi, uvicorn (pydantic viene con fastapi)
├── database.db        # generado, NO commiteado (agregar a .gitignore)
└── static/
    ├── index.html     # una sola página con header + 2 vistas
    ├── app.js         # controlador de pestañas + lógica de cada vista
    ├── style.css      # estilos propios (timeline, KPIs, gráfica)
    └── (CDNs)         # Tailwind, Chart.js
```

## Backend

### Endpoints (contratos sin cambios)

- `POST /api/rutas` — body `{categoria, nivel}` → lista de ≤3 cursos (`id, titulo, descripcion_breve, categoria, nivel, duracion_horas`).
  - Devuelve **404** si no hay cursos que coincidan (comportamiento actual, conservar).
  - Datos en memoria (`COURSES_DB`, 18 cursos; id 6 comentado → Tecnología/Intermedio tiene 2).
- `GET /api/progreso/{user_id}` → `{cursos_terminados, racha_dias, historial_semana[]}`.
  - Streak con `date.today()` (local) vs SQL `date('now')` (UTC): off-by-one conocido, **no** cambiar en esta tarea.
  - `except Exception` → 500 genérico: conservar (el detalle va al log del servidor).

### Reglas de montaje

- `app.mount("/", StaticFiles(directory="static", html=True))` debe ser **la última** línea de `main.py`; todas las rutas `/api/*` van antes.
- Uvicorn siempre se ejecuta **desde `unified-app/`**: `database.db` y `static/` son rutas relativas al cwd.
- Unificar en `main.py` con `APIRouter` (`rutas_router`, `progreso_router`) o funciones en un mismo archivo — prefiero dos routers con `prefix="/api"` para no mezclar responsabilidades.
- Mantener los imports/validaciones Pydantic del generador (`RutaRequest`, `CursoResponse`).

## Frontend

### Layout

- Header fijo: logo/brand + 2 pestañas: **«Generar Ruta»** y **«Mi Progreso»**; activa resaltada (Tailwind).
- Cada pestaña muestra su `<section>` y oculta la otra (clase `hidden`); sin router ni recargas.
- Footer común con enlace a `/docs`.

### Vista 1 — Generar Ruta

- Migrar tal cual el formulario + timeline de `learning-path-generator/static/` (index.html, app.js, style.css) sin cambiar IDs ni lógica de render (`path-form`, `path-results`, `timeline-wrapper`, `feedback-container`, `empty-state`, `path-meta`, `total-hours`).
- `fetch('/api/rutas')` ya es relativo → sin cambios.

### Vista 2 — Mi Progreso

- Migrar KPIs + gráfica de `dashboard-elearning/frontend/`.
- **Cambio obligatorio**: `API_URL = 'http://localhost:8000/api/progreso/1'` → ruta relativa `'/api/progreso/1'` (mismo origen).
- Inicialización **perezosa**: cargar datos al primer click de la pestaña, no en `DOMContentLoaded`; si no, la gráfica se monta en un canvas oculto (Chart.js lo dibuja con tamaño 0).
- Al volver a la pestaña, re-render o destruir+recrear la instancia del chart (ya hay guardia `chartInstance.destroy()`).

### Estilos

- Base visual: conservar el look del generador (paleta `#2563eb`, tarjetas, sombras suaves).
- Portear los bloques del dashboard (`.kpi-grid`, `.card`, `.alert-error`) al CSS propio `style.css` con la misma paleta, en vez de mezclar dos hojas de estilo distintas.

## Restricciones / no hacer

- No añadir frameworks (React, Vite, etc.) ni pasos de build: sigue siendo Vanilla JS + CDN.
- No crear tests/lint/CI: no existen y no forma parte de esta tarea.
- No cambiar contratos de API, semilla de datos ni la lógica de negocio (streak, filtrado, 404).
- No dejar restos: al terminar, borrar `learning-path-generator/` y `dashboard-elearning/` y actualizar el README raíz (pasos de instalación, ejecución única en `:8000`).

## Criterios de aceptación

1. `cd unified-app && python database.py && python -m uvicorn main:app --reload` levanta todo en `http://localhost:8000`.
2. Pestaña 1: generar ruta en las 3 categorías muestra timeline + total de horas; combinación sin cursos muestra el error 404 del backend.
3. Pestaña 2: KPIs y gráfica cargan al entrar por primera vez y al volver; valores coinciden con la seed (`curl` de control).
4. No hay fetch a `localhost:8000` hardcodeado ni segundo servidor.
5. `learning-path-generator/` y `dashboard-elearning/` ya no existen; `README.md` describe solo la app unificada.
