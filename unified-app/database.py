import sqlite3
import datetime

def init_db():
    # Conexión a SQLite 
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # 1. Crear tablas relacionales
    c.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
                    id INTEGER PRIMARY KEY, 
                    nombre TEXT
                )''')
                
    c.execute('''CREATE TABLE IF NOT EXISTS Actividad_Estudio (
                    id INTEGER PRIMARY KEY,
                    usuario_id INTEGER,
                    fecha DATE,
                    curso TEXT,
                    horas REAL,
                    completado BOOLEAN
                )''')
                
    # Limpiar datos previos por si se ejecuta múltiples veces
    c.execute('DELETE FROM Usuarios')
    c.execute('DELETE FROM Actividad_Estudio')

    # 2. Insertar usuario de prueba
    c.execute("INSERT INTO Usuarios (id, nombre) VALUES (1, 'Candidato Full-Stack')")

    # 3. Generar datos de prueba realistas para la última semana
    today = datetime.date.today()
    data = [
        (1, today - datetime.timedelta(days=6), 'Python Intermedio', 2.5, False),
        (1, today - datetime.timedelta(days=5), 'Diseño de Bases de Datos', 1.5, True),
        (1, today - datetime.timedelta(days=4), 'Python Intermedio', 2.0, True),
        (1, today - datetime.timedelta(days=3), 'JavaScript Moderno', 1, False),
        (1, today - datetime.timedelta(days=2), 'JavaScript Moderno', 1.0, False),
        (1, today - datetime.timedelta(days=1), 'APIs con FastAPI', 2.0, False),
        (1, today, 'APIs con FastAPI', 1.5, True)
    ]
    
    c.executemany("""
        INSERT INTO Actividad_Estudio (usuario_id, fecha, curso, horas, completado) 
        VALUES (?, ?, ?, ?, ?)
    """, data)
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

if __name__ == '__main__':
    init_db()