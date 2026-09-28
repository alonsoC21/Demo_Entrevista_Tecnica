from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import logging
import sqlite3
from datetime import date, timedelta

# Configuración básica de logs para QA/Troubleshooting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="E-Learning Unificado API")

# ---------------------------------------------------------------------------
# Funcionalidad 1: Generador de Rutas de Aprendizaje
# ---------------------------------------------------------------------------
rutas_router = APIRouter(prefix="/api", tags=["rutas"])

# Esquemas de Datos (Pydantic)
class RutaRequest(BaseModel):
    categoria: str
    nivel: str

class CursoResponse(BaseModel):
    id: int
    titulo: str
    descripcion_breve: str
    categoria: str
    nivel: str
    duracion_horas: int

# Base de datos simulada en memoria (18 cursos garantizan 3 por cada combinación)
COURSES_DB = [
    # Categoría: Tecnología
    {"id": 1, "titulo": "Lógica y Algoritmos", "descripcion_breve": "Fundamentos de programación.", "categoria": "Tecnología", "nivel": "Básico", "duracion_horas": 10},
    {"id": 2, "titulo": "Bases de Web", "descripcion_breve": "HTML, CSS y Vanilla JS.", "categoria": "Tecnología", "nivel": "Básico", "duracion_horas": 15},
    {"id": 3, "titulo": "Git y GitHub", "descripcion_breve": "Control de versiones.", "categoria": "Tecnología", "nivel": "Básico", "duracion_horas": 8},
    {"id": 4, "titulo": "Desarrollo Frontend", "descripcion_breve": "Frameworks reactivos.", "categoria": "Tecnología", "nivel": "Intermedio", "duracion_horas": 20},
    {"id": 5, "titulo": "Backend con FastAPI", "descripcion_breve": "Creación de APIs RESTful.", "categoria": "Tecnología", "nivel": "Intermedio", "duracion_horas": 25},
    #{"id": 6, "titulo": "Arquitectura Cloud", "descripcion_breve": "Despliegue y contenedores.", "categoria": "Tecnología", "nivel": "Intermedio", "duracion_horas": 15},

    # Categoría: Ventas
    {"id": 7, "titulo": "Fundamentos de Ventas", "descripcion_breve": "Ciclo de ventas y prospectos.", "categoria": "Ventas", "nivel": "Básico", "duracion_horas": 8},
    {"id": 8, "titulo": "Comunicación Efectiva", "descripcion_breve": "Expresión y escucha activa.", "categoria": "Ventas", "nivel": "Básico", "duracion_horas": 5},
    {"id": 9, "titulo": "Gestión de CRM", "descripcion_breve": "Organización de leads.", "categoria": "Ventas", "nivel": "Básico", "duracion_horas": 10},
    {"id": 10, "titulo": "Negociación B2B", "descripcion_breve": "Técnicas corporativas.", "categoria": "Ventas", "nivel": "Intermedio", "duracion_horas": 12},
    {"id": 11, "titulo": "Cierre Avanzado", "descripcion_breve": "Manejo de objeciones.", "categoria": "Ventas", "nivel": "Intermedio", "duracion_horas": 10},
    {"id": 12, "titulo": "Retención de Clientes", "descripcion_breve": "Fidelización a largo plazo.", "categoria": "Ventas", "nivel": "Intermedio", "duracion_horas": 8},

    # Categoría: Salud
    {"id": 13, "titulo": "Primeros Auxilios", "descripcion_breve": "Soporte vital básico.", "categoria": "Salud", "nivel": "Básico", "duracion_horas": 12},
    {"id": 14, "titulo": "Nutrición Fundamental", "descripcion_breve": "Macronutrientes y dietas.", "categoria": "Salud", "nivel": "Básico", "duracion_horas": 15},
    {"id": 15, "titulo": "Higiene Pública", "descripcion_breve": "Prevención de enfermedades.", "categoria": "Salud", "nivel": "Básico", "duracion_horas": 10},
    {"id": 16, "titulo": "Fisiología Humana", "descripcion_breve": "Sistemas corporales.", "categoria": "Salud", "nivel": "Intermedio", "duracion_horas": 30},
    {"id": 17, "titulo": "Epidemiología Básica", "descripcion_breve": "Propagación de virus.", "categoria": "Salud", "nivel": "Intermedio", "duracion_horas": 20},
    {"id": 18, "titulo": "Gestión Sanitaria", "descripcion_breve": "Administración de clínicas.", "categoria": "Salud", "nivel": "Intermedio", "duracion_horas": 25},
]

@rutas_router.post("/rutas", response_model=list[CursoResponse])
async def generar_ruta(request_data: RutaRequest):
    """
    Recibe categoría y nivel, devuelve exactamente 3 cursos ordenados.
    """
    logger.info(f"Petición recibida: Categoría='{request_data.categoria}', Nivel='{request_data.nivel}'")

    # Filtrar cursos por los criterios solicitados
    cursos_filtrados = [
        curso for curso in COURSES_DB
        if curso["categoria"] == request_data.categoria and curso["nivel"] == request_data.nivel
    ]

    # Validar si hay suficientes cursos
    if len(cursos_filtrados) < 1:
        logger.warning("No se encontraron suficientes cursos para la solicitud.")
        raise HTTPException(
            status_code=404,
            detail="No hay suficientes cursos para generar una ruta con estos criterios."
        )

    # Devolver exactamente los primeros 3 cursos como secuencia lógica
    return cursos_filtrados[:3]

# ---------------------------------------------------------------------------
# Funcionalidad 2: Dashboard de Progreso Estudiantil
# ---------------------------------------------------------------------------
progreso_router = APIRouter(prefix="/api", tags=["progreso"])

def get_db_connection():
    # Ruta relativa al cwd: ejecutar uvicorn y database.py desde unified-app/
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
    return conn

@progreso_router.get("/progreso/{user_id}")
def get_progreso(user_id: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Lógica 1: Total de cursos completados (únicos)
        cur.execute("""
            SELECT COUNT(DISTINCT curso) as terminados
            FROM Actividad_Estudio
            WHERE usuario_id = ? AND completado = 1
        """, (user_id,))
        terminados = cur.fetchone()['terminados']

        # Lógica 2: Desglose de horas en los últimos 7 días
        cur.execute("""
            SELECT fecha, SUM(horas) as total_horas
            FROM Actividad_Estudio
            WHERE usuario_id = ? AND fecha >= date('now', '-6 days')
            GROUP BY fecha
            ORDER BY fecha ASC
        """, (user_id,))
        historial = [dict(row) for row in cur.fetchall()]

        # Lógica 3: Cálculo de la racha de días consecutivos
        cur.execute("""
            SELECT DISTINCT fecha
            FROM Actividad_Estudio
            WHERE usuario_id = ? AND horas > 0
            ORDER BY fecha DESC
        """, (user_id,))
        fechas_estudio = [row['fecha'] for row in cur.fetchall()]

        racha = 0
        fecha_actual = date.today()
        for f_str in fechas_estudio:
            f_date = date.fromisoformat(f_str)
            if f_date == fecha_actual:
                racha += 1
                fecha_actual -= timedelta(days=1)
            else:
                break # Se rompió la racha

        conn.close()

        return {
            "cursos_terminados": terminados,
            "racha_dias": racha,
            "historial_semana": historial
        }

    except Exception as e:
        logger.error(f"Error consultando progreso: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# ---------------------------------------------------------------------------
# Frontend unificado (siempre al final: no debe sombrear las rutas /api/*)
# ---------------------------------------------------------------------------
app.include_router(rutas_router)
app.include_router(progreso_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
