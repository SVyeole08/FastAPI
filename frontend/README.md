# Stockroom frontend (backend unchanged)

This folder contains only the React/Vite frontend. It uses your original FastAPI routes and request schema; no backend files are included.

## Run
1. Start your existing FastAPI backend on port 8000 (e.g. `uvicorn main:app --reload`).
2. In this folder run `npm install` then `npm run dev`.
3. Open the Vite URL, usually `http://localhost:5173`.

Vite's development proxy forwards `/api/*` to `http://127.0.0.1:8000` and strips `/api`, keeping your backend route definitions untouched.

## Existing API contract used
- `GET /products`
- `GET /product/{id}` (available, not needed for list view)
- `POST /product` JSON body includes `id`, `name`, `description`, `price`, `quantity`
- `PUT /product?id=<id>` JSON body includes the full Product model
- `DELETE /product?id=<id>`

The add form asks for an explicit unused ID because your current Pydantic model requires `id`. This frontend does not modify database sequences or seed behavior.

**Deployment note:** Vite proxy is development-only. For a separately hosted production frontend, use a same-origin reverse proxy to FastAPI; your current backend has no CORS middleware, so direct cross-origin browser calls will be blocked unless CORS is added (which this package deliberately does not do).
