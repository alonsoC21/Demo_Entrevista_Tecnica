from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import date, timedelta

app = FastAPI(title="E-Learning Dashboard API")

# Habilitar CORS para peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
    return conn

@app.get("/api/progreso/{user_id}")
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
        raise HTTPException(status_code=500, detail="Error interno del servidor")