# TASK — Checklist de unificación

Ejecutar en orden. Marcar `[x]` solo cuando el paso esté **verificado**, no solo escrito. Basado en `plan.md` / `spec.md`.

## Fase 1 — Backend

- [x] **T1.** Crear `unified-app/` con `main.py`, `database.py` (copiado de `dashboard-elearning/backend/`), `requirements.txt` (`fastapi`, `uvicorn`) y `.gitignore` con `database.db`.
- [x] **T2.** Unificar rutas en `unified-app/main.py` con dos `APIRouter`:
  - `POST /api/rutas` + `COURSES_DB` + `RutaRequest`/`CursoResponse` (desde `learning-path-generator/main.py`).
  - `GET /api/progreso/{user_id}` (desde `dashboard-elearning/backend/main.py`, sin cambios de lógica).
  - Quitar CORS; `app.mount("/", StaticFiles(directory="static", html=True))` como **última línea**.
- [x] **T3.** `python database.py` desde `unified-app/` → existe `unified-app/database.db` con la seed.
- [x] **T4.** Smoke test (`python -m uvicorn main:app --reload` desde `unified-app/`):
  - `curl -X POST localhost:8000/api/rutas -H 'Content-Type: application/json' -d '{"categoria":"Tecnología","nivel":"Básico"}'` → 3 cursos.
  - Misma llamada con categoría inexistente → 404.
  - `curl localhost:8000/api/progreso/1` → `cursos_terminados`, `racha_dias`, `historial_semana`.

## Fase 2 — Frontend

- [x] **T5.** `static/index.html`: base = generador; header con pestañas «Generar Ruta» / «Mi Progreso»; sección 2 con KPIs + `<canvas id="progresoChart">` + `#error-alert` del dashboard; footer común con `/docs`.
- [x] **T6.** Controlador de pestañas en `static/app.js`: alterna clases `hidden`, resalta activa, sin recarga.
- [x] **T7.** Migrar lógica de la vista ruta (fetch `/api/rutas`, `renderTimeline`, `feedback-container`, `empty-state`, `total-hours`) conservando los mismos IDs de DOM.
- [x] **T8.** Migrar lógica de la vista progreso con: `API_URL` → `'/api/progreso/1'` (relativa) e **init perezosa** al primer click de la pestaña; conservar `chartInstance.destroy()` antes de re-render.
- [x] **T9.** `static/style.css`: una sola hoja = timeline (generador) + estilos de KPIs/tarjetas/gráfica portados del dashboard a la misma paleta.

## Fase 3 — Verificación

- [x] **T10.** Navegador con servidor único en `:8000`: generar ruta en Tecnología/Ventas/Salud, cambiar de pestaña ida y vuelta, recargar la página. Sin errores de consola. *(Verificado por el usuario: "todo funciona correctamente". Verificación estática previa: IDs DOM cruzados, `node --check`, curl.)*
- [x] **T11.** `grep -r "localhost" unified-app/` → sin URLs hardcodeadas en el JS; sin segundo servidor (`:8080`) en ninguna instrucción nueva.

## Fase 4 — Limpieza

- [x] **T12.** Borrar `learning-path-generator/` y `dashboard-elearning/`.
- [x] **T13.** Reescribir `README.md` raíz: app única, comandos desde `unified-app/`, sin paso de frontend separado.
- [x] **T14.** Actualizar `AGENTS.md`: quitar secciones de los proyectos viejos, describir solo `unified-app/`, marcar unificación completada.
- [x] **T15.** Pasada final sobre los 5 criterios de aceptación de `spec.md`.

---

**Estado:** ✅ completado — T1–T15 verificados (prueba visual en navegador incluida).
