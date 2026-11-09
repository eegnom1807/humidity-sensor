# humidity-sensor

Monitoreo de humedad de plantas con sensores conectados a un Arduino.

## Estructura

- `backend/` — API en Flask + SQLite (plantas, sensores, lecturas, imágenes)
- `frontend/` — React + Vite + TypeScript (dashboard y administración)

## Backend

```bash
cd backend
python3 -m venv venv
venv/bin/pip install -r requirements.txt
cp env.example .env        # ajustar valores
venv/bin/flask db upgrade  # crear o actualizar la base
venv/bin/python run.py
```

Agregar una dependencia: `venv/bin/pip freeze > requirements.txt`

## Frontend

```bash
cd frontend
pnpm install
cp env.example .env        # apuntar VITE_API_URL / VITE_API_PORT al backend
pnpm dev
```

## Flujo de ramas

- `develop`: trabajo diario; Dependabot abre aquí sus PRs
- `main`: versión estable
