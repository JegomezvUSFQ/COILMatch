from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

DB = "cursos.db"

class Curso(BaseModel):
    id: int = None
    nombre: str
    descripcion: str
    ideas: str

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            ideas TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/curso")
def agregar_curso(curso: Curso):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO cursos (nombre, descripcion, ideas) VALUES (?, ?, ?)",
              (curso.nombre, curso.descripcion, curso.ideas))
    conn.commit()
    conn.close()
    return {"mensaje": "Curso agregado"}

@app.get("/cursos", response_model=List[Curso])
def listar_cursos():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, nombre, descripcion, ideas FROM cursos")
    data = c.fetchall()
    conn.close()
    return [Curso(id=row[0], nombre=row[1], descripcion=row[2], ideas=row[3]) for row in data]

@app.get("/emparejamientos")
def emparejar():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, descripcion || ' ' || ideas FROM cursos")
    data = c.fetchall()
    conn.close()
    ids, textos = zip(*data)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(textos)
    sim_matrix = cosine_similarity(tfidf_matrix)
    results = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            results.append({
                "cursoA": ids[i],
                "cursoB": ids[j],
                "similitud": round(float(sim_matrix[i][j]), 3)
            })
    return sorted(results, key=lambda x: -x["similitud"])
