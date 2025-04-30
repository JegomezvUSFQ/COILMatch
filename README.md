# Prototipo COIL - Simple

Este prototipo incluye:
- Autenticación básica (botón "Iniciar como Coordinadora")
- Carga y listado de cursos
- Emparejamiento por similitud de texto (TF-IDF)
- Backend con FastAPI y SQLite
- Frontend con React (estructura vacía para completar)

## Requisitos
- Python 3.9+
- Node.js + npm (para frontend)

## Instrucciones backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Instrucciones frontend (React)
```bash
cd frontend
npm install
npm run dev
```

## Acceso
- No hay login con contraseña. Solo haz clic en "Iniciar como Coordinadora".
