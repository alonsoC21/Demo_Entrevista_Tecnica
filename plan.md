# PLAN — Unificación de las dos apps en `unified-app/`

Orden pensado para que cada paso sea verificable por separado y el frontend se integre sobre un backend ya funcionando. El detalle fino (contratos, IDs de DOM, criterios) vive en `spec.md`; el checklist de ejecución en `task.md`.

## Fase 1 — Backend unificado

1. **Scaffolding**: crear `unified-app/` con `main.py`, `database.py` (copiar del dashboard), `requirements.txt` (`fastapi`, `uvicorn`) y `.gitignore` con `database.db`.
2. **Combinar rutas**: llevar `COURSES_DB` + `POST /api/rutas` (con `RutaRequest`/`CursoResponse`) y `GET /api/progreso/{user_id}` a un solo `main.py` con dos `APIRouter`. Quitar los `CORSMiddleware` (mismo origen). **Dejar `app.mount("/", StaticFiles(...))` al final del archivo.**
3. **Semilla**: `python database.py` desde `unified-app/` → verificar que `database.db` aparece ahí.
4. **Smoke test API**: `uvicorn main:app --reload` desde `unified-app/` y comprobar con `curl`:
   - `POST /api/rutas` con `{"categoria":"Tecnología","nivel":"Básico"}` → 3 cursos.
   - `POST /api/rutas` con una combinación inexistente → 404.
   - `GET /api/progreso/1` → los 3 KPIs con la seed actual.
   - `GET /` → `index.html` servido (aunque aún sea el placeholder).

## Fase 2 — Frontend unificado

5. **`index.html`**: partir del HTML del generador; añadir el header con las 2 pestañas y una sección por vista. Dentro de la sección "Mi Progreso", insertar el marcado de KPIs + gráfica del dashboard (sin sus clases CSS originales).
6. **Pestañas (JS)**: controlador mínimo en `app.js` que alterna `hidden` entre secciones y resalta la activa.
7. **Vista ruta**: copiar sin cambios la lógica de `learning-path-generator/static/app.js` (fetch `/api/rutas`, feedback, `renderTimeline`, total de horas) → ya funciona porque el endpoint está montado.
8. **Vista progreso**: copiar `dashboard-elearning/frontend/app.js` con dos cambios: `API_URL` relativa (`/api/progreso/1`) y **init perezosa** al primer click de la pestaña (si no, Chart.js monta el canvas con tamaño 0). Conservar `chartInstance.destroy()` en cada re-render.
9. **`style.css`**: unificar en una sola hoja — timeline del generador + portar `.kpi-grid`, `.card`, `.alert-error`, `.canvas-wrapper` del dashboard a la misma paleta (`#2563eb`).

## Fase 3 — Verificación integral

10. **Manual**: servidor único en `:8000`; probar en navegador ambas pestañas (generar ruta en las 3 categorías, cargar KPIs, cambiar de pestaña ida y vuelta, recargar la página).
11. **Regresión**: comparar `curl` de `/api/progreso/1` antes/después (mismos valores) y confirmar que no quedan llamadas a `http://localhost:8000` hardcodeadas ni fetch a puertos externos (`grep -r "localhost"`).

## Fase 4 — Limpieza y docs

12. **Borrar** `learning-path-generator/` y `dashboard-elearning/`.
13. **Reescribir `README.md` raíz**: una sola app, `pip install -r requirements.txt`, `python database.py`, `python -m uvicorn main:app --reload`, `http://localhost:8000` (sin segundo servidor ni paso de frontend separado).
14. **Actualizar `AGENTS.md`**: secciones de "Current layout" y comandos de los proyectos viejos pasan a describir solo `unified-app/`; marcar la unificación como completada.
15. **Checklist final**: repasar los 5 criterios de aceptación de `spec.md` y cerrar los ítems de `task.md`.

## Riesgos conocidos

- **StaticFiles antes que las rutas API** → el `POST /api/rutas` dejaría de responder: montar siempre al final.
- **Uvicorn desde otra carpeta** → `database.db` vacío en el cwd incorrecto y queries fallando.
- **Chart en canvas oculto** → init perezosa obligatoria al cambiar de pestaña.
- **Data drift en seed** → `database.py` borra y reinserta con fechas relativas a hoy; regenerar antes de comparar valores.
- **Borrado prematuro** → no eliminar los proyectos originales hasta pasar la Fase 3 (son la referencia para comparar comportamiento).
