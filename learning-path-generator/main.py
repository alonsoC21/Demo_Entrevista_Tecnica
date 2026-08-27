from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Configuración básica de logs para QA/Troubleshooting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Generador de Rutas de Aprendizaje API")

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

@app.post("/api/rutas", response_model=list[CursoResponse])
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

# Montar el frontend estático en la raíz para facilitar pruebas de QA
app.mount("/", StaticFiles(directory="static", html=True), name="static")